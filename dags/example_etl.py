"""
### Use the @aql.dataframe decorator without an Airflow connection

This DAG shows how the @aql.dataframe decorator can be leveraged even without
access to a relational database to run transformations on pandas dataframes.
"""


from airflow.decorators import dag
from pendulum import datetime

# Import decorators and classes from the SDK
from astro import sql as aql
import pandas as pd


@dag(
    start_date=datetime(2023, 3, 27),
    schedule=None,
    catchup=False,
    tags=["Astro Python SDK", "Pandas"],
)
def astro_python_sdk_example():
    @aql.dataframe()
    def create_table(contents_col_2):
        my_dict = {"col1": [1, 2, 3], "col2": contents_col_2, "col3": [0, 0, 0]}
        df = pd.DataFrame(my_dict)
        return df

    # with no output table specified the result is stored in the Airflow metastore
    # serialized as astro.dataframes.pandas.PandasDataframe
    my_table = create_table(["hi", "bye", "hello"])

    @aql.dataframe()
    def sum_col_1(in_table):
        my_sum = in_table.col1.sum()
        print(my_sum)
        return int(my_sum)

    sum_col_1(my_table)


astro_python_sdk_example()
