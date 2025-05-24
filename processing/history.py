from spark_app import SparkApp
from pyspark.sql.window import Window
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.regression import LinearRegression
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml import PipelineModel
from pyspark.sql import functions as F
from pyspark.sql import types as T
from dotenv import load_dotenv
import os
import glob
import shutil

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

def train_model(df):
    window_spec = Window.orderBy("datetime").partitionBy("datetime")
    data = df.withColumn("prev_close", F.lag("close", 1).over(window_spec)) \
             .withColumn("prev_open", F.lag("open", 1).over(window_spec)) \
             .withColumn("prev_high", F.lag("high", 1).over(window_spec)) \
             .withColumn("prev_low", F.lag("low", 1).over(window_spec)) \
             .withColumn("prev_volume", F.lag("volume", 1).over(window_spec)) \
             .na.drop()
    
    data = data.withColumnRenamed("close", "label")  
    
    assembler = VectorAssembler(
        inputCols=["prev_close", "prev_open", "prev_high", "prev_low", "prev_volume"],
        outputCol="features"
    )
    scaler = StandardScaler(inputCol="features", outputCol="scaledFeatures")
    lr = LinearRegression(featuresCol="scaledFeatures", labelCol="label")

    pipeline = Pipeline(stages=[assembler, scaler, lr])
    
    train_data, test_data = data.randomSplit([0.8, 0.2], seed=42)
    
    pipeline_model = pipeline.fit(train_data)
    
    predictions = pipeline_model.transform(test_data)
    predictions.select("label", "prediction").show(10)
    
    evaluator = RegressionEvaluator(labelCol="label", predictionCol="prediction", metricName="rmse")
    rmse = evaluator.evaluate(predictions)
    print("RMSE:", rmse)
    
    model_path = os.path.join(os.path.dirname(__file__), "..", "models", "gold_price_pipeline")
    if os.path.exists(model_path):
        shutil.rmtree(model_path)
    pipeline_model.write().overwrite().save(model_path)

if __name__ == "__main__":        
  spark_app = SparkApp(KAFKA_URL, POSTGRES_URL)
  csv_dir = os.path.join(os.path.dirname(__file__), "..", "data", "*.csv")
  csv_files = glob.glob(csv_dir)
  
  df = spark_app.read_csv(csv_files)   
    
  processed_df = process_data(df)
    
  spark_app.insert_to_postgres(df=processed_df, table="history_data")
  # train_model(processed_df)