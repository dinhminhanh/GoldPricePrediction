from spark_app import SparkApp
from pyspark.sql import functions as F
from pyspark.sql import types as T
from dotenv import load_dotenv
import os
import glob

load_dotenv()

#############################
KAFKA_URL = os.getenv("KAFKA_URL")
POSTGRES_URL = os.getenv("POSTGRES_URL")
#############################

def process_data(df):
  process_df = df.withColumn("datetime", F.to_timestamp(F.col("Date"), "yyyy.MM.dd HH:mm")) \
    .drop(F.col("Date")) \
    .withColumnRenamed("Open", "open") \
    .withColumnRenamed("High", "high") \
    .withColumnRenamed("Low", "low") \
    .withColumnRenamed("Close", "close") \
    .withColumnRenamed("Volume", "volume")
    
  return process_df

if __name__ == "__main__":        
  spark_app = SparkApp(KAFKA_URL, POSTGRES_URL)
  csv_dir = os.path.join(os.path.dirname(__file__), "..", "data", "*.csv")
  csv_files = glob.glob(csv_dir)
  
  df = spark_app.read_csv(csv_files)   
    
  processed_df = process_data(df)
    
  spark_app.insert_to_postgres(df=processed_df, table="history_data")