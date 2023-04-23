source .env

docker build -t data-engineer-zoomcamp-capstone-project:latest \
--no-cache \
--build-arg GOOGLE_CLOUD_STORAGE_BUCKET=$GOOGLE_CLOUD_STORAGE_BUCKET .
