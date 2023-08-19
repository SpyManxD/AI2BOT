# 3DataProcessing.py

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

from pyspark.ml.feature import KafkaStreams, NLP, MinMaxScaler
from pyspark.ml.clustering import ClusteringOutlierDetector

spark = SparkSession.builder.config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka:0.10').getOrCreate()

df = spark.readStream.format('kafka').option('kafka.bootstrap.servers', 'localhost:9092').load()

# Calculate indicators
df = df.withColumn('rsi', rsi(col('close'), 14)) \
       .withColumn('sma', sma(col('close'), 200)) \
       .withColumn('kc', klinger_channels(col('high'), col('low'), col('close')))

# Sentiment analysis
df = NLP(df, input_col="news", output_col="sentiment")

# Min/max scaling
scaler = MinMaxScaler(inputCol='sentiment', outputCol='scaled_sentiment')
df = scaler.fit(df).transform(df)

# Outlier detection
detector = ClusteringOutlierDetector(featuresCol='scaled_sentiment')
df = detector.fit(df).transform(df)

query = df.writeStream.format('console').start()