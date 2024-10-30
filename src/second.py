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

query4 = "SELECT c.concept_name as stroke_type, COUNT (*) as count FROM omop_cdm_53_pmtx_202203.condition_occurrence AS co JOIN omop_cdm_53_pmtx_202203.concept AS c ON co.condition_concept_id = c.concept_id WHERE c.concept_id IN (372924,375557,376713,443454,441874,439847,432923) GROUP BY c.concept_name ORDER BY count DESC;"

df4 = pd.read_sql(query4, conn)

sns.set(style="whitegrid")

# for bar chart
plt.figure(figsize=(12, 6))
sns.barplot(data=df4, x='stroke_type', y='count', palette='Blues_d')
plt.xticks(rotation=45, ha='right')
plt.title("Counts of Different Types of Strokes")
plt.xlabel("Stroke Type")
plt.ylabel("Count")
#plt.tight_layout() 
plt.savefig("second.png", bbox_inches='tight')
plt.show()

cursor.close()
conn.close()