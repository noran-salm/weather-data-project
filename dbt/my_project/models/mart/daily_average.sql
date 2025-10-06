{{ config(
    materialized='table'
) }}

select
    city,
    date(weather_time_local) as date,
    round(avg(temperature)::numeric, 2) as avg_temperature,
    round(avg(wind_speed)::numeric, 2) as avg_wind_speed,
    round(avg(humidity)::numeric, 2) as avg_humidity,
    round(avg(pressure)::numeric, 2) as avg_pressure,
    round(avg(cloudcover)::numeric, 2) as avg_cloudcover,
    round(avg(precipitation)::numeric, 2) as avg_precipitation,
    round(avg(dewpoint)::numeric, 2) as avg_dewpoint,
    round(avg(weathercode)::numeric, 0) as avg_weathercode
from {{ ref('stg_weather_data') }}
group by
    city,
    date(weather_time_local)
order by
    city,
    date(weather_time_local)
