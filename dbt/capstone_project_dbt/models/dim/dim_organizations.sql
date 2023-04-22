
{{ config(materialized='table') }}

-- Define a CTE to get distinct event types from your source table
with distinct_organizations as (
  select distinct 
    org_id,
    org_name,
    org_url,
    org_avatar_url
  from {{ source('bigquery_sources', 'staging_gh_archive')}}
),

-- Define the final SELECT statement to create the distinct_organizations table
select_statement as (
  select
    org_id,
    org_name,
    org_url,
    org_avatar_url
  from distinct_organizations
  where org_id is not null
  order by org_id asc
)

-- Define the final CREATE TABLE statement to create the dim_event_type table
select * from select_statement


