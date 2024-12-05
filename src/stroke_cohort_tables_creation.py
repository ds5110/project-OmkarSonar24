import pandas as pd
import sqlite3

# Connect to the local SQLite database
conn = sqlite3.connect('DB/mydb.db')
cursor = conn.cursor()

query1 = """
SELECT * from stroke_cohort_ischemic;
"""
d = pd.read_sql(query1, conn)
df1=pd.DataFrame(data=d,columns= ["condition_occurrence_id","person_id","condition_concept_id","condition_start_date","condition_end_date","age","gender_concept_id","condition_descendant_concept_id","observation_start_date","observation_end_date","observation_period_id"])

query2 = """
SELECT * from stroke_cohort_hemorrhagic ;
"""

# Fetch the data into a pandas DataFrame
f = pd.read_sql(query2, conn)

df2=pd.DataFrame(data=f,columns= ["condition_occurrence_id","person_id","condition_concept_id","condition_start_date","condition_end_date","age","gender_concept_id","condition_descendant_concept_id","observation_start_date","observation_end_date","observation_period_id"])

query3 = """
SELECT * from ancestor_decendant_hemorrhagic;
"""

# Fetch the data into a pandas DataFrame
ad = pd.read_sql(query3, conn)

df3=pd.DataFrame(data=ad,columns=["descendant_concept_id","concept_name","domain_id","vocabulary_id","concept_class_id"])

hemorrhagic_descendants = set(df3["descendant_concept_id"])

# Map the condition to 'ischemic' or 'haemmoragic'
df1["stroke_type"] = df1["condition_descendant_concept_id"].apply(
    lambda x: "hemorrhagic" if x in hemorrhagic_descendants else "ischemic"
)

df2["stroke_type"] = df2["condition_descendant_concept_id"].apply(
    lambda x: "hemorrhagic" if x in hemorrhagic_descendants else "ischemic"
)

data = pd.concat([df1, df2], ignore_index=True)

data["gender"] = data["gender_concept_id"].apply(
    lambda x: "male" if x == 8507 else "female"
)
print(data.head())
data['condition_start_date'] = pd.to_datetime(data['condition_start_date'], errors='coerce')
data['condition_end_date'] = pd.to_datetime(data['condition_end_date'], errors='coerce')
data['observation_end_date'] = pd.to_datetime(data['observation_end_date'], errors='coerce')
data['observation_start_date']= pd.to_datetime(data['observation_start_date'], errors='coerce')

data['condition_start_date'] = data['condition_start_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
data['condition_end_date'] = data['condition_end_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
data['observation_end_date'] = data['observation_end_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
data['observation_start_date'] = data['observation_start_date'].dt.strftime('%Y-%m-%d %H:%M:%S')

data = data[data["age"] > 20]
cursor.execute("""
CREATE TABLE IF NOT EXISTS final_stroke_cohort (
    condition_occurrence_id INTEGER,
    person_id INTEGER,
    condition_concept_id INTEGER,
    condition_start_date TEXT,
    condition_end_date TEXT,
    age INTEGER,
    gender_concept_id INTEGER,
    condition_descendant_concept_id INTEGER,
    observation_start_date TEXT,
    observation_end_date TEXT,
    observation_period_id INTEGER,
    stroke_type TEXT,
    gender TEXT
);
""")
conn.commit()

# Insert the data into the 'final_stroke_cohort' table
for row in data.itertuples(index=False, name=None):
    cursor.execute("""
    INSERT INTO final_stroke_cohort (
        condition_occurrence_id, person_id, condition_concept_id, 
        condition_start_date, condition_end_date, age, 
        gender_concept_id, condition_descendant_concept_id, 
        observation_start_date, observation_end_date, observation_period_id, 
        stroke_type, gender
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, row)


conn.commit()


conn.close()

