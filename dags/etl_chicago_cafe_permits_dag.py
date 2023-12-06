from calendar import c
from logging import config
from utils.modify_file_name import modify_file_name
from utils.format_url import format_url
from utils.get_time_period import get_time_period
from dags.utils.rename_columns import rename_columns_name
from utils.drop_duplicates import drop_duplicates
from utils.drop_full_null_rows import drop_full_null_rows
from utils.drop_full_null_columns import drop_full_null_columns
from utils.drop_missing import drop_missing
import polars as pl
import pandas as pd
from airflow.decorators import dag
from airflow.utils.helpers import chain
from airflow.operators.bash import BashOperator
from astro import sql as aql
from astro.files import File
from astro.sql.table import Table, Metadata
from astro.databases.google.bigquery import BigqueryDatabase
from pendulum import datetime, duration
import logging
import os
from include.soda.check_function import check
from ydata_profiling import ProfileReport, compare
from duckdb_provider.hooks.duckdb_hook import DuckDBHook
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateEmptyDatasetOperator
)


# Reference: https://catalog.data.gov/dataset/sidewalk-cafe-permits

# get the airflow.task logger
task_logger = logging.getLogger("airflow.task")

SODA_PATH = "include/soda"
DUCKDB_CONN_ID = "duckdb_conn"
DUCKDB_POOL_NAME = "duckdb_pool"
LOCAL_DUCKDB_STORAGE_PATH = "include/my_local_ducks.db"
BIGQUERY_CONN_ID = "gcp"
gcp_project_name = os.getenv("GCP_PROJECT_NAME", "chicago-cafe-permits") 
bigquery_dataset_name = os.getenv("BIGQUERY_DATASET", "cafe_permits")


@aql.dataframe(pool=DUCKDB_POOL_NAME, columns_names_capitalization="original")
def transform_data(df: pd.DataFrame):
    """Apply some transformations to DataFrame"""
    df_pl = pl.from_pandas(df).lazy()
    df_pl = (
        df_pl.pipe(rename_columns_name)  # Convert all columns to lowercase
        .pipe(drop_duplicates)  # Drop duplicate rows
        .pipe(drop_full_null_rows)  # Drop a row only if all values are null
        .pipe(drop_missing)
    )

    df_pl = drop_full_null_columns(df_pl.collect())
    return df_pl.to_pandas()


@aql.dataframe(pool=DUCKDB_POOL_NAME)
def create_report(df: pd.DataFrame, prefix: str):
    """Create a report from DataFrame"""
    profile = ProfileReport(
        df, title=f"Chicago Sidewalk Cafe Permits - {prefix.capitalize()}"
    )
    profile.to_file(
        os.path.join(
            "include/reports/",
            f"chicago_{prefix}_profiling_report_{get_time_period()}.html",
        )
    )


@aql.dataframe(pool=DUCKDB_POOL_NAME)
def create_comparison_report(raw_df: pd.DataFrame, trans_df: pd.DataFrame):
    """Create a comparison report"""
    raw_report = ProfileReport(raw_df, title="Chicago Sidewalk Cafe Permits - Raw data")
    transformed_report = ProfileReport(
        trans_df, title="Chicago Sidewalk Cafe Permits - Transformed data"
    )
    comparison_report = compare([raw_report, transformed_report])
    comparison_report.to_file(
        os.path.join("include/reports/", f"chicago_comparison_{get_time_period()}.html")
    )

@aql.dataframe(pool=DUCKDB_POOL_NAME)
def soda_check_transform(df: pd.DataFrame):
    """Apply data quality check with SODA"""
    my_duck_hook = DuckDBHook.get_hook(DUCKDB_CONN_ID)
    con = my_duck_hook.get_conn()
    con.sql(
        """
        CREATE OR REPLACE VIEW transformed_permits_view AS
        SELECT *
        FROM df
        """
    )
    result = check(
        scan_name="transformation",
        duckdb_conn=con,
        data_source="duckdb",
        checks_subpath="transform",
    )
    con.close()
    return result


