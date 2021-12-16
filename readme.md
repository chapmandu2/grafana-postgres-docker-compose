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
3.  Ensure that a file named `pyspark-variables.env` is present and correctly filled in with Azure Storage account details.  Use `pyspark-variables.env.example` as a template
4.  Type `make up` to start the services
5.  In another terminal window, type `make get-data` to pull data from the delta lake table on the storage account, and load the data into the postgres db as a table of the same name.  Running the command again will overwrite the data in postgres.
6.  Type `make help` for additional commands
7.  To launch grafana go to `localhost:3001` and log in with admin/admin
8.  Create dashboards based on data in postgres
9.  Export dashboards as json and save to `grafana-dashboards` to persist and share between computers.

# Other tips

Look at the Makefile to see what the make commands are doing

-  Type `docker ps` to see the available docker containers
-  Type `docker exec -it pyspark_container bash` to get into the pyspark container.
-  Type `/opt/spark/bin/pyspark` to start a pyspark session
-  At this point can run the code in `write_df.py` to create a pyspark data frame (either from test data or by reading from a delta lake) and then write it to the postgres database.

# To do

- How to configure multiple tables/visualisations
- Automate data refresh - ie get data from delta lake, write to postgres
    - Overwrite everything to start with
    - Append most recent data later



