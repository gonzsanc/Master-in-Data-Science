SELECT country_name, SUM (population) as npop
FROM optd_por_public
WHERE population IS NOT NULL
GROUP BY country_name
ORDER BY npop DESC LIMIT 10;

SELECT tq.country_name, COUNT (*) as nairports
FROM optd_por_public
WHERE location_type IN ('A','CA')
GROUP BY country_name
ORDER BY nairports DESC LIMIT 10;


SELECT t1.country_name, npop, nairports, 1000*(CAST(nairports as float)/npop) AS pc
FROM
    (SELECT country_name, SUM (population) as npop
    FROM optd_por_public
    WHERE population IS NOT NULL
    GROUP BY country_name) as t1,

    (SELECT country_name, count(*) as nairports
    FROM optd_por_public
    WHERE location_type IN ('A','CA')
    GROUP BY country_name) as t2

WHERE t1.country_name = t2.country_name     and npop>0
ORDER by pc DESC limit 10;

