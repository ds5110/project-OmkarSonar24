QUERY_CREATE_INPATIENT_HAEMORRHAGIC_COHORT = """
SELECT co.condition_occurrence_id,
       co.person_id,
       co.condition_concept_id,
       co.condition_start_date,
       co.condition_end_date,
       vo.visit_occurrence_id, -- Calculate age as the difference between the year of condition_start_date and the year_of_birth
 EXTRACT(YEAR
         FROM co.condition_start_date) - p.year_of_birth AS age,
 p.gender_concept_id, -- Include all descendant concept IDs
 ca2.descendant_concept_id AS condition_descendant_concept_id INTO schema_name.inpatient_stroke_haemorrhagic
FROM omop_cdm_53_pmtx_202203.condition_occurrence co
INNER JOIN omop_cdm_53_pmtx_202203.visit_occurrence vo ON co.visit_occurrence_id = vo.visit_occurrence_id
INNER JOIN omop_cdm_53_pmtx_202203.person p ON co.person_id = p.person_id -- Join for visit descendant concepts
INNER JOIN
  (SELECT ca.descendant_concept_id,
          ca.ancestor_concept_id
   FROM omop_cdm_53_pmtx_202203.concept_ancestor ca
   WHERE ca.ancestor_concept_id IN (9201,
                                    9203,
                                    262)) ca1 ON vo.visit_concept_id = ca1.descendant_concept_id -- Join for condition descendant concepts
INNER JOIN
  (SELECT ca.descendant_concept_id,
          ca.ancestor_concept_id
   FROM omop_cdm_53_pmtx_202203.concept_ancestor ca
   WHERE ancestor_concept_id IN (376713,
                                 439847,
                                 432923,
                                 35609033,
                                 4319328)
     AND descendant_concept_id NOT IN (4201421, -- Brain Stem
                                       4249574, -- Haemorrhagic code from here to below
                                       4071589,
                                       37016924,
                                       4345688,
                                       42873157,
                                       444197,
                                       444198,
                                       444196,
                                       437106,
                                       4071732,
                                       4048277,
                                       4048278,
                                       434155,
                                       260841,
                                       4134162,
                                       4017107)) ca2 ON co.condition_concept_id = ca2.descendant_concept_id
WHERE age >= 18
ORDER BY co.person_id,
         co.condition_start_date;
"""

QUERY_CREATE_HAEMORRHAGIC_STROKE_COHORT = f"""
WITH first_stroke_occurrence AS
  (-- Select distinct stroke occurrences by condition start date
 SELECT condition_occurrence_id,
        person_id,
        condition_concept_id,
        condition_start_date,
        condition_end_date,
        age,
        gender_concept_id,
        condition_descendant_concept_id,
        ROW_NUMBER() OVER (PARTITION BY person_id
                           ORDER BY condition_start_date ASC) AS row_num
   FROM schema_name.inpatient_stroke_haemorrhagic),
     distinct_stroke_occurrence AS
  (-- Filter for distinct condition_start_dates
 SELECT condition_occurrence_id,
        person_id,
        condition_concept_id,
        condition_start_date,
        condition_end_date,
        age,
        gender_concept_id,
        condition_descendant_concept_id,
        DENSE_RANK() OVER (PARTITION BY person_id
                           ORDER BY condition_start_date ASC) AS distinct_rank
   FROM first_stroke_occurrence),
     multiple_stroke_occurrence AS
  (-- Find patients with multiple stroke occurrences within 180 days
 SELECT f1.person_id
   FROM distinct_stroke_occurrence f1
   JOIN distinct_stroke_occurrence f2 ON f1.person_id = f2.person_id
   AND f1.distinct_rank = 1 -- First stroke occurrence

   AND f2.distinct_rank = 2 -- Second stroke occurrence

   WHERE (f2.condition_start_date - f1.condition_start_date) <= 180 -- Difference in days

   GROUP BY f1.person_id),
     stroke_cohort AS
  (-- Main query to select relevant stroke occurrences
 SELECT f.*,
        op.observation_period_start_date,
        op.observation_period_end_date,
        op.observation_period_id
   FROM first_stroke_occurrence f
   INNER JOIN omop_cdm_53_pmtx_202203.observation_period op ON op.person_id = f.person_id
   WHERE f.person_id IN
       (SELECT person_id
        FROM multiple_stroke_occurrence)
     AND f.row_num = 1
     AND f.condition_start_date >= op.observation_period_start_date + INTERVAL '180 days'
     AND op.observation_period_end_date >= f.condition_start_date + INTERVAL '180 days') -- Final step: Insert the results into the new table

SELECT * INTO schema_name.haemorrhagic_stroke_cohort
FROM stroke_cohort;
"""

