from pyspark.sql import SparkSession

spark = SparkSession \
        .builder \
        .appName("Ingest Bronze - Iceberg") \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4,org.apache.iceberg:iceberg-spark-runtime-3.5_2.13:1.9.0") \
        .getOrCreate()

sc = spark.sparkContext
sc._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "http://minio:9000")
sc._jsc.hadoopConfiguration().set("fs.s3a.access.key", "minioadmin")
sc._jsc.hadoopConfiguration().set("fs.s3a.secret.key", "minioadmin")
sc._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
sc._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
sc._jsc.hadoopConfiguration().set("fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")


data_path = "s3a://raw/" 

movies = spark.read.parquet(f"{data_path}/movies.parquet")
ratings = spark.read.parquet(f"{data_path}/ratings.parquet")
tags = spark.read.parquet(f"{data_path}/tags.parquet")
links = spark.read.parquet(f"{data_path}/links.parquet")


