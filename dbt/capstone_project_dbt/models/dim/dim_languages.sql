
{{ config(materialized='table') }}

-- Define a CTE to get distinct languages from your source table
with distinct_languages as (
  select distinct language
  from  {{ ref('staging_gh_archive_view') }}
),

-- Define the final SELECT statement to create the dim_language table
select_statement as (
  select
    `language`
  from distinct_languages
  where `language` is not null
  order by language asc
)

-- Define the final CREATE TABLE statement to create the dim_language table
select * from select_statement
