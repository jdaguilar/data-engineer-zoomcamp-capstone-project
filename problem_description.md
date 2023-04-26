# Problem description

El objetivo en este proyecto es demostrar un caso de ejemplo de como aplicar un Data Pipeline para procesar los datos de GitHub Archive.

Si bien ya existe un ejemplo de un Data Warehouse en BigQuery, la idea principal es desarrollar el data pipeline para solo traerse los datos necesarios para el dashboard.

El resultado en este proyecto es conseguir un Data Ware House para analizar la actividad en GitHub desde enero de 2023. Específicamente, la idea es encontrar cuales son los repositorios que han tenido mayor actividad en este periodo, cuales han sido los usuarios que mas han aportado a los repositorios, asi como las organizaciones y sobretodo los lenguajes que manejan.

Para mas información del dataset consultar:
https://www.gharchive.org/

# Cloud

La nube utilizada es Google Cloud, y los servicios que se utilizan son:

- Cloud Function, para traer la data cruda de GH
- Dataproc: Servicio de Google Cloud para correr un entorno de Spark, se utiliza para correr scripts hechos en pyspark
- Cloud Composer: Apache Airflow

Adicionalmente, se utiliza DBT cloud para construir las diferentes tablas en el Data Warehouse

Note: En el futuro se implementara IaC