QUERY_CREATE_INPATIENT_ISCHEMIC_COHORT = """
SELECT co.condition_occurrence_id,
       co.person_id,
       co.condition_concept_id,
       co.condition_start_date,
       co.condition_end_date,
       vo.visit_occurrence_id, -- Calculate age as the difference between the year of condition_start_date and the year_of_birth
 EXTRACT(YEAR
         FROM co.condition_start_date) - p.year_of_birth AS age,
 p.gender_concept_id, -- Include all descendant concept IDs
 ca2.descendant_concept_id AS condition_descendant_concept_id INTO schema_name.inpatient_stroke_ischemic
FROM omop_cdm_53_pmtx_202203.condition_occurrence co
INNER JOIN omop_cdm_53_pmtx_202203.visit_occurrence vo ON co.visit_occurrence_id = vo.visit_occurrence_id
INNER JOIN omop_cdm_53_pmtx_202203.person p ON co.person_id = p.person_id -- Join for visit descendant concepts
INNER JOIN
  (SELECT ca.descendant_concept_id,
          ca.ancestor_concept_id
   FROM omop_cdm_53_pmtx_202203.concept_ancestor ca
   WHERE ca.ancestor_concept_id IN (9201,
                                    9203,
                                    262)) ca1 ON vo.visit_concept_id = ca1.descendant_concept_id -- Join for condition descendant concepts
INNER JOIN
  (SELECT ca.descendant_concept_id,
          ca.ancestor_concept_id
   FROM omop_cdm_53_pmtx_202203.concept_ancestor ca
   WHERE ca.ancestor_concept_id IN (372924,
                                    375557,
                                    443454,
                                    441874,
                                    4310996,
                                    45876543,
                                    4319330)
     AND ca.descendant_concept_id NOT IN (4201421)) ca2 ON co.condition_concept_id = ca2.descendant_concept_id
WHERE age >= 18
ORDER BY co.person_id,
         co.condition_start_date;
"""

QUERY_CREATE_ISCHEMIC_STROKE_COHORT = f"""
WITH first_stroke_occurrence AS
  (-- Select distinct stroke occurrences by condition start date
 SELECT condition_occurrence_id,
        person_id,
        condition_concept_id,
        condition_start_date,
        condition_end_date,
        age,
        gender_concept_id,
        condition_descendant_concept_id,
        ROW_NUMBER() OVER (PARTITION BY person_id
                           ORDER BY condition_start_date ASC) AS row_num
   FROM schema_name.inpatient_stroke_ischemic),
     distinct_stroke_occurrence AS
  (-- Filter for distinct condition_start_dates
 SELECT condition_occurrence_id,
        person_id,
        condition_concept_id,
        condition_start_date,
        condition_end_date,
        age,
        gender_concept_id,
        condition_descendant_concept_id,
        DENSE_RANK() OVER (PARTITION BY person_id
                           ORDER BY condition_start_date ASC) AS distinct_rank
   FROM first_stroke_occurrence),
     multiple_stroke_occurrence AS
  (-- Find patients with multiple stroke occurrences within 180 days
 SELECT f1.person_id
   FROM distinct_stroke_occurrence f1
   JOIN distinct_stroke_occurrence f2 ON f1.person_id = f2.person_id
   AND f1.distinct_rank = 1 -- First stroke occurrence

   AND f2.distinct_rank = 2 -- Second stroke occurrence

   WHERE (f2.condition_start_date - f1.condition_start_date) <= 180 -- Difference in days

   GROUP BY f1.person_id),
     stroke_cohort AS
  (-- Main query to select relevant stroke occurrences
 SELECT f.*,
        op.observation_period_start_date,
        op.observation_period_end_date,
        op.observation_period_id
   FROM first_stroke_occurrence f
   INNER JOIN omop_cdm_53_pmtx_202203.observation_period op ON op.person_id = f.person_id
   WHERE f.person_id IN
       (SELECT person_id
        FROM multiple_stroke_occurrence)
     AND f.row_num = 1
     AND f.condition_start_date >= op.observation_period_start_date + INTERVAL '180 days'
     AND op.observation_period_end_date >= f.condition_start_date + INTERVAL '180 days') -- Final step: Insert the results into the new table

SELECT * INTO schema_name.ischemic_stroke_cohort
FROM stroke_cohort;
"""

QUERY_CREATE_COMMON_STROKE_COHORT = f"""
SELECT hsc.*
INTO schema_name.common_people_cohort
FROM schema_name.haemorrhagic_stroke_cohort hsc
WHERE hsc.person_id IN (SELECT hsc.person_id
   FROM schema_name.haemorrhagic_stroke_cohort hsc
   INNER JOIN schema_name.ischemic_stroke_cohort isc ON hsc.person_id = isc.person_id);
"""

QUERY_CREATE_HAEMORRHAGIC_ONLY_COHORT = f"""
SELECT hsc.* INTO schema_name.haemorrhagic_only_stroke_cohort
FROM schema_name.haemorrhagic_stroke_cohort hsc
WHERE hsc.person_id NOT IN
    (SELECT person_id
     FROM schema_name.common_people_cohort);
"""
    
QUERY_CREATE_ISCHEMIC_ONLY_COHORT = f"""
SELECT isc.* INTO schema_name.ischemic_only_stroke_cohort
FROM schema_name.ischemic_stroke_cohort isc
WHERE isc.person_id NOT IN
    (SELECT person_id
     FROM schema_name.common_people_cohort);
"""

