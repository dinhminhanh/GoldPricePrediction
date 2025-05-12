# Gold Price Prediction Project

## Project Overview
This project focuses on analyzing historical gold price data and key influencing factors such as exchange rates and oil prices to build a predictive model for future gold prices.

## Data Collection
The system automatically collects data from various sources:
- **Metals-API** for oil prices.
- **Investing.com** for gold prices in USD.
- Web scraping using **Scrapy** and **Selenium**.

The collected data is then published to **Apache Kafka** for real-time processing.

## Data Processing Pipeline
- **Spark Streaming** consumes data from Kafka.
- Perform data cleaning, normalization, and feature extraction (e.g., gold price fluctuations, time-based factors).
- Transform and store the processed data in **MongoDB** to ensure scalability and flexible querying.

## Machine Learning Models
The project applies the following machine learning techniques to build predictive models:
- **Linear Regression**
- **Decision Tree**
- **Artificial Neural Networks (ANNs)**

Each model is evaluated based on accuracy metrics to determine the optimal model for price forecasting.

## Expected Outcomes
The project aims to provide **real-time gold price forecasts**, offering investors insights into market trends and assisting in making accurate financial decisions.

## Technologies Used
- **Apache Kafka** (Real-time data streaming)
- **Scrapy & Selenium** (Web scraping)
- **Apache Spark Streaming** (Data processing)
- **MongoDB** (Data storage)
- **Machine Learning** (Predictive modeling)

## Installation & Setup
1. Install dependencies:
```bash
pip install pyspark kafka-python scrapy selenium pymongo
```
2. Start Kafka Server:
```bash
bin/zookeeper-server-start.sh config/zookeeper.properties &
bin/kafka-server-start.sh config/server.properties &
```
3. Run Spark Streaming Consumer:
```bash
spark-submit spark_streaming.py
```
4. Train ML models:
```bash
python train_model.py
```

## Docker
### Run 
Previous: cd to project directory
```bash
docker-compose up --build
```
### See received data in kafka topic
1. Open terminal inside the Kafka broker container
```bash
docker exec -it <broker-id> bash
```
2. Check gold-data
```bash
kafka-console-consumer --bootstrap-server broker:29092 --topic gold-data --from-beginning
```
3. Check gold-history-data
```bash
kafka-console-consumer --bootstrap-server broker:29092 --topic gold-history-data --from-beginning
```
4. Check old-data
```bash
kafka-console-consumer --bootstrap-server broker:29092 --topic old-data --from-beginning
```
5. Check oil-history-data
```bash
kafka-console-consumer --bootstrap-server broker:29092 --topic oil-history-data --from-beginning
```
6. Check spx-data
```bash
kafka-console-consumer --bootstrap-server broker:29092 --topic spx-data --from-beginning
```
7. Check dxy-data
```bash
kafka-console-consumer --bootstrap-server broker:29092 --topic dxy-data --from-beginning
```
8. Check dxy-history-data
```bash
kafka-console-consumer --bootstrap-server broker:29092 --topic dxy-history-data --from-beginning
```




