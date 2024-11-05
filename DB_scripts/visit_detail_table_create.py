import sqlite3
from faker import Faker
import random
 
# Initialize the Faker library
fake = Faker()
 
# Connect to the SQLite database
connection = sqlite3.connect('DB/mydb.db')
cursor = connection.cursor()
 
# SQL command to create the 'visit_detail' table
create_table_query = '''
CREATE TABLE IF NOT EXISTS visit_detail (
    visit_detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER,
    visit_detail_concept_id INTEGER,
    visit_detail_start_date DATE,
    visit_detail_start_datetime DATETIME,
    visit_detail_end_date DATE,
    visit_detail_end_datetime DATETIME,
    visit_detail_type_concept_id INTEGER,
    provider_id INTEGER,
    care_site_id INTEGER,
    visit_detail_source_value VARCHAR(100),
    visit_detail_source_concept_id INTEGER,
    admitted_from_concept_id INTEGER,
    admitted_from_source_value VARCHAR(100),
    discharged_to_source_value VARCHAR(100),
    discharged_to_concept_id INTEGER,
    preceding_visit_detail_id INTEGER,
    parent_visit_detail_id INTEGER,
    visit_occurence_id INTEGER,
    FOREIGN KEY (visit_detail_concept_id) REFERENCES concept (concept_id),
    FOREIGN KEY (visit_detail_type_concept_id) REFERENCES concept (concept_id),
    FOREIGN KEY (visit_detail_source_concept_id) REFERENCES concept (concept_id),
    FOREIGN KEY (admitted_from_concept_id) REFERENCES concept (concept_id),
    FOREIGN KEY (discharged_to_concept_id) REFERENCES concept (concept_id),
    FOREIGN KEY (visit_occurence_id) REFERENCES visit_occurence (visit_occurence_id)
)
'''
 
# Ensure that the table exists before proceeding
cursor.execute(create_table_query)
connection.commit()  # Commit the changes to the database
 
# Function to generate random data for the visit_detail table
def generate_visit_detail_data():
    person_id = random.randint(1, 1000)  # Random person_id
    visit_detail_concept_id = random.randint(1, 100)  # Random concept ID
    visit_detail_start_date = fake.date_this_decade()  # Random start date within this decade
    visit_detail_start_datetime = fake.date_this_decade().strftime('%Y-%m-%d') + ' ' + fake.time()  # Corrected: Convert date to string and concatenate with time
    visit_detail_end_date = fake.date_this_decade()  # Random end date
    visit_detail_end_datetime = fake.date_this_decade().strftime('%Y-%m-%d') + ' ' + fake.time()  # Corrected: Convert date to string and concatenate with time
    visit_detail_type_concept_id = random.randint(1, 100)  # Random visit type concept ID
    provider_id = random.randint(1, 1000)  # Random provider ID
    care_site_id = random.randint(1, 100)  # Random care site ID
    visit_detail_source_value = fake.word()  # Random source value
    visit_detail_source_concept_id = random.randint(1, 100)  # Random source concept ID
    admitted_from_concept_id = random.randint(1, 100)  # Random admitted from concept ID
    admitted_from_source_value = fake.word()  # Random admitted from source value
    discharged_to_source_value = fake.word()  # Random discharged to source value
    discharged_to_concept_id = random.randint(1, 100)  # Random discharged to concept ID
    preceding_visit_detail_id = random.choice([None, random.randint(1, 1000)])  # Random preceding visit or None
    parent_visit_detail_id = random.choice([None, random.randint(1, 1000)])  # Random parent visit or None
    visit_occurence_id = random.randint(1, 1000)  # Random visit occurrence ID
 
    return (
        person_id, visit_detail_concept_id, visit_detail_start_date,
        visit_detail_start_datetime, visit_detail_end_date, visit_detail_end_datetime,
        visit_detail_type_concept_id, provider_id, care_site_id, visit_detail_source_value,
        visit_detail_source_concept_id, admitted_from_concept_id, admitted_from_source_value,
        discharged_to_source_value, discharged_to_concept_id, preceding_visit_detail_id,
        parent_visit_detail_id, visit_occurence_id
    )
 
# Insert 100 random rows of data into the visit_detail table
for _ in range(100):
    visit_detail_data = generate_visit_detail_data()
   
    insert_query = '''
    INSERT INTO visit_detail (
        person_id, visit_detail_concept_id, visit_detail_start_date, visit_detail_start_datetime,
        visit_detail_end_date, visit_detail_end_datetime, visit_detail_type_concept_id, provider_id,
        care_site_id, visit_detail_source_value, visit_detail_source_concept_id, admitted_from_concept_id,
        admitted_from_source_value, discharged_to_source_value, discharged_to_concept_id,
        preceding_visit_detail_id, parent_visit_detail_id, visit_occurence_id
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
   
    cursor.execute(insert_query, visit_detail_data)
 
# Commit the changes and close the connection
connection.commit()
connection.close()
 
print("Random data inserted successfully into 'visit_detail' table.")