QUERY_CREATE_HAEMORRHAGIC_ONLY_VISITS = f"""
CREATE TABLE schema_name.haemorrhagic_only_visits AS 
SELECT 
hosc.person_id, hosc.condition_concept_id, c.concept_name AS condition_concept_name, hosc.condition_start_date, 
vo.visit_start_date, vo.visit_end_date, vo.visit_concept_id, c2.concept_name AS visit_concept_name, 
vo.discharge_to_concept_id, c3.concept_name  AS discharge_to_concept_name 
FROM schema_name.haemorrhagic_only_stroke_cohort hosc 
INNER JOIN omop_cdm_53_pmtx_202203.visit_occurrence vo ON hosc.person_id = vo.person_id 
INNER JOIN omop_cdm_53_pmtx_202203.concept c ON hosc.condition_concept_id  = c.concept_id
INNER JOIN omop_cdm_53_pmtx_202203.concept c2 ON vo.visit_concept_id = c2.concept_id
INNER JOIN omop_cdm_53_pmtx_202203.concept c3 ON vo.discharge_to_concept_id = c3.concept_id 
WHERE vo.visit_start_date >= hosc.condition_start_date 
ORDER BY hosc.person_id, hosc.condition_start_date, vo.visit_start_date ;
"""

QUERY_CREATE_ISCHEMIC_ONLY_VISITS = f"""
CREATE TABLE schema_name.ischemic_only_visits AS 
SELECT 
iosc.person_id, iosc.condition_concept_id, c.concept_name AS condition_concept_name, iosc.condition_start_date, 
vo.visit_start_date, vo.visit_end_date, vo.visit_concept_id, c2.concept_name AS visit_concept_name, 
vo.discharge_to_concept_id, c3.concept_name  AS discharge_to_concept_name 
FROM schema_name.ischemic_only_stroke_cohort iosc 
INNER JOIN omop_cdm_53_pmtx_202203.visit_occurrence vo ON iosc.person_id = vo.person_id 
INNER JOIN omop_cdm_53_pmtx_202203.concept c ON iosc.condition_concept_id  = c.concept_id
INNER JOIN omop_cdm_53_pmtx_202203.concept c2 ON vo.visit_concept_id = c2.concept_id
INNER JOIN omop_cdm_53_pmtx_202203.concept c3 ON vo.discharge_to_concept_id = c3.concept_id 
WHERE vo.visit_start_date >= iosc.condition_start_date 
ORDER BY iosc.person_id, iosc.condition_start_date, vo.visit_start_date ;
"""

QUERY_FETCH_PROCEDURE_PLOT1_1="""
WITH FirstLastCondition AS (
    SELECT
        ish.person_id,
        MIN(ish.condition_start_date) AS first_condition_start_date,
        MAX(ish.condition_start_date) AS last_condition_start_date
    FROM schema_name.inpatient_stroke_haemorrhagic ish
    GROUP BY ish.person_id
)
SELECT 
    hbp.procedure_concept_id, 
    hbp.concept_name, 
    COUNT(DISTINCT hosc.person_id) AS distinct_person_count
FROM schema_name.haemorrhagic_only_stroke_cohort hosc
INNER JOIN omop_cdm_53_pmtx_202203.procedure_occurrence po 
    ON po.person_id = hosc.person_id
INNER JOIN schema_name.haemorrhagic_bucket_procedures hbp 
    ON hbp.procedure_concept_id = po.procedure_concept_id
INNER JOIN FirstLastCondition flc 
    ON flc.person_id = hosc.person_id
WHERE po.procedure_date >= flc.first_condition_start_date
  AND po.procedure_date < (flc.last_condition_start_date + INTERVAL '180 days')
  AND po.procedure_concept_id != 2617378
GROUP BY hbp.procedure_concept_id, hbp.concept_name
ORDER BY distinct_person_count DESC
LIMIT 10;
"""

QUERY_FETCH_PROCEDURE_PLOT1_2="""
WITH FirstLastCondition AS (
    SELECT
        isi.person_id,
        MIN(isi.condition_start_date) AS first_condition_start_date,
        MAX(isi.condition_start_date) AS last_condition_start_date
    FROM schema_name.inpatient_stroke_ischemic isi
    GROUP BY isi.person_id
)
SELECT 
    ibp.procedure_concept_id, 
    ibp.concept_name, 
    COUNT(DISTINCT iosc.person_id) AS distinct_person_count
FROM schema_name.ischemic_only_stroke_cohort iosc
INNER JOIN omop_cdm_53_pmtx_202203.procedure_occurrence po 
    ON po.person_id = iosc.person_id
INNER JOIN schema_name.ischemic_bucket_procedures ibp 
    ON ibp.procedure_concept_id = po.procedure_concept_id
INNER JOIN FirstLastCondition flc 
    ON flc.person_id = iosc.person_id
WHERE po.procedure_date >= flc.first_condition_start_date
  AND po.procedure_date < (flc.last_condition_start_date + INTERVAL '180 days')
  AND po.procedure_concept_id != 2617378
GROUP BY ibp.procedure_concept_id, ibp.concept_name
ORDER BY distinct_person_count DESC
LIMIT 10;
"""


