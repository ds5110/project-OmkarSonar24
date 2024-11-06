import sqlite3
from faker import Faker
import random

# Initialize the Faker library
fake = Faker()

# Connect to the SQLite database
connection = sqlite3.connect('DB/mydb.db')
cursor = connection.cursor()

# SQL command to create the 'condition_occurrence' table
create_table_query = '''
CREATE TABLE IF NOT EXISTS condition_occurrence (
    condition_occurrence_id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER,
    condition_concept_id INTEGER,
    condition_start_date DATE,
    condition_start_datetime DATETIME,
    condition_end_date DATE,
    condition_end_datetime DATETIME,
    condition_type_concept_id INTEGER,
    condition_status_concept_id INTEGER,
    stop_reason VARCHAR(100),
    provider_id INTEGER,
    visit_occurrence_id INTEGER,
    visit_detail_id INTEGER,
    condition_source_value VARCHAR(100),
    condition_source_concept_id INTEGER,
    condition_status_source_value VARCHAR(100),
    FOREIGN KEY (condition_concept_id) REFERENCES concept (concept_id),
    FOREIGN KEY (condition_type_concept_id) REFERENCES concept (concept_id),
    FOREIGN KEY (condition_status_concept_id) REFERENCES concept (concept_id),
    FOREIGN KEY (condition_source_concept_id) REFERENCES concept (concept_id)
)
'''

# Ensure that the table exists before proceeding
cursor.execute(create_table_query)
connection.commit()  # Commit the changes to the database

# Function to generate random data for the condition_occurrence table
def generate_condition_occurrence_data():
    person_id = random.randint(1, 1000)  # Random person_id
    condition_concept_id = random.randint(1, 5000)  # Random condition concept ID
    condition_start_date = fake.date_this_decade()  # Random start date within this decade
    condition_start_datetime = fake.date_this_decade().strftime('%Y-%m-%d') + ' ' + fake.time()  # Corrected: Convert date to string and concatenate with time
    condition_end_date = fake.date_this_decade()  # Random end date
    condition_end_datetime = fake.date_this_decade().strftime('%Y-%m-%d') + ' ' + fake.time()  # Corrected: Convert date to string and concatenate with time
    condition_type_concept_id = random.randint(1, 1000)  # Random condition type concept ID
    condition_status_concept_id = random.randint(1, 1000)  # Random condition status concept ID
    stop_reason = fake.word()  # Random stop reason
    provider_id = random.randint(1, 1000)  # Random provider ID
    visit_occurrence_id = random.randint(1, 1000)  # Random visit occurrence ID
    visit_detail_id = random.randint(1, 10000)  # Random visit detail ID
    condition_source_value = fake.word()  # Random source value
    condition_source_concept_id = random.randint(1, 1000)  # Random source concept ID
    condition_status_source_value = fake.word()  # Random condition status source value

    return (
        person_id, condition_concept_id, condition_start_date, condition_start_datetime,
        condition_end_date, condition_end_datetime, condition_type_concept_id,
        condition_status_concept_id, stop_reason, provider_id, visit_occurrence_id,
        visit_detail_id, condition_source_value, condition_source_concept_id, condition_status_source_value
    )

# Insert 100 random rows of data into the condition_occurrence table
for _ in range(100):
    condition_occurrence_data = generate_condition_occurrence_data()

    insert_query = '''
    INSERT INTO condition_occurrence (
        person_id, condition_concept_id, condition_start_date, condition_start_datetime,
        condition_end_date, condition_end_datetime, condition_type_concept_id,
        condition_status_concept_id, stop_reason, provider_id, visit_occurrence_id,
        visit_detail_id, condition_source_value, condition_source_concept_id, condition_status_source_value
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    cursor.execute(insert_query, condition_occurrence_data)

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Random data inserted successfully into 'condition_occurrence' table.")