@aql.dataframe(pool=DUCKDB_POOL_NAME, columns_names_capitalization="lower")
def soda_check_raw(df: pd.DataFrame):
    """Apply data quality check with SODA"""
    my_duck_hook = DuckDBHook.get_hook(DUCKDB_CONN_ID)
    con = my_duck_hook.get_conn()
    con.sql(
        """
        CREATE OR REPLACE VIEW raw_permits_view AS
        SELECT *
        FROM df
        """
    )

    result = check(
        scan_name="raw", checks_subpath="sources", duckdb_conn=con, data_source="duckdb"
    )
    con.close()
    return result

@aql.dataframe(pool=DUCKDB_POOL_NAME)
def load_to_bigquery(df: pd.DataFrame):
    """Load DataFrame to BigQuery"""
    BigqueryDatabase(
        conn_id=BIGQUERY_CONN_ID, 
        table=f"{gcp_project_name}.{bigquery_dataset_name}"
        ).load_pandas_dataframe_to_table(
            source_dataframe=df,
            target_table=Table(
                name="cafe_permits", 
                conn_id=BIGQUERY_CONN_ID,
                metadata=Metadata(schema='cafe_permits')),
            if_exists='replace',)
    return None

# Define some default arguments for DAG
default_args = {
    "owner": "Matheus",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": duration(seconds=10),
}

@dag(
    start_date=datetime(2023, 10, 1),
    schedule="@once",
    catchup=False,
    tags=["Sidewalk Cafe Permits"],
    default_args=default_args,
    description="""A list of permits for sidewalk cafes -- outdoor 
    restaurant seating on the public way.""",
)
def etl_chicago_cafe_permits():
    """DAG to extract, transform and load Chicago cafe permits data"""

    name, url = (
        "Sidewalk Cafe Permits",
        "https://data.cityofchicago.org/api/views/nxj5-ix6z/rows.csv?accessType=DOWNLOAD",
    )

    # Format the file name
    name = modify_file_name(name)

    # Format the URL
    url = format_url(url)

    # Log the formatted URL and name
    task_logger.info(f"Selected item URL (Formatted): {url}")
    task_logger.info(f"Selected item name (Formatted): {name}")

    # Create a pool to avoid operations conflits in database
    create_duckdb_pool = BashOperator(
        task_id="create_duckdb_pool",
        bash_command=f"airflow pools list | grep -q '{DUCKDB_POOL_NAME}' || airflow pools set {DUCKDB_POOL_NAME} 1 'Pool for duckdb'",
    )

    # Load file and save it as Table
    load_ducks = aql.load_file(
        task_id="load_csv_to_duckdb",
        input_file=File(path=url),
        output_table=Table(
            name="raw_permits",
            conn_id=DUCKDB_CONN_ID,
            temp=False,
        ),
        if_exists="replace",
    )

    # Transform raw table and save it as Table
    transformed = transform_data(
        df=load_ducks,
        output_table=Table(
            name="transformed_permits",
            conn_id=DUCKDB_CONN_ID,
            temp=False,
        ),
    )
    
    # Create an empty dataset in BigQuery
    create_cafe_permits_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id='create_cafe_permits_dataset',
        dataset_id=bigquery_dataset_name,
        gcp_conn_id=BIGQUERY_CONN_ID)

    # Export transformed data to BigQuery
    export_to_bigquery = load_to_bigquery(transformed)
    
    # Chain tasks
    chain(
        create_duckdb_pool,
        load_ducks,
        soda_check_raw(load_ducks),
        create_report(load_ducks, prefix="raw"),
        transformed,
        soda_check_transform(transformed),
        create_report(df=transformed, prefix="transformed"),
        create_comparison_report(load_ducks, transformed),
        create_cafe_permits_dataset,
        export_to_bigquery,
        aql.cleanup(),
    )


etl_chicago_cafe_permits()
