Streamlined ETL Process: Unleashing Polars, Dataprep and Airflow
==============================

Project Summary:

This ETL (Extract, Transform, Load) project employs several Python libraries, including Polars, Airflow, Dataprep, Requests, BeautifulSoup, and Loguru, to streamline the extraction, transformation, and loading of CSV datasets from the U.S. government's data repository at https://catalog.data.gov.

Project Objectives:

Extraction: I utilize the requests library and BeautifulSoup to scrape datasets from https://catalog.data.gov, a repository of various data formats, including CSV, XLS, and HTML.

Transformation: Data manipulation and cleaning are accomplished using Polars, a high-performance data manipulation library written in Rust.

Data Profiling: YData Profiling is employed to create dynamic data reports and facilitate data profiling, quality assessment, and visualization, providing insights into data quality and characteristics.

Loading: Transformed data is saved in CSV files using Polars.

Logging: Loguru is chosen for logging, ensuring transparency, and facilitating debugging throughout the ETL process.

Orchestration: Airflow is employed to orchestrate the whole ETL process.

Through the automation of these ETL tasks, I establish a robust data pipeline that transforms raw data into valuable assets, supporting informed decision-making and data-driven insights.


Project Organization
------------

```
Streamlined-ETL-Process-Unleashing-Polars-Dataprep-and-Airflow/
├── .devcontainer                        # VS Code development container 
|   └── devcontainer.json                
├── .github                              # GitHub Actions for continuous integration (CI) 
|   └── workflows
|       └── main.yml                     # GitHub Actions configurations 
├── dags
|   └── utils
|        ├── drop_duplicates.py          # Method to remove duplicates
|        ├── drop_full_null_columns.py   # Method to drop columns if all values are null
|        ├── drop_full_null_rows.py      # Method to drop rows if all values in a row are null
|        ├── drop_missing.py             # Method to drop rows with missing values in specific columns
|        ├── format_url.py               # Method to format the url
|        ├── get_time_period.py          # Method to get currently time period
|        ├── modify_file_name.py         # Method to create a formatted file name
|        └── rename_columns.py           # Method to rename DataFrame columns name
├── include
|   ├── data                             # Directory to save CSV files
|   ├── reports                          # Directory with reports
|   └── soda                             # Directory with SODA files
|        ├── checks                      # Directory containing data quality rules yml files
|        |    └── transformation.yml     # Data quality rules for transformation step
|        ├── check_function.py           # Helpful function for run SODA data quality checks 
|        └── configuration.yml           # Configurations to connect Soda to a data source (DuckDB)
├── README.md                               
├── notebooks                            # COLAB notebooks
├── plugins
├── tests                                # Diretory for Python test files
├── .dockerignore
├── .gitignore
├── airflow_setttings.yaml
├── format.sh                            # Bash script to format code with ruff  
├── LICENSE   
├── lint.sh                              # Bash script to lint code with ruff
├── Makefile                             # Makefile with some helpfull commands  
├── packages.txt
├── README.md 
├── requirements.txt                     # Required Python libraries 
├── setup_data_folders.sh                # Bash script to create some directories
├── source_env_linux.sh                  # Bash script to create an Python virtual enviroment in linux
├── source_env_windows.sh                # Bash script to create an Python virtual enviroment in windows
└── test.sh                              # Bash script to test code with pytest 
```


--------

## Prerequisites

* The Astro CLI installed. You can find installation instructions in this link [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli?tab=linux#install-the-astro-cli)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) 
* Make utility*
* Airflow DuckDB connection (See **Creating a connection to DuckDB** section bellow)

*Optional

## Exploring datasets 

You can can explore some datasets by using this notebook: [gov_etl.ipynb](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Polars-Dataprep-and-Airflow/blob/master/notebooks/gov_etl.ipynb)

Bellow you can see some images of it:

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

2. Use the Makefile command `astro-start` on `Terminal`. Notice that you maybe need to install Makefile utility on your machine.

```bash
astro-start
```

Now you can visit the Airflow Webserver at: http://localhost:8080 and trigger the ETL workflow or run the Astro command `astro dev ps` to see running containers 

```bash
astro dev ps
```

Output

![image](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Polars-Dataprep-and-Airflow/assets/94936606/f6127f6f-bae9-4604-927a-a0f4fa8a8d8c)


## Creating a new connection to DuckDB

## TODO

Next, unpause by clicking in the toggle button next to the dag name

## TODO !insert image here


Finally, click on the play button to trigger the workflow

## TODO !insert image here


If everything goes well you will see a result like this one bellow

## TODO !insert image here


### TODO
- [ ] Add column description to reports - [column-descriptions](https://docs.profiling.ydata.ai/4.6/features/metadata/#column-descriptions)
- [ ] Try data modeling with DBT
- [ ] Try to upload data to BigQuery and create a dashboard with Looker
- [ ] Record how to create a DuckDB connection in airflow
- [ ] Record workflow running
- [ ] Create the architecture image of the project
- [ ] Completed!


