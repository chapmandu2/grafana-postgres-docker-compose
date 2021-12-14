# About

Aim of this repo is to provide a mechanism to monitor the output of spark data pipelines with Grafana in a context where it is difficult to host the necessary components of Grafana - ie there is no Kubernetes, options for VMs, suitable databses etc available.

Instead this problem is solved as follows:

- Use docker compose locally to run Grafana and source data from a local postgres db
- Use Data Mechanics Spark Docker image to retrieve data from remote Azure Blob storage in delta format, and write to the local postgres database.

This setup can be easily run locally by cloning the code repo, and typing some make commands

The above is currently in progress, instructions below and how to currently run the code.

# Instructions

1.  Clone the repo
2.  Make sure that docker is installed.
3.  Type `docker compose up` to start the services
4.  Type `docker ps` to see the available docker containers
5.  Type `docker exec -it pyspark_container bash` to get into the pyspark container.
6.  Type `/opt/spark/bin/pyspark` to start a pyspark session
7.  At this point can run the code in `write_df.py` to create a pyspark data frame (either from test data or by reading from a delta lake) and then write it to the postgres database.
8.  To launch grafana go to `localhost:3001` and log in with admin/admin
9.  Create dashboards based on data in postgres

# To do

- Parameterise config for access to delta lake etc
- Add makefile to provide a wrapper over standard commands
- Automate data refresh - ie get data from delta lake, write to postgres
    - Overwrite everything to start with
    - Append most recent data later
- How to automatically populate dashboards etc with standard viz?

