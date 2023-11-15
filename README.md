[![GitHub Actions - CI](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Polars-Dataprep-and-Airflow/actions/workflows/main.yml/badge.svg)](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Polars-Dataprep-and-Airflow/actions/workflows/main.yml)

# Streamlined ETL Process: Unleashing  Airflow, Polars, SODA, and YData Profiling


## Project Summary:

This ETL (Extract, Transform, Load) project employs several Python libraries, including Polars, Airflow, Soda, YData Profiling, Requests, BeautifulSoup, and Loguru, to streamline the extraction, transformation, and loading of CSV datasets from the [U.S. government's data repository](https://catalog.data.gov) and the [Chicago Sidewalk Cafe Permits] (https://catalog.data.gov/dataset/sidewalk-cafe-permits). The notebook in the notebooks directory is used to extract, transform, and load datasets from the U.S. government's data repository and the Airflow workflow to extract, transform, and load the Chicago Sidewalk Cafe Permits dataset.

## Architecture Overview (warning: the architecture can change in the future)

![etl_airflow_soda_bigquery_looker](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/b4635702-c5cc-45b6-91cf-a3b69ef09419)


## Architecture of Continuous Integration with GitHub Actions


![etl_ci drawio](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/04b81049-e0f8-4336-a059-bea6640402ce)


### Workflow with Airflow (warning: the workflow can change in the future)

### Part 1

![image](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/ab7f4353-f30b-4f8a-aaf2-4b47c040ae23)
1. I created a concurrency of 1 using the BashOperator to avoid two or more executions against DuckDB as allowing  two or more calls to DuckDB would cause an error
2. I loaded the CSV file using an HTTP call by leveraging the Astro Python SDK `load_file()` function and the DuckDB connection that I created in Airflow `Admin/Connections`
3. Then, I create a task to check raw data quality using [Soda](https://docs.soda.io/)
   3.1 Check the number of rows

   <img src="https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/7861bcba-09d4-4f3b-b00f-5a86e6288f40" width=40%><br/>

   3.2 Confirm that the required columns are present 

   <img src="https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/d9a907be-c061-4341-85cd-1b202221bf73" width=70%><br/>

   3.3 Check columns data type

   <img src="https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/70904470-35c5-487a-be84-9fa431524d00" width=40%><br/>

4. Next, I created tasks to count the number of rows and to create a data profiling 
5. Finally, I create a transform task to apply the following transformations: lower column name, remove duplicated rows, remove missing values, and drop a row if all values are null


### Part 2

![image](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/8b325417-bdc9-4adb-8a22-cf2a04d7171e)

1. After the transformation of data I used Soda to check data quality to ensure that data was transformed as expected
   1.1 Check the number of rows

   <img src="https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/c51ba209-2f06-4a05-8a76-e5b74a89b4fd" width=40%><br/>

   1.2 Check validation 

   <img src="https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/2f296667-20bc-4404-b015-3079739b3920" width=60%><br/>

   1.3 Check duplicate data

   <img src="https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/1cf19ff3-e19c-441a-ac9d-1ee1b6b1cec6" width=40%><br/>

   1.4 Check missing values

  <img src="https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/fca39a17-a96c-4f5c-863b-d76ddbdeb3a1" width=60%><br/>

   1.5 Confirm that the required columns are present

   <img src="https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/dcb5612b-788a-4f7b-82ed-280c129a0846" width=70%><br/>

   1.6 Check columns data type

   <img src="https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/25341326-5f66-4b46-94c9-568204c1c690" width=40%><br/>

2. Next, I created tasks to count the number of rows and to create a data profiling 
3. Finally, I created a task to create a data profiling comparing the raw data with the transformed data

Part 3 - TODO

## Project Objectives:

**Extraction**: I utilize the requests library and BeautifulSoup to scrape datasets from https://catalog.data.gov and the Chicago Sidewalk Cafe Permits dataset.

**Transformation**: Data manipulation and cleaning are accomplished using Polars, a high-performance data manipulation library written in Rust.

**Data Profiling**: YData Profiling is employed to create dynamic data reports and facilitate data profiling, quality assessment, and visualization, providing insights into data quality and characteristics.

**Loading**: Transformed data is saved in CSV files using Polars.

**Logging**: Loguru is chosen for logging, ensuring transparency, and facilitating debugging throughout the ETL process.

**Data quality**: Soda is employed to ensure data quality.

**Tests**: Pytest is employed for code validation.

**Linting**: Ruff is employed to ensure code quality.

**Formatting**: Ruff is again employed to ensure code quality.

**Orchestration**: Airflow is employed to orchestrate the whole ETL process.

**Continuos Integration**: GitHub Actions is used for continuous integration to push code to GitHub. 

By automating these ETL tasks, I establish a robust data pipeline that transforms raw data into valuable assets, supporting informed decision-making and data-driven insights.

## Project Organization
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
* Make utility*
* Airflow DuckDB connection (See **Creating a connection to DuckDB** section bellow)

*Optional

## Exploring datasets 

You can explore some datasets by using this notebook: [gov_etl.ipynb](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Polars-Dataprep-and-Airflow/blob/master/notebooks/gov_etl.ipynb)

Below you can see some images of it:

Fetching datasets<br/>

<img src="https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Polars-Dataprep-and-Airflow/assets/94936606/f633d13d-8835-4187-95e8-59db9c6794b7" width=80%><br/>


Extracting, transforming, and loading a dataset<br/>

<img src="https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Polars-Dataprep-and-Airflow/assets/94936606/f4d6ddb4-a6a6-494b-a715-f0459b6e2878" width=80%><br/>

## Running this project

First things first, we need to start astro project. you have two options:

1. Run the following command on Terminal

```bash
astro dev start
```

2. Use the Makefile command `astro-start` on `Terminal`. Just so you know, you might need to install the Makefile utility on your machine.

```bash
astro-start
```

Now you can visit the Airflow Webserver at http://localhost:8080 and trigger the ETL workflow or run the Astro command `astro dev ps` to see running containers 

```bash
astro dev ps
```

Output

![image](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Polars-Dataprep-and-Airflow/assets/94936606/f6127f6f-bae9-4604-927a-a0f4fa8a8d8c)


## Creating a new connection to DuckDB

## TODO

Next, unpause by clicking on the toggle button next to the DAG name

## TODO !insert image here


Finally, click on the play button to trigger the workflow

## TODO !insert image here


If everything goes well you will see a result like this one below

## TODO !insert image here


## GitHub Action workflow (Continuos Integration)

![image](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/4a13a7bd-080f-49a1-aaaa-db353180385f)


### TODO
- [ ] Add column description to reports - [column-descriptions](https://docs.profiling.ydata.ai/4.6/features/metadata/#column-descriptions)
- [ ] Try data modeling with DBT
- [ ] Try to upload data to BigQuery and create a dashboard with Looker
- [ ] Record how to create a DuckDB connection in airflow
- [ ] Record workflow running
- [ ] Create the architecture image of the project
- [ ] Change the order of GitHub Actions to lint, format, test
- [ ] Review README (add ETL section for notebook and airflow)
- [ ] Completed!