QUERY_FETCH_PROCEDURE_PLOT2_1 = """

WITH FirstLastCondition AS (
    SELECT
        ish.person_id,
        MIN(ish.condition_start_date) AS first_condition_start_date,
        MAX(ish.condition_start_date) AS last_condition_start_date
    FROM schema_name.inpatient_stroke_haemorrhagic ish
    GROUP BY ish.person_id
)
SELECT 
    hbp.procedure_concept_id, 
    hbp.concept_name, 
    hbp.procedure_category,
    hbp.procedure_count,
    COUNT(DISTINCT hosc.person_id) AS distinct_person_count
FROM schema_name.haemorrhagic_only_stroke_cohort hosc
INNER JOIN omop_cdm_53_pmtx_202203.procedure_occurrence po 
    ON po.person_id = hosc.person_id
INNER JOIN schema_name.haemorrhagic_bucket_procedures hbp 
    ON hbp.procedure_concept_id = po.procedure_concept_id
INNER JOIN FirstLastCondition flc 
    ON flc.person_id = hosc.person_id
WHERE po.procedure_date >= flc.first_condition_start_date
  AND po.procedure_date < (flc.last_condition_start_date + INTERVAL '180 days')
GROUP BY hbp.procedure_concept_id, hbp.concept_name, hbp.procedure_category, hbp.procedure_count
ORDER BY hbp.procedure_count DESC;
"""

QUERY_FETCH_PROCEDURE_PLOT2_2 = """
WITH FirstLastCondition AS (
    SELECT
        isi.person_id,
        MIN(isi.condition_start_date) AS first_condition_start_date,
        MAX(isi.condition_start_date) AS last_condition_start_date
    FROM schema_name.inpatient_stroke_ischemic isi
    GROUP BY isi.person_id
)
SELECT 
    ibp.procedure_concept_id, 
    ibp.concept_name, 
    ibp.procedure_category,
    ibp.procedure_count,
    COUNT(DISTINCT iosc.person_id) AS distinct_person_count
FROM schema_name.ischemic_only_stroke_cohort iosc
INNER JOIN omop_cdm_53_pmtx_202203.procedure_occurrence po 
    ON po.person_id = iosc.person_id
INNER JOIN schema_name.ischemic_bucket_procedures ibp 
    ON ibp.procedure_concept_id = po.procedure_concept_id
INNER JOIN FirstLastCondition flc 
    ON flc.person_id = iosc.person_id
WHERE po.procedure_date >= flc.first_condition_start_date
  AND po.procedure_date < (flc.last_condition_start_date + INTERVAL '180 days')
GROUP BY ibp.procedure_concept_id, ibp.concept_name, ibp.procedure_category, ibp.procedure_count
ORDER BY ibp.procedure_count DESC;
"""

QUERY_FETCH_EDA_1="""
SELECT c.concept_name as stroke_type, COUNT (*) as count 
FROM omop_cdm_53_pmtx_202203.condition_occurrence AS co 
JOIN omop_cdm_53_pmtx_202203.concept AS c ON co.condition_concept_id = c.concept_id 
WHERE c.concept_name LIKE '%stroke%' 
AND c.domain_id = 'Condition' 
AND c.concept_name NOT LIKE '%heat stroke%' 
AND c.concept_name NOT LIKE '%heatstroke%' 
AND c.concept_name NOT LIKE '%sun stroke%' 
GROUP BY c.concept_name 
ORDER BY count DESC;

"""


QUERY_FETCH_EDA_2="""
SELECT c.concept_name as stroke_type, COUNT (*) as count 
FROM omop_cdm_53_pmtx_202203.condition_occurrence AS co 
JOIN omop_cdm_53_pmtx_202203.concept AS c ON co.condition_concept_id = c.concept_id 
WHERE c.concept_id IN (372924,375557,376713,443454,441874,439847,432923) 
GROUP BY c.concept_name 
ORDER BY count DESC;
"""











QUERY_CREATE_HEMMORHAGIC_PROCEDURE_CLASSIFICATION = """
CREATE TABLE schema_name.haemorrhagic_procedure_classification AS
SELECT
   p.procedure_concept_id,                     -- Select procedure concept ID
   c.concept_name,                             -- Select concept name (procedure name)
   COUNT(*) AS procedure_count,                -- Count occurrences of each unique procedure
   CASE
       WHEN LOWER(c.concept_name) LIKE '%diagnosis%' OR LOWER(c.concept_name) LIKE '%diagnostic%' THEN 'Diagnosis'
       ELSE 'Treatment'
   END AS procedure_type                       -- Classify as Diagnosis or Treatment
FROM omop_cdm_53_pmtx_202203.procedure_occurrence p
INNER JOIN omop_cdm_53_pmtx_202203.concept c
   ON p.procedure_concept_id = c.concept_id
INNER JOIN (
   SELECT
       hosc.person_id,                             -- Select person_id
       MIN(ish.condition_start_date) AS earliest_start_date,  -- Earliest condition start date
       MAX(ish.condition_start_date) AS latest_start_date    -- Latest condition start date
   FROM  schema_name.inpatient_stroke_haemorrhagic ish
   INNER JOIN schema_name.haemorrhagic_only_stroke_cohort hosc
       ON hosc.person_id = ish.person_id            -- Join with haemorrhagic only cohort
   GROUP BY hosc.person_id                        -- Group by person_id
) AS date_ranges
   ON p.person_id = date_ranges.person_id         -- Join procedures to date ranges
WHERE
   p.procedure_date >= date_ranges.earliest_start_date                  -- Procedure after earliest condition start date
   AND p.procedure_date <= date_ranges.latest_start_date + INTERVAL '180 days'  -- Within 180 days of latest condition start date
GROUP BY
   p.procedure_concept_id,                        -- Group by procedure concept ID
   c.concept_name                                 -- Group by concept name
ORDER BY
   procedure_count DESC;                          -- Order by count in descending order
"""

