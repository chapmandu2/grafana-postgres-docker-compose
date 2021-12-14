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

delta_df_url = f"wasbs://{os.environ['DELTA_CONTAINER_NAME']}@{os.environ['DELTA_ACCOUNT_NAME']}.blob.core.windows.net/{os.environ['DELTA_TABLE_PATH']}"
delta_df = spark.read.format("delta").load(delta_df_url)
delta_write_df = delta_df.limit(100).cache()
delta_write_df.show()

# write dataframe to postgres
delta_write_df.write \
    .format("jdbc") \
    .option("mode", "overwrite") \
    .option("url", "jdbc:postgresql://postgres:5432/analytics") \
    .option("dbtable", "test_delta") \
    .option("user", "analytics") \
    .option("password", "analytics") \
    .option("driver", "org.postgresql.Driver") \
    .save()