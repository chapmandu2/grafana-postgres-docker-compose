help:
	@echo Makefile commands
	@echo
	@echo help: print this help message and exit
	@echo up: start everything
	@echo stop: stop everything
	@echo get-data: get the data from the delta lake

up:
	docker compose up

down:
	docker compose down

get-data:
	docker exec -it grafana-postgres-docker-compose-pyspark-1 /opt/spark/bin/spark-submit /opt/pyscripts/main.py