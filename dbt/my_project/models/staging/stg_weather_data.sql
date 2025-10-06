{{ config(
    materialized='table',
    unique_key='id'
) }}

with source as (
    select * 
    from {{ source('dev','raw_weather_data') }}
),
de_dup as (
    select 
        *,
        ROW_NUMBER() OVER (PARTITION BY time ORDER BY inserted_at) AS rn
    from source
)

select 
    id,
    city,
    temperature,
    wind_speed,
    humidity,
    pressure,
    cloudcover,
    precipitation,
    dewpoint,
    weathercode,
    time as weather_time_local,
    inserted_at + (utc_offset || ' hours')::interval as inserted_at_local
from de_dup    
where rn = 1
