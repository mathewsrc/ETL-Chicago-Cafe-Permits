[![CI](https://github.com/mathewsrc/ETL-Chicago-Cafe-Permits/actions/workflows/main.yml/badge.svg)](https://github.com/mathewsrc/ETL-Chicago-Cafe-Permits/actions/workflows/main.yml)

# Streamlined ETL Process: Unleashing  Airflow, BigQuery, Looker, Polars, Soda, DuckDB and YData Profiling

Contact:

https://www.linkedin.com/in/matheusrc/

## Project Summary:

This ETL (Extract, Transform, Load) project employs several Python libraries, including Polars, Airflow, Soda, YData Profiling, DuckDB, Requests, BeautifulSoup, Loguru, and the Google Cloud Services BigQuery and Looker Studio to streamline the extraction, transformation, and loading of CSV dataset from the [Chicago Sidewalk Cafe Permits](https://catalog.data.gov/dataset/sidewalk-cafe-permits). 

You can check the dataset table at: https://data.cityofchicago.org/widgets/qnjv-hj2q?mobile_redirect=true

## Sections

* [Architecture overview](#architecture-overview)
* [Architecture of continuous integration with GitHub Actions](#architecture-of-continuous-integration-with-github-actions)
* [BigQuery table](#bigquery-table)
* [Looker dashboard](#looker-dashboard)
* [Workflow with Airflow](#workflow-with-airflow)
  * [Part 1](#part-1)
  * [Part 2](#part-2)
  * [Part 3](TODO)
* [Project structure](#project-structure)
* [Prerequites](#prerequisites)
* [Running this project](#running-this-project)
* [Creating a new connection to DuckDB](#creating-a-new-connection-to-duckdb)
* [Creating a new connection to Google Cloud](#creating-a-new-connection-to-google-cloud)
  
## Architecture overview 

![etl_airflow_soda_bigquery_looker](https://github.com/mathewsrc/ETL-Chicago-Cafe-Permits/assets/94936606/f2c386dd-0125-4dcb-a96e-b89df6669786)


## Architecture of continuous integration with GitHub Actions


![etl_ci drawio](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/04b81049-e0f8-4336-a059-bea6640402ce)


## BigQuery table

![image](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/33d8424e-e860-4796-b996-cd1ffb9df20a)


### BigQuery query to create report view and export it to Looker Studio

```sql
CREATE OR REPLACE VIEW chicago-cafe-permits.cafe_permits.vw_report
OPTIONS(
  description='Number of permits by legal name and doing business name',
  labels=[('legal_name', 'total_permits')],
  expiration_timestamp=TIMESTAMP_ADD(CURRENT_TIMESTAMP(), INTERVAL 60 DAY)
) AS
SELECT 
  legal_name,
  doing_business_as_name,
  street_type,
  city,
  state,
  latitude,
  longitude,
  issued_date,
  expiration_date,
  payment_date,
  site_number,
  COUNT(DISTINCT(permit_number)) AS total_permits,
  COUNT(site_number) AS total_sites,
  ST_GEOGPOINT(latitude, longitude) AS geo,
  CASE 
    WHEN expiration_date > issued_date THEN 'TRUE'
    ELSE 'FALSE'
  END AS expired
FROM `chicago-cafe-permits.cafe_permits.cafe_permits`
GROUP BY legal_name, doing_business_as_name, street_type, city,state, issued_date, expiration_date, payment_date,site_number, latitude, longitude, expired;


SELECT * FROM `chicago-cafe-permits.cafe_permits.vw_report`;
```

## Looker dashboard

![image](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/37dd0503-1244-48ea-b711-1c263a4f2a62)

## Workflow with Airflow 

### Part 1

![image](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/6dd0e4b4-bbab-43ac-9db6-48ec2e6bbf20)

1. I created a concurrency of 1 using the ```BashOperator``` to avoid two or more executions against DuckDB as allowing two or more calls to DuckDB would cause an error
2. I loaded the CSV file using an HTTP call by leveraging the Astro Python SDK `astro.sql.load_file` function and the DuckDB connection that I created in Airflow `Admin/Connections`
3. Then, I create a task to check raw data quality using [Soda](https://docs.soda.io/)
5. Next, I created a task to generate a data profiling 
6. Finally, I create a transform task using the Astro Python SDK ```astro.sql.dataframe``` operator to apply the following transformations: lower column name, remove duplicated rows, remove missing values, and drop a row if all values are null


### Part 2

![image](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/91fc7347-2e70-495e-84c6-f0a9079994fe)

1. After the transformation of data I used Soda to check data quality to ensure that data was transformed as expected
2. Next, I created a task to create a data profiling 
3. Finally, I created a task to create a data profiling comparing the raw data with the transformed data

### Part 3 

![image](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/e5f95838-d437-4aac-9ae9-86c8eecf1a22)

1. I used the ```BigQueryCreateEmptyDatasetOperator``` operator to create a new empty dataset in BigQuery
2. Then, I used Astro Python SDK ```BigqueryDatabase..load_pandas_dataframe_to_table``` function to load data into BigQuery
3. Finally, I used the Astro Python SDK ```astro.sql.cleanup()``` function to clean up all tables  

## Project structure
------------

```
├── .devcontainer                        # VS Code development container 
|   └── devcontainer.json                
├── .github                              # GitHub Actions for continuous integration (CI) 
|   └── workflows
|       └── main.yml                     # GitHub Actions configurations 
├── Dockerfile
├── LICENSE
├── Makefile                             # Makefile with some helpful commands  
├── README.md
├── airflow_settings.yaml
├── dags
│   ├── __init__.py
│   ├── etl_chicago_cafe_permits_dag.py
│   ├── example_etl.py
│   └── utils
│       ├── __init__.py
│       ├── drop_duplicates.py           # Function to remove duplicates
│       ├── drop_full_null_columns.py    # Function to drop columns if all values are null
│       ├── drop_full_null_rows.py       # Function to drop rows if all values in a row are null
│       ├── drop_missing.py              # Function to drop rows with missing values
│       ├── format_url.py                # Function to format the URL
│       ├── get_time_period.py           # Function to get the current period
│       ├── modify_file_name.py          # Function to create a formatted file name
│       └── rename_columns.py            # Function to rename DataFrame columns name
├── format.sh                            # Bash script to format code with ruff  
├── include
│   ├── data
│   │   ├── chicago_sidewalk_cafe_permits_2023_11.csv
│   │   └── jobs_nyc_postings_2023_10.csv
│   ├── my_local_ducks.db
│   ├── my_local_ducks.db.wal
│   ├── reports                          # Directory with reports
│   │   ├── chicago_comparison_2023_11.html
│   │   ├── chicago_raw_profiling_report_2023_11.html
│   │   └── chicago_transformed_profiling_report_2023_11.html
│   └── soda                             # Directory with SODA files
│       ├── check_function.py            # Helpful function for running SODA data quality checks 
│       ├── checks                       # Directory containing data quality rules YML files
│       │   ├── sources
│       │   │   └── raw.yml              # Soda data quality check for raw data 
│       │   └── transform
│       │       └── transformed.yml      # Soda data quality check for transformed data 
│       └── configuration.yml            # Configurations to connect Soda to a data source (DuckDB)
├── lint.sh                              # Bash script to format code with ruff  
├── notebooks                            # COLAB notebooks
│   └── gov_etl.ipynb
├── packages.txt
├── plugins
├── requirements.txt
├── setup_data_folders.sh                # Bash script to create some directories
├── source_env_linux.sh                  # Bash script to create a Python virtual environment in linux
├── source_env_windows.sh                # Bash script to create a Python virtual environment in windows
├── test.sh                              # Bash script to test code with pytest 
└── tests                                # Diretory for Python test files
    ├── __init__.py
    ├── dags
    │   └── test_dag_example.py
    └── utils
        ├── __init__.py
        ├── test_drop_duplicates.py
        ├── test_drop_full_null_columns.py
        ├── test_drop_full_null_rows.py
        ├── test_drop_missing.py
        ├── test_format_url.py
        ├── test_modify_file_name.py
        ├── test_rename_columns.py
        └── test_rename_columns_name.py
```

--------

## Prerequisites

* The Astro CLI installed. You can find installation instructions in this link [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli?tab=linux#install-the-astro-cli)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) 
* Google Cloud account
* Make utility*
* Airflow DuckDB connection (See **Creating a connection to DuckDB** section bellow)

*Optional

## Running this project

First things first, we need to create a Google Cloud Account with a BigQuery Admin Role:

You can find a tutorial at directory docs/google_cloud.md or [click here](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/blob/master/docs/google_cloud.md) 

After finishing the tutorial is time to start the project, you can use one of the following commands on Terminal:

1. Run the following command on Terminal

```bash
astro dev start
```

2. Use the Makefile command `astro-start` on `Terminal`. So that you know, you might need to install the Makefile utility on your machine.

```bash
astro-start
```

Now you can visit the Airflow Webserver at http://localhost:8080 and trigger the ETL workflow or run the Astro command `astro dev ps` to see running containers 

```bash
astro dev ps
```

Output

![image](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Polars-Dataprep-and-Airflow/assets/94936606/f6127f6f-bae9-4604-927a-a0f4fa8a8d8c)

Before triggering the Dag you must create the following connections in the ```Admin``` tab.

## Creating a new connection to DuckDB

![image](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/faffc419-cad4-460d-aec5-b070f17fc7b7)


## Creating a new connection to Google Cloud

![image](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/5a811d8e-283c-4e55-ad79-a1a63dacb1b9)


Next, execute the ```etl_chicago_cafe_permits``` dag

![image](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/3e7c7063-8eb6-4362-9750-f22474fcaa36)
