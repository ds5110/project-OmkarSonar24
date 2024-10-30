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

query = "select vo.person_id, vo.visit_occurrence_id, c.concept_id, c.concept_name from work_dhande_ak210.visit_detail vo join omop_cdm_53_pmtx_202203.concept c on vo.visit_detail_concept_id =c.concept_id order by vo.visit_occurrence_id ;"
cursor.execute(query)
df = cursor.fetch_dataframe()

sns.histplot(data=df, x='concept_name')
plt.xticks(rotation=90);
plt.xlabel("Types of Patient Visits")
plt.title("Patients Visit Types Distribution")
plt.savefig("patients_visit_type_distribution.jpg", bbox_inches='tight')

cursor.close()
conn.close()