# Peer review criteria

Please cosider this criteria to evaluate this project.

1. **Problem description**

- 0 points: Problem is not described
- 1 point: Problem is described but shortly or not clearly
- 2 points: Problem is well described and it's clear what the problem the project solves

2. **Cloud**

- 0 points: Cloud is not used, things run only locally
- 2 points: The project is developed in the cloud
- 4 points: The project is developed in the cloud and IaC tools are used

3. **Data ingestion (batch)**

    Batch / Workflow orchestration

    - 0 points: No workflow orchestration
    - 2 points: Partial workflow orchestration: some steps are orchestrated, some run manually
    - 4 points: End-to-end pipeline: multiple steps in the DAG, uploading data to data lake

4. **Data warehouse**

- 0 points: No DWH is used
- 2 points: Tables are created in DWH, but not optimized
- 4 points: Tables are partitioned and clustered in a way that makes sense for the upstream queries (with explanation)

5. **Transformations (dbt, spark, etc)**

- 0 points: No tranformations
- 2 points: Simple SQL transformation (no dbt or similar tools)
- 4 points: Tranformations are defined with dbt, Spark or similar technologies

6. **Dashboard**

- 0 points: No dashboard
- 2 points: A dashboard with 1 tile
- 4 points: A dashboard with 2 tiles

7. **Reproducibility**

- 0 points: No instructions how to run code at all
- 2 points: Some instructions are there, but they are not complete
- 4 points: Instructions are clear, it's easy to run the code, and the code works