import pandas as pd
import os
import sqlite3  
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to the local SQLite database 
conn = sqlite3.connect('DB/mydb.db')  
cursor = conn.cursor()

# SQL query to fetch data from the local database
query = """
SELECT vo.person_id, vo.visit_occurrence_id, c.concept_id, c.concept_name
FROM visit_detail vo
JOIN concept c ON vo.visit_detail_concept_id = c.concept_id
ORDER BY vo.visit_occurrence_id;
"""

# Execute the query and fetch data into a pandas DataFrame
df = pd.read_sql(query, conn)

# Set up the seaborn style for plotting
sns.set(style="whitegrid")

# Plotting a histogram for the distribution of 'concept_name'
plt.figure(figsize=(12, 6))
sns.histplot(data=df, x='concept_name', kde=False, bins=20)
plt.xticks(rotation=90)
plt.xlabel("Types of Patient Visits")
plt.title("Patients Visit Types Distribution")

# Save the plot as a JPG file
plt.savefig("patients_visit_type_distribution.jpg", bbox_inches='tight')

# Show the plot
plt.show()

# Close the cursor and connection
cursor.close()
conn.close()
