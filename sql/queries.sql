-- ============================================================
-- Under-Five Mortality Analysis — SQL Queries
-- Database: mortality.db (SQLite)
-- Tables: countries(entity, code, year, u5mr)
--         regions(entity, code, year, u5mr)
--         country_meta(entity, code)
-- ============================================================

-- 1. Latest available under-5 mortality rate per country, ranked highest first
--    (uses a subquery to find each country's most recent year, since
--    countries don't all report the same latest year)
SELECT c.entity,
       c.year AS latest_year,
       c.u5mr AS latest_u5mr
FROM countries c
INNER JOIN (
    SELECT entity, MAX(year) AS max_year
    FROM countries
    GROUP BY entity
) latest
    ON c.entity = latest.entity AND c.year = latest.max_year
ORDER BY c.u5mr DESC;


-- 2. Percentage reduction in under-5 mortality from 1990 to the latest
--    available year, per country (self-join on the same table)
SELECT y1990.entity,
       y1990.u5mr AS u5mr_1990,
       latest.u5mr AS u5mr_latest,
       latest.year AS latest_year,
       ROUND(
           (y1990.u5mr - latest.u5mr) * 100.0 / y1990.u5mr, 1
       ) AS pct_reduction
FROM countries y1990
INNER JOIN (
    SELECT c.entity, c.year, c.u5mr
    FROM countries c
    INNER JOIN (
        SELECT entity, MAX(year) AS max_year
        FROM countries
        GROUP BY entity
    ) m ON c.entity = m.entity AND c.year = m.max_year
) latest ON y1990.entity = latest.entity
WHERE y1990.year = 1990
ORDER BY pct_reduction DESC;


-- 3. Join example: country entity + code lookup, latest rate only
--    (demonstrates a JOIN against the country_meta lookup table)
SELECT cm.entity,
       cm.code,
       c.year,
       c.u5mr
FROM country_meta cm
INNER JOIN countries c ON cm.entity = c.entity
INNER JOIN (
    SELECT entity, MAX(year) AS max_year
    FROM countries
    GROUP BY entity
) latest ON c.entity = latest.entity AND c.year = latest.max_year
ORDER BY c.u5mr ASC;


-- 4. Regional trend: average of the four tracked decade points
--    (1990, 2000, 2010, latest) per region
SELECT entity,
       MAX(CASE WHEN year = 1990 THEN u5mr END) AS y1990,
       MAX(CASE WHEN year = 2000 THEN u5mr END) AS y2000,
       MAX(CASE WHEN year = 2010 THEN u5mr END) AS y2010,
       MAX(CASE WHEN year = 2024 THEN u5mr END) AS y2024
FROM regions
GROUP BY entity;


-- 5. Countries with a rate above the most recent African regional
--    average (cross-table comparison between countries and regions)
SELECT c.entity, c.year, c.u5mr
FROM countries c
WHERE c.year = (SELECT MAX(year) FROM countries)
  AND c.u5mr > (
      SELECT u5mr FROM regions
      WHERE entity = 'Africa'
      ORDER BY year DESC LIMIT 1
  );
