import pandas as pd
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lag
from pyspark.sql.window import Window
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.regression import RandomForestRegressor, LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml import Pipeline

DATA_DIR = "data"
OUTPUT_MERGED = os.path.join(DATA_DIR, "merged_gold_data.csv")


def merge_cleaned_files():
    gold_df = pd.read_csv(os.path.join(DATA_DIR, "gold_cleaned.csv"), parse_dates=["Date"])
    oil_df = pd.read_csv(os.path.join(DATA_DIR, "oil_cleaned.csv"), parse_dates=["Date"])
    dxy_df = pd.read_csv(os.path.join(DATA_DIR, "dxy_cleaned.csv"), parse_dates=["Date"])
    sp500_df = pd.read_csv(os.path.join(DATA_DIR, "sp500_cleaned.csv"), parse_dates=["Date"])

    merged_df = gold_df.merge(oil_df, on="Date", how="outer")
    merged_df = merged_df.merge(dxy_df, on="Date", how="outer")
    merged_df = merged_df.merge(sp500_df, on="Date", how="outer")

    merged_df = merged_df.sort_values("Date").drop_duplicates(subset=["Date"]).reset_index(drop=True)
    merged_df = merged_df.ffill()

    merged_df.to_csv(OUTPUT_MERGED, index=False)


def train_model(n_lags=5):
    spark = SparkSession.builder.appName("GoldPricePrediction").getOrCreate()

    df_pd = pd.read_csv(OUTPUT_MERGED)
    df_pd = df_pd.dropna()
    df_pd["Date"] = pd.to_datetime(df_pd["Date"])
    df_pd = df_pd.sort_values("Date")

    df = spark.createDataFrame(df_pd)

    # Chọn feature
    features = [c for c in df.columns if c.startswith("dxy_") or c.startswith("sp500_") or c.startswith("gold_") or c.startswith("oil_")]
    features = [f for f in features if f not in ["gold_last", "gold_change_percent"]]

    window_spec = Window.orderBy("Date")
    for feat in features:
        for i in range(1, n_lags + 1):
            df = df.withColumn(f"{feat}_lag_{i}", lag(col(feat), i).over(window_spec))

    df = df.withColumn("target", lag("gold_last", -1).over(window_spec)).dropna()

    # Remove outliers
    df_pd = df.toPandas()
    for col_name in df_pd.select_dtypes(include="number").columns:
        Q1 = df_pd[col_name].quantile(0.25)
        Q3 = df_pd[col_name].quantile(0.75)
        IQR = Q3 - Q1
        lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
        df_pd = df_pd[(df_pd[col_name] >= lower) & (df_pd[col_name] <= upper)]

    df = spark.createDataFrame(df_pd)
    df = df.orderBy("Date")

    train_df, test_df = df.randomSplit([0.7, 0.3], seed=42)

    drop_cols = ["Date", "gold_last", "gold_change_percent", "target"]
    feature_cols = [c for c in df.columns if c not in drop_cols]

    assembler = VectorAssembler(inputCols=feature_cols, outputCol="features_raw")
    scaler = StandardScaler(inputCol="features_raw", outputCol="features")

    models = {
        "Random Forest": RandomForestRegressor(labelCol="target", featuresCol="features", numTrees=100, seed=42),
        "Linear Regression": LinearRegression(labelCol="target", featuresCol="features")
    }

    results = []
    evaluator = RegressionEvaluator(labelCol="target", predictionCol="prediction")

    best_r2 = float("-inf")
    best_model_name = None
    best_pipeline_model = None

    for name, model in models.items():
        pipeline = Pipeline(stages=[assembler, scaler, model])
        pipeline_model = pipeline.fit(train_df)

        train_pred = pipeline_model.transform(train_df)
        test_pred = pipeline_model.transform(test_df)

        mae = evaluator.setMetricName("mae").evaluate(test_pred)
        mse = evaluator.setMetricName("mse").evaluate(test_pred)
        rmse = evaluator.setMetricName("rmse").evaluate(test_pred)
        r2 = evaluator.setMetricName("r2").evaluate(test_pred)
        r2_train = evaluator.evaluate(train_pred)
        mean_target = test_pred.select("target").rdd.map(lambda x: x[0]).mean()
        accuracy = 1 - (mae / mean_target)

        overfit_status = "Good"
        if r2_train - r2 > 0.1:
            overfit_status = "Overfit"
        elif r2 - r2_train > 0.1:
            overfit_status = "Underfit"

        results.append({
            "Model": name,
            "MAE": mae,
            "MSE": mse,
            "RMSE": rmse,
            "R2 Test": r2,
            "R2 Train": r2_train,
            "Accuracy": accuracy,
            "Fit Status": overfit_status
        })

        if r2 > best_r2:
            best_r2 = r2
            best_model_name = name
            best_pipeline_model = pipeline_model

    df_result = pd.DataFrame(results).sort_values("R2 Test", ascending=False)
    print(df_result)
    df_result.to_csv("model_results.csv", index=False)

    # Save best pipeline model
    model_path = f"models/{best_model_name.replace(' ', '_').lower()}_pipeline"
    best_pipeline_model.write().overwrite().save(model_path)
    print(f"Saved best pipeline model '{best_model_name}' to {model_path}")


if __name__ == "__main__":
    merge_cleaned_files()
    train_model()
