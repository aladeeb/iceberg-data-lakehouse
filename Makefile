MINIO_ALIAS ?= minio
BUCKET_NAME ?= mybucket

.PHONY: create-bucket

set-minio-alias:
	@mc alias set $(MINIO_ALIAS) http://localhost:9000 minioadmin minioadmin
	@echo "MinIO alias '$(MINIO_ALIAS)' set to http://localhost:9000"

create-bucket:
	@mc mb $(MINIO_ALIAS)/$(BUCKET_NAME)
	@echo "Bucket '$(BUCKET_NAME)' created in MinIO alias '$(MINIO_ALIAS)'"