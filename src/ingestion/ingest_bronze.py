from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Ingest Data to Iceberg") \
    .config("spark.jars.packages", "org.apache.iceberg:iceberg-spark3-runtime:0.13.1,org.apache.hadoop:hadoop-aws:3.2.0") \
    .getOrCreate()


sc = spark.sparkContext
sc._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "http://minio:9000")
sc._jsc.hadoopConfiguration().set("fs.s3a.access.key", "minioadmin")
sc._jsc.hadoopConfiguration().set("fs.s3a.secret.key", "minioadmin")
sc._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
sc._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
sc._jsc.hadoopConfiguration().set("fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")


data_path = "./data/movie-lens/small/"  # adjust to your download path

movies = spark.read.csv(f"{data_path}/movies.csv", header=True)
ratings = spark.read.csv(f"{data_path}/ratings.csv", header=True)
tags = spark.read.csv(f"{data_path}/tags.csv", header=True)
links = spark.read.csv(f"{data_path}/links.csv", header=True)

movies.write.format("iceberg").mode("overwrite").parquet("s3a://bronze/movies/")
ratings.write.format("iceberg").mode("overwrite").parquet("s3a://bronze/ratings/")
tags.write.format("iceberg").mode("overwrite").parquet("s3a://bronze/tags/")
links.write.format("iceberg").mode("overwrite").parquet("s3a://bronze/links/")

print("Ingested CSVs to MinIO as Parquet")