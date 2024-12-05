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
QUERY_FETCH_ISCHEMIC_ONLY_VISITS = "SELECT * FROM ischemic_only_visits;"
QUERY_FETCH_HAEMORRHAGIC_ONLY_VISITS = "SELECT * FROM haemorrhagic_only_visits;"

CREATE_TABLE_QUERY_MAP = {
    "inpatient_stroke_haemorrhagic": QUERY_CREATE_INPATIENT_HAEMORRHAGIC_COHORT,
    "haemorrhagic_stroke_cohort": QUERY_CREATE_HAEMORRHAGIC_STROKE_COHORT,
    "inpatient_stroke_ischemic": QUERY_CREATE_INPATIENT_ISCHEMIC_COHORT,
    "ischemic_stroke_cohort": QUERY_CREATE_ISCHEMIC_STROKE_COHORT,
    "common_people_cohort": QUERY_CREATE_COMMON_STROKE_COHORT,
    "haemorrhagic_only_stroke_cohort": QUERY_CREATE_HAEMORRHAGIC_ONLY_COHORT,
    "ischemic_only_stroke_cohort": QUERY_CREATE_ISCHEMIC_ONLY_COHORT,
    "haemorrhagic_only_visits": QUERY_CREATE_HAEMORRHAGIC_ONLY_VISITS,
    "ischemic_only_visits": QUERY_CREATE_ISCHEMIC_ONLY_VISITS
}