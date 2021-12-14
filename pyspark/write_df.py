# this code can write a data frame to the postgres db, needs to be run manually for now

from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.jars", "/opt/spark/jars/postgresql-42.3.1.jar") \
    .getOrCreate()


## create local test dataframe
from pyspark.sql.types import StructType,StructField, StringType, IntegerType
data2 = [("James","","Smith","36636","M",3000),
    ("Michael","Rose","","40288","M",4000),
    ("Robert","","Williams","42114","M",4000),
    ("Maria","Anne","Jones","39192","F",4000),
    ("Jen","Mary","Brown","","F",-1)
  ]

schema = StructType([ \
    StructField("firstname",StringType(),True), \
    StructField("middlename",StringType(),True), \
    StructField("lastname",StringType(),True), \
    StructField("id", StringType(), True), \
    StructField("gender", StringType(), True), \
    StructField("salary", IntegerType(), True) \
  ])
 
df = spark.createDataFrame(data=data2,schema=schema)
df.printSchema()
df.show(truncate=False)


# write dataframe to postgres  (this doesn't work with dockerised postgres)
df.write \
    .format("jdbc") \
    .option("mode", "overwrite") \
    .option("url", "jdbc:postgresql://postgres:5432/analytics") \
    .option("dbtable", "test_table") \
    .option("user", "analytics") \
    .option("password", "analytics") \
    .option("driver", "org.postgresql.Driver") \
    .save()


# read a test data frame (this doesn't work with dockerised postgres)
test_data = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://postgres:5432/analytics") \
    .option("dbtable", "public.test_table") \
    .option("user", "analytics") \
    .option("password", "analytics") \
    .load()


# get data from delta lake (this bit works)
storage_account_name = "fs.azure.account.key.<storage_account_name>.blob.core.windows.net"
storage_account_access_key = 'access_key'
spark.conf.set(storage_account_name, storage_account_access_key)

delta_df = spark.read.format("delta").load('wasbs://<container_name>@<storage_account_name>.blob.core.windows.net/')
delta_write_df = delta_df.limit(100).cache()
delta_write_df.show()

# then write to postgres as above
