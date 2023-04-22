source .env

gcloud dataproc jobs submit pyspark process_gh_archive_dataproc.py\
    --cluster=${DATAPROC_CLUSTER_NAME} \
    --region=${REGION} \
    -- \
    --year=2023 \
    --month=01 \
    --day=01 \
    --source_files_pattern=${GOOGLE_CLOUD_STORAGE_SOURCE_FILES} \
    --destination_files_pattern=${GOOGLE_CLOUD_STORAGE_DESTINATION_FILES}



