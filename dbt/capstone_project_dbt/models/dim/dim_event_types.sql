
{{ config(materialized='table') }}

-- Define a CTE to get distinct event types from your source table
with distinct_event_types as (
  select distinct event_type
  from  {{ ref('staging_gh_archive_view') }}
),

-- Define the final SELECT statement to create the dim_event_type table
select_statement as (
  select
    event_type
  from distinct_event_types
  where event_type is not null
  order by event_type asc
)

-- Define the final CREATE TABLE statement to create the dim_event_type table
select * from select_statement