QUERY_CREATE_ISCHEMIC_PROCEDURES_CLASSIFICATION = """
CREATE TABLE schema_name.ischemic_procedure_classification AS
SELECT
   p.procedure_concept_id,                     -- Select procedure concept ID
   c.concept_name,                             -- Select concept name (procedure name)
   COUNT(*) AS procedure_count,                -- Count occurrences of each unique procedure
   CASE
       WHEN LOWER(c.concept_name) LIKE '%diagnosis%' OR LOWER(c.concept_name) LIKE '%diagnostic%' THEN 'Diagnosis'
       ELSE 'Treatment'
   END AS procedure_type                       -- Classify as Diagnosis or Treatment
FROM omop_cdm_53_pmtx_202203.procedure_occurrence p
INNER JOIN omop_cdm_53_pmtx_202203.concept c
   ON p.procedure_concept_id = c.concept_id
INNER JOIN (
   SELECT
       iosc.person_id,                             -- Select person_id
       MIN(isi.condition_start_date) AS earliest_start_date,  -- Earliest condition start date
       MAX(isi.condition_start_date) AS latest_start_date    -- Latest condition start date
   FROM schema_name.inpatient_stroke_ischemic isi
   INNER JOIN schema_name.ischemic_only_stroke_cohort iosc
       ON iosc.person_id = isi.person_id            -- Join with ischemic only cohort
   GROUP BY iosc.person_id                        -- Group by person_id
) AS date_ranges
   ON p.person_id = date_ranges.person_id         -- Join procedures to date ranges
WHERE
   p.procedure_date >= date_ranges.earliest_start_date                  -- Procedure after earliest condition start date
   AND p.procedure_date <= date_ranges.latest_start_date + INTERVAL '180 days'  -- Within 180 days of latest condition start date
GROUP BY
   p.procedure_concept_id,                        -- Group by procedure concept ID
   c.concept_name                                 -- Group by concept name
ORDER BY
   procedure_count DESC;                          -- Order by count in descending order
"""

QUERY_CREATE_HEMMORHAGIC_PROCEDURE_REHAB= """
CREATE TABLE schema_name.haemorrhagic_procedure_rehab AS
SELECT *
FROM schema_name.haemorrhagic_procedure_classification
WHERE LOWER(concept_name) LIKE '%therapy%'
  OR LOWER(concept_name) LIKE '%speech%'
  OR LOWER(concept_name) LIKE '%exercise%'
  OR LOWER(concept_name) LIKE '%skill%'
  OR LOWER(concept_name) LIKE '%physical%'
  OR LOWER(concept_name) LIKE '%occupational%'
  OR LOWER(concept_name) LIKE '%rehabilitation%'
  OR LOWER(concept_name) LIKE '%recovery%'
  OR LOWER(concept_name) LIKE '%motor%'
  OR LOWER(concept_name) LIKE '%neuroplasticity%'
  OR LOWER(concept_name) LIKE '%cognitive%'
  OR LOWER(concept_name) LIKE '%movement%'
  OR LOWER(concept_name) LIKE '%functional%'
  OR LOWER(concept_name) LIKE '%balance%'
  OR LOWER(concept_name) LIKE '%coordination%'
  OR LOWER(concept_name) LIKE '%gait%'
  OR LOWER(concept_name) LIKE '%training%'
  OR LOWER(concept_name) LIKE '%hand%'
  OR LOWER(concept_name) LIKE '%sensory%'
  OR LOWER(concept_name) LIKE '%vestibular%'
  OR LOWER(concept_name) LIKE '%strengthening%'
  OR LOWER(concept_name) LIKE '%stretching%'
  OR LOWER(concept_name) LIKE '%aphasia%'
  OR LOWER(concept_name) LIKE '%stroke%'
  OR LOWER(concept_name) LIKE '%mobility%'
  OR LOWER(concept_name) LIKE '%assistive devices%'
  OR LOWER(concept_name) LIKE '%adaptive equipment%'
  AND procedure_type NOT IN ('Diagnosis')
ORDER BY procedure_count DESC;
"""

