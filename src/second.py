import pandas as pd
import os
import sqlite3  
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to the local SQLite database 
conn = sqlite3.connect('DB/mydb.db')  
cursor = conn.cursor()

# Sample query to fetch data from the local database 
query4 = """
SELECT c.concept_name as stroke_type, COUNT(*) as count 
FROM condition_occurrence AS co 
JOIN concept AS c ON co.condition_concept_id = c.concept_id 
WHERE c.concept_id IN (372924, 375557, 376713, 443454, 441874, 439847, 432923) 
GROUP BY c.concept_name 
ORDER BY count DESC;
"""

# Fetch the data into a pandas DataFrame
df4 = pd.read_sql(query4, conn)

# Set the seaborn style for plotting
sns.set(style="whitegrid")

# Plotting a bar chart
plt.figure(figsize=(12, 6))
sns.barplot(data=df4, x='stroke_type', y='count', palette='Blues_d')
plt.xticks(rotation=45, ha='right')
plt.title("Counts of Different Types of Strokes")
plt.xlabel("Stroke Type")
plt.ylabel("Count")

# Save the plot as a PNG file
plt.savefig("second.png", bbox_inches='tight')

# Show the plot
plt.show()

# Close the cursor and connection
cursor.close()
conn.close()
