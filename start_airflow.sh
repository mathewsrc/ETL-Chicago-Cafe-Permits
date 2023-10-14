#!/bin/bash  

docker-compose up airflow-init
docker-compose up -d
docker-compose ps
#docker exec -it {ID_WEB_SERVER} airflow users create \
#    --username admin \
#    --firstname Example \
#    --lastname Example \
#    --role Admin \
#    --email
#docker exec -it {ID_WEB_SERVER} airflow users list
