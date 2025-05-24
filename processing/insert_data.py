from spark_app import SparkApp
from pyspark.sql import functions as F
import os
import glob
import shutil
from dotenv import load_dotenv

load_dotenv()

#############################
KAFKA_URL = os.getenv("KAFKA_URL")
POSTGRES_URL = os.getenv("POSTGRES_URL")
#############################

if __name__ == "__main__":
  spark = SparkApp(kafka_url=KAFKA_URL, postgres_url=POSTGRES_URL)
  
  dxy_path = os.path.join(os.path.dirname(__file__), "..", "data", "dxy_cleaned.csv")
  sp500_path = os.path.join(os.path.dirname(__file__), "..", "data", "sp500_cleaned.csv")
  gold_path = os.path.join(os.path.dirname(__file__), "..", "data", "gold_cleaned.csv")
  oil_path = os.path.join(os.path.dirname(__file__), "..", "data", "oil_cleaned.csv")
  
  options = {
    "header": "true",
    "inferSchema": "true",                
  }
  
  # Insert dxy
  df = spark.read_csv(path=dxy_path, options=options)   
  df = df.withColumn(
    "date",
    F.to_timestamp(F.col("date"), "yyyy.MM.dd HH:mm")
  )
  spark.insert_to_postgres(
    table="dxy_data",
    df=df
  )
  # Insert sp500
  df = spark.read_csv(path=sp500_path, options=options)
  df = df.withColumn(
    "date",
    F.to_timestamp(F.col("date"), "yyyy.MM.dd HH:mm")
  )
  spark.insert_to_postgres(
    table="sp500_data",
    df=df
  )
  # Insert gold
  df = spark.read_csv(path=gold_path, options=options)
  df = df.withColumn(
    "date",
    F.to_timestamp(F.col("date"), "yyyy.MM.dd HH:mm")
  )
  spark.insert_to_postgres(
    table="gold_data",
    df=df
  )
  # Insert oil
  df = spark.read_csv(path=oil_path, options=options)
  df = df.withColumn(
    "date",
    F.to_timestamp(F.col("date"), "yyyy.MM.dd HH:mm")
  )
  spark.insert_to_postgres(
    table="oil_data",
    df=df
  )  
  
  spark.stop()