QUERY_CREATE_ISCHEMIC_PROCEDURE_REHAB= """
CREATE TABLE schema_name.ischemic_procedure_rehab AS
SELECT *
FROM schema_name.ischemic_procedure_classification
WHERE LOWER(concept_name) LIKE '%therapy%'
  OR LOWER(concept_name) LIKE '%speech%'
  OR LOWER(concept_name) LIKE '%exercise%'
  OR LOWER(concept_name) LIKE '%skill%'
  OR LOWER(concept_name) LIKE '%physical%'
  OR LOWER(concept_name) LIKE '%occupational%'
  OR LOWER(concept_name) LIKE '%rehabilitation%'
  OR LOWER(concept_name) LIKE '%recovery%'
  OR LOWER(concept_name) LIKE '%motor%'
  OR LOWER(concept_name) LIKE '%neuroplasticity%'
  OR LOWER(concept_name) LIKE '%cognitive%'
  OR LOWER(concept_name) LIKE '%movement%'
  OR LOWER(concept_name) LIKE '%functional%'
  OR LOWER(concept_name) LIKE '%balance%'
  OR LOWER(concept_name) LIKE '%coordination%'
  OR LOWER(concept_name) LIKE '%gait%'
  OR LOWER(concept_name) LIKE '%training%'
  OR LOWER(concept_name) LIKE '%hand%'
  OR LOWER(concept_name) LIKE '%sensory%'
  OR LOWER(concept_name) LIKE '%vestibular%'
  OR LOWER(concept_name) LIKE '%strengthening%'
  OR LOWER(concept_name) LIKE '%stretching%'
  OR LOWER(concept_name) LIKE '%aphasia%'
  OR LOWER(concept_name) LIKE '%stroke%'
  OR LOWER(concept_name) LIKE '%mobility%'
  OR LOWER(concept_name) LIKE '%assistive devices%'
  OR LOWER(concept_name) LIKE '%adaptive equipment%'
  AND procedure_type NOT IN ('Diagnosis')
ORDER BY procedure_count DESC;
"""

