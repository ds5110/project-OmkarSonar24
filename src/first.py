import pandas as pd
import os
import redshift_connector
import matplotlib.pyplot as plt
import seaborn as sns

conn = redshift_connector.connect(
    host='ohdsi-lab-redshift-cluster-prod.clsyktjhufn7.us-east-1.redshift.amazonaws.com',
    database='ohdsi_lab',
    user=os.environ['redshift_user'],
    password=os.environ['redshift_pass']
 )
cursor = conn.cursor()

#print(cursor)

query3 = "SELECT c.concept_name as stroke_type, COUNT (*) as count FROM omop_cdm_53_pmtx_202203.condition_occurrence AS co JOIN omop_cdm_53_pmtx_202203.concept AS c ON co.condition_concept_id = c.concept_id WHERE c.concept_name LIKE '%stroke%' AND c.domain_id = 'Condition' AND c.concept_name NOT LIKE '%heat stroke%' AND c.concept_name NOT LIKE '%heatstroke%' AND c.concept_name NOT LIKE '%sun stroke%' GROUP BY c.concept_name ORDER BY count DESC;"

df3 = pd.read_sql(query3, conn)

sns.set(style="whitegrid")

# for bar chart
plt.figure(figsize=(12, 6))
sns.barplot(data=df3, x='stroke_type', y='count', palette='Blues_d')
plt.xticks(rotation=45, ha='right')
plt.title("Counts of Different Types of Strokes")
plt.xlabel("Stroke Type")
plt.ylabel("Count")
plt.show()