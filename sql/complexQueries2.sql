SELECT 
"2char_code"
,o.name
,flight_freq

FROM ref_airline_nb_of_flights AS r
LEFT OUTER JOIN optd_airlines AS o
on o."2char_code"  = r.airline_code_2c
ORDER BY flight_freq DESC 
LIMIT 10
;

SELECT AVG(cast(flight_freq as float)) from ref_airline_nb_of_flights;


SELECT name, country_name, elevation
FROM optd_por_public
WHERE  
    elevation > (
            SELECT avg(elevation) FROM optd_por_public 
            WHERE
            location_type='C'
            AND elevation IS NOT NULL
    )
ORDER BY elevation DESC
LIMIT 10
;

SELECT country_name, count(*) AS city_nbr
FROM optd_por_public
WHERE  
    elevation > (
            SELECT avg(elevation) FROM optd_por_public 
            WHERE
            location_type='C'
            AND elevation IS NOT NULL
    )

GROUP BY country_name
HAVING count(*)>3
ORDER BY COUNT(*) DESC
LIMIT 10
;
