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
from loguru import logger
from airflow.decorators import dag, task
from airflow.utils.helpers import chain
from airflow.operators.bash import BashOperator
from astro import sql as aql
from astro.files import File
from astro.sql.table import Table
from pendulum import datetime, duration
import duckdb
import logging
from include.soda.check_function import check

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


@aql.transform(pool=DUCKDB_POOL_NAME)
def count_items(in_table):
    return "SELECT count(*) FROM {{ in_table }}"
    
    
@aql.dataframe(pool=DUCKDB_POOL_NAME)
def soda_check_transformation(df: pd.DataFrame):
    with duckdb.connect(":memory:") as con:
            con.sql(
                """\
                CREATE VIEW ducks_cafe_permits AS
                SELECT *
                FROM df
                """
            )
    
            check(scan_name='transformation', 
                  db_conn=con, 
                  data_source='duckdb',
                  checks_subpath=None)
    

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
    restaurant seating on the public way. Businesses may begin sidewalk
    cafe operations on March 1 and operate through December 1.""",
)
def etl_chicago_cafe_permits():
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

    create_duckdb_pool = BashOperator(
        task_id="create_duckdb_pool",
        bash_command=f"airflow pools list | grep -q '{DUCKDB_POOL_NAME}' || airflow pools set {DUCKDB_POOL_NAME} 1 'Pool for duckdb'",
    )

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

    create_duckdb_pool >> load_ducks 

    count = count_items(load_ducks)
    
    print(count)
    
    task_logger.info(f"COUNT(*) before transformations: {count}")
    
    transformed = transform_data(
        df=load_ducks,
        output_table=Table(
            name="ducks_cafe_permits", conn_id=DUCKDB_CONN_ID
        ),
    )
       
    count2 = count_items(transformed)
    
    print(count2)
    
    task_logger.info(f"COUNT(*) after transformations: {count}")

    # @task.external_python(python='/usr/local/airflow/soda_venv/bin/python')
    # def check_transformation(scan_name="transformation"):
    #     from include.soda.check_function import check

    #     return check(scan_name, None)


    # Write SQL tables to CSV or parquet files and store them
    #gcs_bucket = os.getenv("GCS_BUCKET", "gs://dag-authoring")

    export_file = aql.export_to_file(
        task_id="save_file_to_bigquery",
        input_data=transformed,
        output_file=File(
        path= "include/data/cafe_permits.csv" #f"{gcs_bucket}/{{{{ task_instance_key_str }}}}/cafe_permits.csv",
        #conn_id=BIGQUERY_CONN_ID,
        ),
        if_exists="replace",
    )

    chain(soda_check_transformation(transformed),
          export_file,
          aql.cleanup()
        )   

etl_chicago_cafe_permits()
