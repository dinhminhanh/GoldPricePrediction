from spark_app import SparkApp
from pyspark.sql import functions as F
from pyspark.sql import types as T

#############################
KAFKA_URL = "localhost:9092"
POSTGRES_URL = "jdbc:postgresql://localhost:5432/gold_predict"
#############################

def process_data(df):
    """
    Process the DataFrame by performing necessary transformations.
    """
    gold_schema = T.StructType() \
        .add("percentChange", T.StringType()) \
        .add("datetime", T.StringType()) \
        .add("price", T.StringType()) \
        .add("change", T.StringType())
    gold_data = df.filter(F.col("topic") == "gold-data") \
        .select(F.from_json(F.col("value").cast("string"), gold_schema).alias("data")) \
        .select("data.*") \
        .drop("percentChange") \
        .withColumn(
            "datetime",
            F.to_timestamp("datetime", "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'")
        ) \
        .withColumn(
            "price",
            F.regexp_replace("price", ",", "").cast(T.DoubleType())
        ) \
        .withColumn(
            "change",
            F.regexp_replace("change", r"[+]", "").cast(T.DoubleType())
        )

    oil_schema = gold_schema
    oil_data = df.filter(F.col("topic") == "oil-data") \
        .select(F.from_json(F.col("value").cast("string"), oil_schema).alias("data")) \
        .select("data.*") \
        .drop("percentChange") \
        .withColumn(
            "datetime",
            F.to_timestamp("datetime", "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'")
        ) \
        .withColumn(
            "price",
            F.regexp_replace("price", ",", "").cast(T.DoubleType())
        ) \
        .withColumn(
            "change",
            F.regexp_replace("change", r"[+]", "").cast(T.DoubleType())
        )
    
    dxy_schema = gold_schema
    dxy_data = df.filter(F.col("topic") == "dxy-data") \
        .select(F.from_json(F.col("value").cast("string"), dxy_schema).alias("data")) \
        .select("data.*") \
        .drop("percentChange") \
        .withColumn(
            "datetime",
            F.to_timestamp("datetime", "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'")
        ) \
        .withColumn(
            "price",
            F.regexp_replace("price", ",", "").cast(T.DoubleType())
        ) \
        .withColumn(
            "change",
            F.regexp_replace("change", r"[+]", "").cast(T.DoubleType())
        )
    
    # spx_schema = T.StructType() \
    #     .add("date", T.StringType()) \
    #     .add("last", T.StringType()) \
    #     .add("open", T.StringType()) \
    #     .add("high", T.StringType()) \
    #     .add("low", T.StringType()) \
    #     .add("volume", T.StringType()) \
    #     .add("percent", T.StringType()) 
    # spx_data = df.filter(F.col("topic") == "spx-data") \
    #     .select(F.from_json(F.col("value").cast("string"), spx_schema).alias("data")) \
    #     .select("data.*") \
    #     .withColumn(
    #         "percent",
    #         (F.regexp_replace("percent", r"[()%+]", "").cast("double"))
    #     ) \
    #     .withColumn(
    #         "date",
    #         F.to_date("date", "yyyy-MM-dd")
    #     ) \
    #     .withColumn(
    #         "last",
    #         F.regexp_replace("last", ",", "").cast(T.DoubleType())
    #     ) \
    #     .withColumn(
    #         "open",
    #         F.regexp_replace("open", ",", "").cast(T.DoubleType())
    #     ) \
    #     .withColumn(
    #         "high",
    #         F.regexp_replace("high", ",", "").cast(T.DoubleType())
    #     ) \
    #     .withColumn(
    #         "low",
    #         F.regexp_replace("low", ",", "").cast(T.DoubleType())
    #     ) \
    #     .withColumn(
    #         "volume",
    #         F.regexp_replace("volume", ",", "").cast(T.LongType())
    #     )

    return gold_data, oil_data, dxy_data  # , spx_data

if __name__ == "__main__":
    spark = SparkApp(KAFKA_URL, POSTGRES_URL)

    df = spark.read_message(topics=["gold-data", "oil-data", "dxy-data"], options=None)

    gold_data, oil_data, dxy_data = process_data(df)

    spark.write_to_postgres(table="gold_data", df=gold_data, mode="append")
    spark.write_to_postgres(table="oil_data", df=oil_data, mode="append")
    spark.write_to_postgres(table="dxy_data", df=dxy_data, mode="append")