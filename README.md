Building a local data lakehouse solution
---
## Tech stack
- Minio (as a blob storage, S3 compatible)
- Apache Spark (as a writer engine, could be reader as well at some point)
- Apache Iceberg (as a table format)
- Apache Gravitino (as an Iceberg catalog)
- DuckDB (as a reader engine)
- Trino (as a reader engine)
- Apache Airflow (for orchestration, not yet decided if this will be in the scope or not)

Learning References
---
- (Setting up Apache Spark on Docker)[https://medium.com/@MarinAgli1/setting-up-a-spark-standalone-cluster-on-docker-in-layman-terms-8cbdc9fdd14b]