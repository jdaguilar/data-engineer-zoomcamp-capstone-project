source .env

docker run data-engineer-zoomcamp-capstone-project:latest \
driver local:///opt/application/process_gh_archive.py \
--year 2023 \
--month 01 \
--day 01 \
--source_files_pattern $GOOGLE_CLOUD_STORAGE_SOURCE_FILES \
--destination_files_pattern $GOOGLE_CLOUD_STORAGE_DESTINATION_FILES
