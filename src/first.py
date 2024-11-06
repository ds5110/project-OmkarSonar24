import pandas as pd
import os
import sqlite3  
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to local SQLite database 
conn = sqlite3.connect('DB/mydb.db')  
cursor = conn.cursor()

# Sample query to fetch data from the local database 
query = """
SELECT c.concept_name as stroke_type, COUNT(*) as count 
FROM condition_occurrence AS co 
JOIN concept AS c ON co.condition_concept_id = c.concept_id 
WHERE c.concept_name LIKE '%stroke%' 
  AND c.domain_id = 'Condition' 
  AND c.concept_name NOT LIKE '%heat stroke%' 
  AND c.concept_name NOT LIKE '%heatstroke%' 
  AND c.concept_name NOT LIKE '%sun stroke%' 
GROUP BY c.concept_name 
ORDER BY count DESC;
"""

# Fetch the data into a pandas DataFrame
df = pd.read_sql(query, conn)

# Set the seaborn style for plotting
sns.set(style="whitegrid")

# Plotting a bar chart
plt.figure(figsize=(12, 6))
sns.barplot(data=df, x='stroke_type', y='count', palette='Blues_d')
plt.xticks(rotation=45, ha='right')
plt.title("Counts of Different Types of Strokes")
plt.xlabel("Stroke Type")
plt.ylabel("Count")
plt.show()

# Close the connection to the database
conn.close()
