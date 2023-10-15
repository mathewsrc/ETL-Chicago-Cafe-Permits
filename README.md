Streamlined ETL Process: Unleashing Polars, Dataprep and Airflow
==============================

Project Summary:

This ETL (Extract, Transform, Load) project employs several Python libraries, including Polars, Airflow, Dataprep, Requests, BeautifulSoup, and Loguru, to streamline the extraction, transformation, and loading of CSV datasets from the U.S. government's data repository at https://catalog.data.gov.

Project Objectives:

Extraction: I utilize the requests library and BeautifulSoup to scrape datasets from https://catalog.data.gov, a repository of various data formats, including CSV, XLS, and HTML.

Transformation: Data manipulation and cleaning are accomplished using Polars, a high-performance data manipulation library written in Rust.

Data Profiling: Dataprep is employed to create dynamic data reports and facilitate data profiling, quality assessment, and visualization, providing insights into data quality and characteristics.

Loading: Transformed data is saved in CSV files using Polars.

Logging: Loguru is chosen for logging, ensuring transparency, and facilitating debugging throughout the ETL process.

Orchestration: Airflow is employed to orchestrate the whole ETL process.

Through the automation of these ETL tasks, I establish a robust data pipeline that transforms raw data into valuable assets, supporting informed decision-making and data-driven insights.


Project Organization
------------

```
Streamlined-ETL-Process-Unleashing-Polars-Dataprep-and-Airflow/
├── .devcontainer # Tells VS Code how to access (or create) a development container with a well-defined tool and runtime stack
|   └── devcontainer.json
├── .github # GitHub Actions for continuous integration and deployment 
|   └── workflows
|       └── main.yml
├── LICENSE     
├── README.md                  
├── Makefile                     # Makefile with commands                    
├── configs                      # Config files 
│   └── configs.yaml              
│
├── data                         
│   ├── external                 # Data from third-party sources.
│   ├── interim                  # Intermediate data that has been transformed.
│   ├── processed                # The final, canonical data sets for modeling.
│   └── raw                      # The original, immutable data dump.
│
├── docs                         # Project documentation.
│
├── notebooks                    # Jupyter notebooks.
│
├── reports                      # Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures                  # Generated graphics and figures to be used in reporting.
│
├── requirements.txt             # The requirements file for reproducing the analysis environment.
└── src                          # Source code for use in this project.
    ├── __init__.py              # Makes src a Python module.
    │
    ├── cli       # Scripts to create a CLI tool.
    |   ├── app.py     
    |   ├── requirements.txt
    |   └── Dockerfile 
    |
    └──   webapp        # Scripts to create a FastAPI microservice.
        ├── webapp.py
        ├── requirements.txt    
        └── Dockerfile
      
```


--------


Notebook

Fetching datasets<br/>

<img src="https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Polars-Dataprep-and-Airflow/assets/94936606/f633d13d-8835-4187-95e8-59db9c6794b7" width=80%><br/>


Extracting, transforming, and loading a dataset<br/>

<img src="https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Polars-Dataprep-and-Airflow/assets/94936606/f4d6ddb4-a6a6-494b-a715-f0459b6e2878" width=80%><br/>


