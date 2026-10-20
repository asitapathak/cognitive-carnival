-- Cognitive Performance & Wellness Analytics: business questions in SQL
-- Run in DuckDB. dataset.csv is the same file the Streamlit app uses.

-- Clean data and flag high performers (logic score at or above the 80th percentile)
CREATE OR REPLACE VIEW people AS
SELECT *,
       PMAT24_A_CR >= (SELECT quantile_cont(PMAT24_A_CR, 0.8) FROM read_csv_auto('dataset.csv')) AS high_performer
FROM read_csv_auto('dataset.csv')
WHERE PMAT24_A_CR IS NOT NULL
  AND PSQI_Score IS NOT NULL
  AND PicSeq_AgeAdj IS NOT NULL
  AND LifeSatisf_Unadj IS NOT NULL;


-- Q1. What are the headline numbers?
SELECT COUNT(*)                                   AS people,
       ROUND(AVG(PMAT24_A_CR), 1)                 AS avg_logic_score,
       ROUND(100 * AVG(high_performer::INT), 1)   AS pct_high_performers,
       ROUND(AVG(PSQI_Score), 1)                  AS avg_sleep_problem_score
FROM people;


-- Q2. Do people with poor sleep perform worse?
SELECT CASE WHEN PSQI_Score > 5 THEN 'Poor sleep' ELSE 'Good sleep' END AS sleep_group,
       COUNT(*)                                 AS people,
       ROUND(AVG(PMAT24_A_CR), 1)               AS avg_logic_score,
       ROUND(100 * AVG(high_performer::INT), 1) AS pct_high_performers
FROM people
GROUP BY sleep_group
ORDER BY sleep_group DESC;


-- Q3. How much does working memory matter?
WITH quarters AS (
    SELECT *, NTILE(4) OVER (ORDER BY PicSeq_AgeAdj) AS memory_quarter
    FROM people
)
SELECT memory_quarter,
       COUNT(*)                                 AS people,
       ROUND(AVG(PMAT24_A_CR), 1)               AS avg_logic_score,
       ROUND(100 * AVG(high_performer::INT), 1) AS pct_high_performers
FROM quarters
GROUP BY memory_quarter
ORDER BY memory_quarter;


-- Q4. Does performance differ by age band and gender?
SELECT Age AS age_band,
       Gender,
       COUNT(*)                                 AS people,
       ROUND(AVG(PMAT24_A_CR), 1)               AS avg_logic_score,
       ROUND(100 * AVG(high_performer::INT), 1) AS pct_high_performers
FROM people
GROUP BY Age, Gender
HAVING COUNT(*) >= 30
ORDER BY Age, Gender;


-- Q5. What happens when good sleep and strong memory come together?
WITH grouped AS (
    SELECT *,
           CASE WHEN PSQI_Score > 5 THEN 'Poor sleep' ELSE 'Good sleep' END AS sleep_group,
           CASE WHEN PicSeq_AgeAdj >= (SELECT MEDIAN(PicSeq_AgeAdj) FROM people)
                THEN 'Strong memory' ELSE 'Weaker memory' END AS memory_group
    FROM people
)
SELECT sleep_group,
       memory_group,
       COUNT(*)                                 AS people,
       ROUND(AVG(PMAT24_A_CR), 1)               AS avg_logic_score,
       ROUND(100 * AVG(high_performer::INT), 1) AS pct_high_performers
FROM grouped
GROUP BY sleep_group, memory_group
ORDER BY pct_high_performers DESC;
