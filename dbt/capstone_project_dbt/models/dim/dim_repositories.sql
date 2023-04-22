
{{ config(materialized='table') }}

-- Define a CTE to get distinct event types from your source table
with distinct_repositories as (
  select distinct 
    repository_id,
    repository_name,
    repository_url
  from {{ source('bigquery_sources', 'staging_gh_archive')}}
),

-- Define the final SELECT statement to create the dim_event_type table
select_statement as (
  select
    repository_id,
    repository_name,
    repository_url  
  from distinct_repositories
  where repository_id is not null
  order by repository_id asc
)

-- Define the final CREATE TABLE statement to create the dim_event_type table
select * from select_statement


