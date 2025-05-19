from spark_app import SparkApp

#############################
KAFKA_URL = "localhost:9092"
POSTGRES_URL = "jdbc:postgresql://localhost:5432/your_database"
#############################

if __name__ == "__main__":
    spark_app = SparkApp(KAFKA_URL, POSTGRES_URL)