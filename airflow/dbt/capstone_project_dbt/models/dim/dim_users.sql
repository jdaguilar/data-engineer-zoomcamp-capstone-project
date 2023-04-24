
{{ config(materialized='table') }}

-- Define a CTE to get distinct event types from your source table
with distinct_users as (
  select distinct 
    user_id,
    user_name,
    user_url,
    user_avatar_url
  from {{ source('bigquery_sources', 'staging_gh_archive')}}
),

-- Define the final SELECT statement to create the dim_event_type table
select_statement as (
  select
    user_id,
    user_name,
    user_url,
    user_avatar_url
  from distinct_users
  where user_id is not null
  order by user_id asc
)

-- Define the final CREATE TABLE statement to create the dim_event_type table
select * from select_statement
