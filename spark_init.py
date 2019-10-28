##

# Argument Mining with Tone Analysis 6.0
# 'spark_init'
# Gide Inc 2019

##

# Initializing Spark Session
from pyspark.sql import SparkSession, SQLContext
import random

spark = SparkSession.builder.appName('Argument Mining 6.0')\
    .master("local[2]")\
    .config('spark.ui.port', random.randrange(4000, 5000)).getOrCreate()