QUERY_CREATE_HEMMORHAGIC_BUCKET_PROCEDURES= """
 CREATE TABLE schema_name.haemorrhagic_bucket_procedures AS
SELECT *,
       CASE
           WHEN hpr.procedure_concept_id IN (2314284,
                                             2314285,
                                             2314290,
                                             4203780,
                                             2314317,
                                             4030218,
                                             2414382,
                                             2314048,
                                             2314311,
                                             2794475,
                                             2794464,
                                             2794460,
                                             2313971,
                                             2314307,
                                             2314306,
                                             46257452,
                                             2794302,
                                             2314305,
                                             2794324,
                                             2794301,
                                             2794303,
                                             40661615,
                                             2794271,
                                             2794080,
                                             2791958,
                                             2794267,
                                             2794274,
                                             2794114,
                                             2796180,
                                             2794111,
                                             2796204,
                                             2786528,
                                             2791724,
                                             2794292,
                                             2788287,
                                             2794289,
                                             40757006,
                                             2796194,
                                             2796192,
                                             2794323,
                                             2796795,
                                             2794126,
                                             2794266,
                                             2794270,
                                             2314143,
                                             2796232,
                                             2791971,
                                             2795985,
                                             2794298,
                                             2314294,
                                             2314287,
                                             2617366,
                                             710051,
                                             710052,
                                             2313972,
                                             42742395,
                                             2314286,
                                             725118,
                                             725119,
                                             2313643,
                                             42742396,
                                             2794471,
                                             2794457,
                                             2794467,
                                             40661971,
                                             40658719,
                                             2794277,
                                             2791967,
                                             2794297,
                                             2794474,
                                             2794321,
                                             2794284,
                                             2794108,
                                             2314312,
                                             2796200,
                                             2794103,
                                             2794468,
                                             2794129,
                                             2794469,
                                             2796206,
                                             2796767,
                                             2796013,
                                             2796187,
                                             2794287,
                                             2796205,
                                             40757109,
                                             2794125,
                                             2794083,
                                             2794107,
                                             2794472,
                                             2796190,
                                             2794090) THEN 'Physical Therapy'
           WHEN hpr.procedure_concept_id IN (42627910,
                                             2721448,
                                             42627998,
                                             2314296,
                                             2794466,
                                             2798568,
                                             2314297,
                                             2314299,
                                             42627954,
                                             42628093,
                                             2314298,
                                             2794708,
                                             2617447,
                                             2794887,
                                             2314320,
                                             2721290,
                                             2314334) THEN 'Occupational Therapy'
           WHEN hpr.procedure_concept_id IN (2313727,
                                             2798608,
                                             44816445,
                                             2313726,
                                             44816444,
                                             2790655,
                                             2313725,
                                             2798574,
                                             2798604,
                                             2790873,
                                             2790897,
                                             2313786,
                                             2313770,
                                             2798587,
                                             2106568,
                                             2111257,
                                             2795777,
                                             2313701,
                                             44816446,
                                             2313702,
                                             2721447,
                                             725120,
                                             2798588,
                                             2790898,
                                             2798607,
                                             2313760,
                                             2790625,
                                             2790634,
                                             2313769,
                                             2211323,
                                             2798581) THEN 'Speech and Language Therapy'
           WHEN hpr.procedure_concept_id IN (43527904,
                                             43527986,
                                             2213548,
                                             2213546,
                                             2213552,
                                             43527989,
                                             2213545,
                                             43527990,
                                             2213562,
                                             44786387,
                                             2213555,
                                             43527991,
                                             2795845,
                                             2795874,
                                             2795677,
                                             2795843,
                                             2795889,
                                             43527905,
                                             2314295,
                                             43527987,
                                             43527988,
                                             2514493,
                                             2100627,
                                             40664776,
                                             2213547,
                                             2514494,
                                             2795855,
                                             2794699,
                                             43527992,
                                             2795682) THEN 'Mental and Psycho Therapy'
           WHEN hpr.procedure_concept_id IN (2211633,
                                             2211635,
                                             4029715,
                                             40756993,
                                             2211856,
                                             2211879,
                                             46257422,
                                             2108983,
                                             2108140,
                                             2111038,
                                             725117,
                                             2617415,
                                             43527932,
                                             43527898,
                                             2106609,
                                             2212071,
                                             927097,
                                             4161415,
                                             2314249,
                                             2212078,
                                             725058,
                                             2106642,
                                             2721430,
                                             46257728,
                                             2786482,
                                             43527899,
                                             2108141,
                                             43527931,
                                             42628483,
                                             2314157,
                                             2108138,
                                             2314158,
                                             2791323,
                                             2111102,
                                             2109637,
                                             2106908) THEN 'Surgical Procedures'
           ELSE 'Others'
       END AS procedure_category
FROM schema_name.haemorrhagic_procedure_rehab hpr;
"""
QUERY_CREATE_ISCHEMIC_BUCKET_PROCEDURES= """
 CREATE TABLE schema_name.ischemic_bucket_procedures AS
SELECT *,
       CASE
           WHEN ipr.procedure_concept_id IN (2314294,
                                             2314287,
                                             2313972,
                                             2617366,
                                             2314299,
                                             725119,
                                             2314286,
                                             2314311,
                                             2794471,
                                             40658719,
                                             40661615,
                                             2794457,
                                             2794467,
                                             2791967,
                                             2794297,
                                             2794302,
                                             2314312,
                                             2794301,
                                             2794108,
                                             2794474,
                                             2794870,
                                             2791958,
                                             2791964,
                                             2794125,
                                             2794298,
                                             2796187,
                                             2796200,
                                             2794272,
                                             2794090,
                                             2794469,
                                             2794080,
                                             2796793,
                                             2796192,
                                             2794129,
                                             2794103,
                                             2791956,
                                             2794098,
                                             2794289,
                                             2795077,
                                             2794109,
                                             2794107,
                                             2794114,
                                             2796190,
                                             2794093,
                                             40756921,
                                             2794287,
                                             2791971,
                                             2794083,
                                             2796206,
                                             2794472,
                                             2794468,
                                             2796195,
                                             2794284,
                                             2794124,
                                             2794270,
                                             2796036,
                                             2794111,
                                             2788084,
                                             2794323,
                                             2794267,
                                             2795985,
                                             2795250,
                                             2796375,
                                             2794092,
                                             2794121,
                                             2795236,
                                             2791724,
                                             2796010,
                                             2794458,
                                             2795232,
                                             2788287,
                                             2794099,
                                             2314284,
                                             2314285,
                                             2314290,
                                             4203780,
                                             2414382,
                                             2313971,
                                             2794475,
                                             2313643,
                                             2314306,
                                             40661971,
                                             2794464,
                                             2794460,
                                             2794277,
                                             2796788,
                                             2794104,
                                             2795995,
                                             2794101,
                                             2794461,
                                             2794072,
                                             2796180,
                                             2791969,
                                             2791160,
                                             2796204,
                                             2795999,
                                             2796037,
                                             2796040,
                                             2796764,
                                             2794126,
                                             2795994,
                                             2796011,
                                             2796231,
                                             2796762,
                                             46257452,
                                             2794271,
                                             2794324,
                                             2794321,
                                             2794303,
                                             2796205,
                                             2794266,
                                             2794274,
                                             2794292) THEN 'Physical Therapy'
           WHEN ipr.procedure_concept_id IN (2314297,
                                             42627954,
                                             42628093,
                                             42627998,
                                             2314298,
                                             2314320,
                                             2794704,
                                             2617231,
                                             2798568,
                                             42627910,
                                             2721448,
                                             2314296,
                                             2795059,
                                             2795063) THEN 'Occupational Therapy'
           WHEN ipr.procedure_concept_id IN (2313701,
                                             44816446,
                                             2313727,
                                             2313702,
                                             2721447,
                                             2313726,
                                             2790898,
                                             2795777,
                                             2313760,
                                             2211323,
                                             2790655,
                                             2798581,
                                             2313770,
                                             2111257,
                                             2795781,
                                             2790897,
                                             2798574,
                                             2790625,
                                             2106568,
                                             2790634,
                                             2313767,
                                             44816445,
                                             2798608,
                                             2798595,
                                             2798585,
                                             2798604,
                                             2798583,
                                             2313786,
                                             2790878,
                                             2798588,
                                             44816444,
                                             2313725,
                                             2313769) THEN 'Speech and Language Therapy'
           WHEN ipr.procedure_concept_id IN (43527905,
                                             710051,
                                             2314295,
                                             710052,
                                             43527987,
                                             43527988,
                                             2213546,
                                             2213552,
                                             725120,
                                             2514494,
                                             2795855,
                                             44786387,
                                             43527991,
                                             2794699,
                                             2795683,
                                             2795678,
                                             2617264,
                                             2795843,
                                             2213555,
                                             2213547,
                                             2795682,
                                             42742381,
                                             40664881,
                                             2798587,
                                             2798607,
                                             2795845,
                                             2795676,
                                             2795680,
                                             2795684,
                                             2795890,
                                             43527992,
                                             2618103,
                                             2795847,
                                             43527986,
                                             43527904,
                                             2213548,
                                             725118,
                                             40664776,
                                             43527990,
                                             2314335,
                                             2795876,
                                             2795889,
                                             2213545,
                                             43527989,
                                             2617265) THEN 'Mental and Psycho Therapy'
           WHEN ipr.procedure_concept_id IN (2211633,
                                             2111102,
                                             40756828,
                                             2721024,
                                             2106241,
                                             2111051,
                                             2212078,
                                             2109637,
                                             725116,
                                             2212066,
                                             2211877,
                                             2106642,
                                             2314157,
                                             46257708,
                                             40756930,
                                             42628064,
                                             42628483,
                                             43527899,
                                             2109893,
                                             46257728,
                                             2106908,
                                             2103013,
                                             2108603,
                                             2111047,
                                             2110100,
                                             2111045,
                                             2108139,
                                             725059,
                                             2791323,
                                             2313796,
                                             2103119,
                                             2617415) THEN 'Surgical Procedures'
           ELSE 'Others'
       END AS procedure_category
FROM schema_name.ischemic_procedure_rehab ipr ;

"""





