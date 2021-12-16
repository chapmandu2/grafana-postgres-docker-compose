from pyspark.sql import SparkSession
import os, datetime

# set up spark session
spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.jars", "/opt/spark/jars/postgresql-42.3.1.jar") \
    .getOrCreate()

#configure delta storage account details
storage_account_name = f"fs.azure.account.key.{os.environ['DELTA_ACCOUNT_NAME']}.blob.core.windows.net"
storage_account_access_key = os.environ['DELTA_ACCESS_KEY']
spark.conf.set(storage_account_name, storage_account_access_key)

delta_table_paths = os.environ['DELTA_TABLE_PATHS'].split(',')

def get_data(tbl):

    # make sure table length is sensible
    if len(tbl) == 0:
        return
    
    delta_df_url = f"wasbs://{os.environ['DELTA_CONTAINER_NAME']}@{os.environ['DELTA_ACCOUNT_NAME']}.blob.core.windows.net/{tbl}"
    print(f"Getting data from {delta_df_url}")
    delta_df = spark.read.format("delta").load(delta_df_url)

    # write dataframe to postgres
    delta_df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/analytics") \
        .option("dbtable", tbl) \
        .option("user", "analytics") \
        .option("password", "analytics") \
        .option("driver", "org.postgresql.Driver") \
        .mode('overwrite') \
        .save()
    
    print(f"Data written to {tbl} table in postgres")

    

for t in delta_table_paths:
    get_data(t)
    