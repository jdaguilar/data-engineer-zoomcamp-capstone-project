# How to Reproduce

This guide explain the steps to reproduce this project.

*Note: Before continuing, please create a fork of this repository.*

## 1. Configure GCP

### 1.1. Create a GCP account

The first thing you need to do is creating a GCP account. To do this go to the main page of Google Cloud [here](https://cloud.google.com/). After that, you need to click on **Start Free** and follow the instructions.

*Note: If you're going to create a GCP account for the first time, you will have $300 in credits, very useful to test this project.*

### 1.2. Create a Service Account file

Click on the following link to create a service account key file:

[Create and delete service account keys](https://cloud.google.com/iam/docs/keys-create-delete)

After you have downloaded the JSON file, create a folder called `credentials` in the root of this project, move the credentials file inside this directoy and finally rename the file as `google_application_credentials.json`

### 1.3. Grant roles

It's necessary to grant specific permission to the `client_email` provided by the JSON file. To do this follow the instructions bellow:

1. Open the `google_application_credentials.json` file and copy the `client_email` value.

2. Log in into the GCP console, then go to IAM-Admin->IAM.

3. Grant al least the following roles:
    - BigQuery Admin
    - Composer Administrator
    - Cloud Composer v2 API Service Agent Extension
    - Cloud Functions Developer
    - Cloud Functions Invoker
    - Dataproc Metastore Metadata User
    - Dataproc Service Agent
    - Dataproc Worker
    - Storage Admin
    - Storage Object Admin

    *Note: Only for testing purposes, you can grant a `Owner` role to the service account*

## 2. Configure DBT

Go  to https://www.getdbt.com/ and creates a free account. After creating your account you need to create your project following the instructions:

1. Choose a name in *Name your project* option.
2. In *Choose a connection*, select BigQuery.
3. In *Configure your environment*, upload the service account file.
    - You have to configure *Development Credentials*, setting *dataset* field with the value `capstone_project_dw`.
4. In *Setup a Repository*, choose GitHub:
    - Yo need to sign in to github to enable DBT, then you'll able to choose `data-engineer-zoomcamp-capstone-project`
5. Go to *Account Settings*, select project you have created, and change *Project subdirectory* to `dbt/capstone_project_dbt`
6. Select *Develop* tab and click on *initialize dbt project*.
7. Go to Deploy -> Environments and then create an environment, choose a *Name* for this environment, and in *Deployment Credentials* change dataset to `capstone_project_dw`.

8. Finally, Go to Deploy -> Jobs and then click on *Create Job*
    - Set the environment previously created
    - In commands, set dbt run


# References:

https://docs.getdbt.com/docs/cloud/git/connect-github
https://docs.getdbt.com/docs/quickstarts/dbt-cloud/bigquery#generate-bigquery-credentials