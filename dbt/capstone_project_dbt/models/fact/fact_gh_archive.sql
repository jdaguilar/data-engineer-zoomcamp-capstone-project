

{{ config(materialized='table') }}

with staging_gh as (
  select *
  from  {{ ref('staging_gh_archive_view') }}
),

dim_event_type as (
    select * from {{ ref('dim_event_types') }}
),

dim_organizations as (
    select * from {{ ref('dim_organizations') }}
),

dim_repositories as (
    select * from {{ ref('dim_repositories') }}
),

dim_users as (
    select * from {{ ref('dim_users') }}
),

dim_languages as (
    select * from {{ ref('dim_languages') }}
),

select_statement as (
    select
        stg.created_at,
        stg.event_id,
        de.event_type,
        dr.repository_id,
        du.user_id,
        do.org_id,
        stg.push_id,
        stg.number_of_commits,
        dl.language
    from staging_gh stg
    left join dim_languages dl on stg.language = dl.language
    left join dim_users du on stg.user_id = du.user_id
    left join dim_repositories dr on stg.repository_id = dr.repository_id
    left join dim_organizations do on stg.org_id = do.org_id
    left join dim_event_type de on stg.event_type = de.event_type 
    order by stg.created_at 
)

-- Define the final CREATE TABLE statement to create the dim_event_type table
select * from select_statement
