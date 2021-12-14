from datamechanics/spark:3.1.1-dm15

ENV PYSPARK_MAJOR_PYTHON_VERSION=3

WORKDIR /opt/application

RUN wget https://jdbc.postgresql.org/download/postgresql-42.3.1.jar
RUN mv postgresql-42.3.1.jar /opt/spark/jars

COPY main.py .

# make sure that the pyspark container doesn't go down so we can docker exec to it
CMD sleep 10000