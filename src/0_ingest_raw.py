from pyspark.sql import SparkSession

spark = SparkSession \
        .builder \
        .appName("Ingest Raw") \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4") \
        .getOrCreate()

sc = spark.sparkContext
sc._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "http://minio:9000")
sc._jsc.hadoopConfiguration().set("fs.s3a.access.key", "minioadmin")
sc._jsc.hadoopConfiguration().set("fs.s3a.secret.key", "minioadmin")
sc._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
sc._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
sc._jsc.hadoopConfiguration().set("fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")


data_path = "./data/movie-lens/small" 

movies = spark.read.csv(f"{data_path}/movies.csv", header=True)
ratings = spark.read.csv(f"{data_path}/ratings.csv", header=True)
tags = spark.read.csv(f"{data_path}/tags.csv", header=True)
links = spark.read.csv(f"{data_path}/links.csv", header=True)

movies.write.parquet("s3a://raw/movies.parquet", mode="overwrite")
ratings.write.parquet("s3a://raw/ratings.parquet", mode="overwrite")
tags.write.parquet("s3a://raw/tags.parquet", mode="overwrite")
links.write.parquet("s3a://raw/links.parquet", mode="overwrite")