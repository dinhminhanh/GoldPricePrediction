from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.sql import DataFrame
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# List of packages to be used in the Spark session
scala_version = '2.12'
spark_version = '3.5.5'

packages = [
  f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
  'org.apache.kafka:kafka-clients:3.9.0',    
]

class SparkApp():
    def __init__(self, kafka_url: str, postgres_url: str):
        """
        kafka_url: Kafka bootstrap server URL
        postgres_url: PostgreSQL connection URL
        e.g: "jdbc:postgresql://localhost:5432/your_database"
        """
        self.spark = (
            SparkSession.builder
            .appName("Spark Application")
            .config("spark.jars.packages", ",".join(packages))  
            .config("spark.jars", "./jars/postgresql-42.6.0.jar")
            .getOrCreate()
        )
        self.kafka_url = kafka_url
        self.postgres_url = postgres_url

    def read_message(self, topics: list[str], options) -> DataFrame:
        """
        Reads data from Kafka topic.
        options is a dictionary of options for the Kafka source.
        e.g. { 
            "startingOffsets": "earliest"
        }
        """

        if options is None:
            options = {
                "startingOffsets": "earliest",
            }
        try:
            df = (
                self.spark.readStream
                .format("kafka")
                .option("kafka.bootstrap.servers", self.kafka_url)
                .option("subscribe", ",".join(topics))
                .options(**options)
                .load()
            )
        except Exception as e:
            logging.error(f"Error reading from Kafka: {e}")
            raise
        
        return df
    
    def write_to_console(self, df: DataFrame, options=None) -> None:
        """
        Writes the DataFrame to the console.
        """
        if options is None:
            options = {}

        try:
            query = (
                df.writeStream
                .outputMode("append")
                .format("console")
                .options(**options)
                .start()
            )
            query.awaitTermination()
        except Exception as e:
            logging.error(f"Error writing to console: {e}")
            raise

    def process(self, df: DataFrame) -> DataFrame:
        """
        Processes the DataFrame, overwrite this function to process data.
        """
        pass

    def write_to_postgres(self, table, uname, passwd, df: DataFrame) -> None:
        """
        Writes the DataFrame to a some sources.
        table: Name of the table in PostgreSQL
        uname: PostgreSQL username
        passwd: PostgreSQL password
        df: DataFrame to be written
        """
        def write_to_postgres(batch_df):
            batch_df.write \
                .format("jdbc") \
                .option("url", self.postgres_url) \
                .option("dbtable", table) \
                .option("user", uname) \
                .option("password", passwd) \
                .option("driver", "org.postgresql.Driver") \
                .mode("append") \
                .save()

        try:
            query = df.writeStream \
                .foreachBatch(write_to_postgres) \
                .outputMode("append") \
                .start()

            query.awaitTermination()
        except Exception as e:
            logging.error(f"Error writing to PostgreSQL: {e}")
            raise

if __name__ == "__main__":
    pass