FROM gcr.io/datamechanics/spark:platform-3.1-dm14

ARG GOOGLE_CLOUD_STORAGE_BUCKET
ENV PYSPARK_MAJOR_PYTHON_VERSION=3

USER root
WORKDIR /opt/application/
RUN wget https://storage.googleapis.com/hadoop-lib/gcs/gcs-connector-hadoop3-latest.jar
RUN mv gcs-connector-hadoop3-latest.jar /opt/spark/jars

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

COPY credentials/google_credentials.json /opt/application/google_credentials.json
ENV GOOGLE_CREDENTIALS_PATH=/opt/application/google_credentials.json
ENV GOOGLE_CLOUD_STORAGE_BUCKET=${GOOGLE_CLOUD_STORAGE_BUCKET}

COPY process_gh_archive.py .
