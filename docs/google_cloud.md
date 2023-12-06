# Set up a Google Cloud Account with a BigQuery admin role

1) Click on ```Select a project```
   
![image](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/c34fd52a-6c4f-4171-a9fe-9c495c54f9d8)

2) Click on ```New Project```
   
![image](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/cd0e2415-9963-4029-975c-0ebdcaa4da46)

3) Give a name and click on ```CREATE```

![image](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/f107a3f6-1778-4585-8def-abaef2a30116)

4) Click on ```Select a project``` again and select your newly created project

![image](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/76b7e6e8-961c-494a-8c72-b42fa5db4a18)

5) Select or search for IAM service. Then, select ```Service Accounts```

![image](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/c099c7c6-6553-4aa3-8262-f1c17638ccc5)

6) Click on ```CREATE SERVICE ACCOUNT```

![image](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/335eeb75-6efd-4cbd-b122-019e8230a50f)

7) Give a name for your ```Service account name``` and click on ```CREATE AND CONTINUE```

![image](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/faa1aa90-d57a-4f01-864d-2ae5effb216f)

8) Create an Admin role for BigQuery, so you can access it on Airflow

![image](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/2ea831e2-0e4c-47bc-8d1d-a8a1d86ac484)

9) Then click on ```CONTINUE```

![image](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/2dd6f741-0885-48b3-813c-770143d7b11c)

10) Click on ```DONE```. Now you can go back to Airflow and use BigQuery Operator to create a data warehouse in BigQuery.

![image](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/0c6daa7b-cd6d-4651-9e15-d69bd458af46)

11) Now select your service account

![image](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/a240c209-f058-4c34-b763-7e550d185693)

12) Click on ```KEYS``` tab, click on ```ADD KEY```, then ```Create new key```

![image](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/8fc523b4-b081-4160-9252-1570f9ea34f4)

13) Finally, select ```Json``` key type and click on ```CREATE```

![image](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/62ccd496-4385-4c8c-9212-93f4806e4a27)

14) Copy the downloaded JSON file to ```include/gcp``` directory in Airflow project and rename it to ```service_account.json```

15) Then, go to airflow webserver at ```http://localhost:8080/```, admin tab, connections option, and add a google cloud connection

![image](https://github.com/mathewsrc/Streamlined-ETL-Process-Unleashing-Airflow-Soda-Polars-and-YData-Profiling/assets/94936606/14fbba79-2018-49ed-a201-1f78a0be30a8)

