import sqlite3
from faker import Faker
import random

# Initialize the Faker library
fake = Faker()

# Connect to the SQLite database
connection = sqlite3.connect('DB/mydb.db')
cursor = connection.cursor()

# Ensure the 'visit_occurrence' table exists (assuming it was created in a previous step)
create_table_query = '''
CREATE TABLE IF NOT EXISTS visit_occurrence (
    visit_occurrence_id INTEGER PRIMARY KEY,
    person_id INTEGER,
    visit_concept_id INTEGER,
    visit_start_date DATE,
    visit_start_datetime DATETIME,
    visit_end_date DATE,
    visit_end_datetime DATETIME,
    visit_type_concept_id INTEGER,
    provider_id INTEGER,
    care_site_id INTEGER,
    visit_source_value VARCHAR(100),
    visit_source_concept_id INTEGER,
    admitted_from_concept_id INTEGER,
    admitted_from_source_value VARCHAR(100),
    discharged_to_concept_id INTEGER,
    discharged_to_source_value VARCHAR(100),
    preceding_visit_occurrence_id INTEGER,
    FOREIGN KEY (visit_concept_id) REFERENCES concept (concept_id),
    FOREIGN KEY (visit_type_concept_id) REFERENCES concept (concept_id),
    FOREIGN KEY (visit_source_concept_id) REFERENCES concept (concept_id),
    FOREIGN KEY (admitted_from_concept_id) REFERENCES concept (concept_id),
    FOREIGN KEY (discharged_to_concept_id) REFERENCES concept (concept_id)
)
'''

# Execute the command to create the table
cursor.execute(create_table_query)
connection.commit()

# Function to generate random data for the visit_occurrence table
def generate_visit_occurrence_data():
    person_id = random.randint(1, 1000)
    visit_concept_id = random.randint(1, 100)
    visit_start_date = fake.date_this_decade()
    visit_start_datetime = f"{visit_start_date} {fake.time()}"
    visit_end_date = fake.date_between(start_date=visit_start_date)
    visit_end_datetime = f"{visit_end_date} {fake.time()}"
    visit_type_concept_id = random.randint(1, 100)
    provider_id = random.randint(1, 1000)
    care_site_id = random.randint(1, 100)
    visit_source_value = fake.word()
    visit_source_concept_id = random.randint(1, 100)
    admitted_from_concept_id = random.randint(1, 100)
    admitted_from_source_value = fake.word()
    discharged_to_concept_id = random.randint(1, 100)
    discharged_to_source_value = fake.word()
    preceding_visit_occurrence_id = random.choice([None, random.randint(1, 1000)])

    return (
        person_id, visit_concept_id, visit_start_date, visit_start_datetime,
        visit_end_date, visit_end_datetime, visit_type_concept_id, provider_id,
        care_site_id, visit_source_value, visit_source_concept_id,
        admitted_from_concept_id, admitted_from_source_value,
        discharged_to_concept_id, discharged_to_source_value,
        preceding_visit_occurrence_id
    )

# Insert 100 random rows of data into the visit_occurrence table
for _ in range(100):
    visit_occurrence_data = generate_visit_occurrence_data()
    
    insert_query = '''
    INSERT INTO visit_occurrence (
        person_id, visit_concept_id, visit_start_date, visit_start_datetime,
        visit_end_date, visit_end_datetime, visit_type_concept_id, provider_id,
        care_site_id, visit_source_value, visit_source_concept_id,
        admitted_from_concept_id, admitted_from_source_value,
        discharged_to_concept_id, discharged_to_source_value,
        preceding_visit_occurrence_id
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    
    cursor.execute(insert_query, visit_occurrence_data)

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Random data inserted successfully into 'visit_occurrence' table.")