QUERY_FETCH_ISCHEMIC_ONLY_VISITS = "SELECT * FROM schema_name.ischemic_only_visits;"
QUERY_FETCH_HAEMORRHAGIC_ONLY_VISITS = "SELECT * FROM schema_name.haemorrhagic_only_visits;"
QUERY_FETCH_ISCHEMIC_ONLY_EDA = "SELECT * FROM schema_name.ischemic_only_stroke_cohort;"
QUERY_FETCH_HAEMORRHAGIC_ONLY_EDA="SELECT * FROM schema_name.haemorrhagic_only_stroke_cohort;"

# QUERY_FETCH_HAEMORRHAGIC_ONLY_VISITS = """SELECT 
# person_id, 
# visit_start_date, visit_end_date, visit_concept_id, visit_concept_name, 
# discharge_to_concept_id, discharge_to_concept_name  FROM schema_name.haemorrhagic_only_visits hov;"""

# QUERY_FETCH_ISCHEMIC_ONLY_VISITS = """SELECT 
# person_id, 
# visit_start_date, visit_end_date, visit_concept_id, visit_concept_name, 
# discharge_to_concept_id, discharge_to_concept_name  FROM schema_name.ischemic_only_visits iov;"""


CREATE_TABLE_QUERY_MAP = {
    "inpatient_stroke_haemorrhagic": QUERY_CREATE_INPATIENT_HAEMORRHAGIC_COHORT,
    "haemorrhagic_stroke_cohort": QUERY_CREATE_HAEMORRHAGIC_STROKE_COHORT,
    "inpatient_stroke_ischemic": QUERY_CREATE_INPATIENT_ISCHEMIC_COHORT,
    "ischemic_stroke_cohort": QUERY_CREATE_ISCHEMIC_STROKE_COHORT,
    "common_people_cohort": QUERY_CREATE_COMMON_STROKE_COHORT,
    "haemorrhagic_only_stroke_cohort": QUERY_CREATE_HAEMORRHAGIC_ONLY_COHORT,
    "ischemic_only_stroke_cohort": QUERY_CREATE_ISCHEMIC_ONLY_COHORT,
    "haemorrhagic_only_visits": QUERY_CREATE_HAEMORRHAGIC_ONLY_VISITS,
    "ischemic_only_visits": QUERY_CREATE_ISCHEMIC_ONLY_VISITS,
    "haemorrhagic_procedure_classification": QUERY_CREATE_HEMMORHAGIC_PROCEDURE_CLASSIFICATION,
    "ischemic_procedure_classification": QUERY_CREATE_ISCHEMIC_PROCEDURES_CLASSIFICATION,
    "ischemic_procedure_rehab":QUERY_CREATE_ISCHEMIC_PROCEDURE_REHAB,
    "haemorrhagic_procedure_rehab":QUERY_CREATE_HEMMORHAGIC_PROCEDURE_REHAB,
    "haemorrhagic_bucket_procedures":QUERY_CREATE_HEMMORHAGIC_BUCKET_PROCEDURES,
    "ischemic_bucket_procedures":QUERY_CREATE_ISCHEMIC_BUCKET_PROCEDURES
}