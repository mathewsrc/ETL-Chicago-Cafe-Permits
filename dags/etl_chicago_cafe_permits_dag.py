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
from astro.sql.table import Table
from pendulum import datetime, duration
import duckdb
import logging
import os
from include.soda.check_function import check
from ydata_profiling import ProfileReport, compare

# Reference: https://catalog.data.gov/dataset/sidewalk-cafe-permits

# get the airflow.task logger
task_logger = logging.getLogger("airflow.task")

SODA_PATH = "include/soda"
DUCKDB_CONN_ID = "duckdb_conn"
DUCKDB_POOL_NAME = "duckdb_pool"
LOCAL_DUCKDB_STORAGE_PATH = "include/my_local_ducks.db"
BIGQUERY_CONN_ID = "bigquery_conn"


@aql.dataframe(pool=DUCKDB_POOL_NAME)
def transform_data(df: pd.DataFrame):
    """Apply some transformations to DataFrame"""
    df_pl = pl.from_pandas(df).lazy()
    df_pl = (
        df_pl.pipe(rename_columns_name)  # Convert all text columns to lowercase
        .pipe(drop_duplicates)  # Drop duplicate rows
        .pipe(drop_full_null_rows)  # Drop a row only if all values are null
        .pipe(rename_columns_name)
        .pipe(drop_missing)
    )

    df_pl = drop_full_null_columns(df_pl.collect())
    return df_pl.to_pandas()


@aql.dataframe(pool=DUCKDB_POOL_NAME)
def create_report(df: pd.DataFrame, prefix: str):
    """Create a report from DataFrame"""
    profile = ProfileReport(df, title=f"Chicago Sidewalk Cafe Permits - {prefix.capitalize()}")
    profile.to_file(
        os.path.join(
            "include/reports/", f"chicago_{prefix}_profiling_report_{get_time_period()}.html"
        )
    )


@aql.dataframe(pool=DUCKDB_POOL_NAME)
def create_comparison_report(raw_df: pd.DataFrame, trans_df: pd.DataFrame):
    """Create a comparison report"""
    raw_report = ProfileReport(raw_df, title="Chicago Sidewalk Cafe Permits - Raw data")
    transformed_report = ProfileReport(trans_df, title="Chicago Sidewalk Cafe Permits - Transformed data")
    comparison_report = compare([raw_report, transformed_report])
    comparison_report.to_file(
        os.path.join("include/reports/", f"chicago_comparison_{get_time_period()}.html")
    )


@aql.transform(pool=DUCKDB_POOL_NAME)
def count_items(in_table):
    """Count the total of rows in table"""
    return "SELECT count(*) FROM {{ in_table }}"


@aql.dataframe(pool=DUCKDB_POOL_NAME)
def soda_check_transformation(df: pd.DataFrame):
    """Apply data quality check with SODA"""
    con = duckdb.connect(":memory:")
    con.sql(
        """\
        CREATE VIEW transformed AS
        SELECT *
        FROM df
        """
    )

    result = check(
        scan_name="transformation",
        db_conn=con,
        data_source="duckdb",
        checks_subpath=None,
    )
    con.close()
    return result


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
        input_file=File(
            path=url
        ),  # File(path='gcs://bucket//nyc_jobs.csv', conn_id=GCP_CONN_ID)
        output_table=Table(
            name="raw_duckdb", conn_id=DUCKDB_CONN_ID
        ),  # Table(name="raw_ny_job", conn_id=GCP_CONN_ID)
        if_exists="replace",
    )

    # Count the total rows in raw table
    count = count_items(load_ducks)
    task_logger.info(f"COUNT(*) before transformations: {count}")

    # Transform raw table and save it as Table
    transformed = transform_data(
        df=load_ducks,
        output_table=Table(name="ducks_cafe_permits", conn_id=DUCKDB_CONN_ID),
    )

    # Count the total rows in transformed table
    count2 = count_items(transformed)
    task_logger.info(f"COUNT(*) after transformations: {count}")

    # Write SQL tables to CSV or parquet files and store them
    # gcs_bucket = os.getenv("GCS_BUCKET", "gs://dag-authoring")
    export_file = aql.export_to_file(
        task_id="save_file_to_bigquery",
        input_data=transformed,
        output_file=File(
            path=f"include/data/chicago_sidewalk_cafe_permits_{get_time_period()}.csv"  # f"{gcs_bucket}/{{{{ task_instance_key_str }}}}/cafe_permits.csv",
            # conn_id=BIGQUERY_CONN_ID,
        ),
        if_exists="replace",
    )

    # Chain tasks
    chain(
        create_duckdb_pool,
        load_ducks,
        [create_report(df=load_ducks, prefix="raw"), count],
        transformed,
        soda_check_transformation(transformed),
        [create_report(df=transformed, prefix="transformed"), count2],
        create_comparison_report(raw_df=load_ducks, trans_df=transformed),
        export_file,
        aql.cleanup(),
    )


etl_chicago_cafe_permits()
