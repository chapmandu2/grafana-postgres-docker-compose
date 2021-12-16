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
3.  Ensure that a file named `pyspark-variables.env` is present and correctly filled in with Azure Storage account details and a comma seperated list of any delta tables you want to use.  Use `pyspark-variables.env.example` as a template
4.  Type `make up` to start the services, Control-C to kill
5.  In another terminal window, type `make get-data` to pull data from the delta lake table on the storage account, and load the data into the postgres db as a table of the same name.  Running the command again will overwrite the data in postgres.
6.  Type `make help` for additional commands
7.  To launch grafana go to `localhost:3001` and log in with admin/admin
8.  Create dashboards based on data in postgres
9.  Export dashboards as json and save to `grafana-dashboards` to persist and share between computers.

Everything can be restarted again with another `make up`.  

# Other tips

Look at the Makefile to see what the make commands are doing

-  Type `docker ps` to see the available docker containers and their names
-  Type `docker exec -it <pyspark_container> bash` to get into the pyspark container.
-  Type `docker exec -it <postgres_container> bash` and then `psql -U analytics` to look at the postgres db
-  Type `/opt/spark/bin/pyspark` to start a pyspark session
-  The `write_df.py` file contains code to create a pyspark data frame without a delta lake being available, and then write it to the postgres database.

# Updating

By default the data in postgres and any dashboards will persist in a Docker volume.  

To start again from scratch type:

`docker rm -f $(docker ps -a -q)` - NOTE: this will delete ALL docker containers so if you are using docker for something else just delete the 3 containers associated with this repo.

Then `docker volume prune` and `docker network prune`.

Then run `docker compose up` again.

To ensure that the Docker images are up to date type `docker compose up --build`

# To do

- Automate data refresh - ie get data from delta lake, write to postgres
    - Overwrite everything to start with
    - Append most recent data later



