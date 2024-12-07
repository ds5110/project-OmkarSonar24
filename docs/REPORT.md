# Overview
Every 40 seconds, someone in the United States suffers a stroke, with 800,000 new strokes occurring annually. Stroke survivors face significant challenges, including deficits in mobility, cognition, and independence, as well as a fragmented care pathway that hinders optimal rehabilitation outcomes.
This project attempts to explore stroke survivor's treatment pathways using the IQVIA Pharmetrics+ dataset, a large commercial health insurance claims database. The aim is to analyze what kind of care is associated to patients after they have a stroke, particularly ischemic and hemorrhagic.

## Common Data Model
![OMOP_CDM](../assets/omop_cdm.png) 

The OMOP CDM provides a standardized data  structure for organizing and viewing healthcare data. This makes it easier for researchers to analyze data across different healthcare systems and databases, even if the data originates from various sources or regions with differing formats.

## ERD of the Common Data Model 
![Figure 1](../assets/erd.jpg)

The OMOP CDM consists of several core tables that store data, including:

**Person:** Information about patients (e.g., age, sex, race). <br>
**Observation Period:** The time frames during which data is available for a patient. <br>
**Condition Occurrence:** Data about diseases or conditions diagnosed for a patient. <br>
**Drug Exposure:** Information on the drugs that patients have been prescribed or taken. <br>
**Procedure Occurrence:** Data on procedures or treatments that were performed. <br>
**Measurement:** Observations and laboratory results (e.g., blood pressure, lab test results). <br>
These tables are related by standardized identifiers, ensuring consistency across datasets. <br>

## Creating a cohort
![Cohort Creation Method](../assets/Method_Flowchart.jpg)

We started upon Casey's cohort and further enhanced those cohorts to build specific cohorts for ischemic stroke patients and hemorrhagic stroke patients. We also found out that 3,378 shared symptoms of both the strokes and created a separate cohort for these patients.
We focused on patients having the following concept ids -

| Stroke Type         | Concept ID | Concept Name               | Code               | Vocabulary | Excluded | Descendants |
|---------------------|------------|----------------------------|--------------------|------------|----------|-------------|
| Ischemic Stroke     | 372924     | Cerebral artery occlusion   | 20059004           | SNOMED     | NO       | YES         |
| Ischemic Stroke     | 375557     | Cerebral embolism           | 75543006           | SNOMED     | NO       | YES         |
| Ischemic Stroke     | 443454     | Cerebral infarction         | 432504007          | SNOMED     | NO       | YES         |
| Ischemic Stroke     | 441874     | Cerebral thrombosis         | 71444005           | SNOMED     | NO       | YES         |
| Ischemic Stroke     | 4310996    | Ischemic stroke             | 422504002          | SNOMED     | NO       | YES         |
| Ischemic Stroke     | 45876543   | Transient ischemic attack - TIA | LA14278-8         | SNOMED     | NO       | YES         |
| Ischemic Stroke     | 4319330    | Brain stem ischemia         | 95456009           | SNOMED     | NO       | YES         |
| Haemorrhagic Stroke | 376713     | Cerebral hemorrage          | 274100004          | SNOMED     | NO       | YES         |
| Haemorrhagic Stroke | 439847     | Intracranial hemorrhage     | 1386000            | SNOMED     | NO       | YES         |
| Haemorrhagic Stroke | 432923     | Subarachnoid hemorrage      | 21454007           | SNOMED     | NO       | YES         |
| Haemorrhagic Stroke | 35609033   | Haemorrhagic stroke         | 1078001000000100   | SNOMED     | NO       | YES         |
| Haemorrhagic Stroke | 4319328    | Brain stem hemorrhage       | 95454007           | SNOMED     | NO       | YES         |

After discussion with our stakeholder, we decide to not pursue cryptogenic stroke and brain stem stroke. Once we had the finalized concept ids, we included all their descendant concepts and focused on kinds of visits of the patients, particularly - 
| Concept ID | Concept Name               | Code               | Vocabulary | Excluded | Descendants |
|------------|----------------------------|--------------------|------------|----------|-------------|
| 262     | Emergency Room and Inpatient Visit   | 20059004           | Visit     | NO       | YES         |
| 9203     | Emergency Room Visit   | 20059004           | Visit     | NO       | YES         |
| 9201     | Inpatient Visit   | 20059004           | Visit     | NO       | YES         |


# Key Findings

We analyzed transitions across treatment locations such as inpatient rehabilitation and emergency room visits.
We also identified patterns of care for stroke subtypes, such as Ischemic and Hemorrhagic strokes.

Stroke care transitions are a critical area for improving patient outcomes, yet gaps in data and understanding make it challenging to optimize care. By refining the original project scope to focus on specific pathways and treatment types, this analysis provides insights that can inform rehabilitation protocols.

![age_distribution_by_stroke_type](figs/age_distribution_by_stroke_type.png)
There is a direct relationship between age and stroke risk; as people age, they become more susceptible to experiencing strokes.

## Challenges and Lessons Learned
1. Data Limitations:
Insurance Claims data lacks direct measures of patient outcomes like mortality rates, recurrence of strokes, or quality of life improvements.
Data irregularities posed challenges in creating standardized comparisons and finalizing conclusions.
2. Time Constraints:
The compressed project timeline limited the extent of data exploration.
Considering the size of the database, large, interconnected tables required significant time for querying and analysis.
3. Scope Refinement:
Shifting focus from broad care transitions to analyzing specific treatment pathways related to different kinds of therapies, allowed for actionable insights.



# Conclusion
This project represents an initial foray into analyzing healthcare claims data to better understand stroke survivor care. The findings shed light on the treatment journeys of stroke survivors, laying the groundwork for further exploration. Future work could incorporate machine learning techniques to classify pathways and identify key factors driving differences in outcomes.