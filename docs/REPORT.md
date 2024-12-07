# Overview
Every 40 seconds, someone in the United States suffers a stroke, with 800,000 new strokes occurring annually. Stroke survivors face significant challenges, including deficits in mobility, cognition, and independence, as well as a fragmented care pathway that hinders optimal rehabilitation outcomes.
This project attempts to explore stroke survivor's treatment pathways using the IQVIA Pharmetrics+ dataset, a large commercial health insurance claims database. The aim is to analyze what kind of care is associated to patients after they have a stroke, particularly ischemic and hemorrhagic.

# Key Findings
We started upon Casey's cohort and further enhanced those cohorts to build specific cohorts for ischemic stroke patients and hemorrhagic stroke patients. We also found out that 3,378 shared symptoms of both the strokes and created a separate cohort for these patients.

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