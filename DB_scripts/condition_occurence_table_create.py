import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize the Faker library
fake = Faker()

# Connect to the SQLite database
connection = sqlite3.connect('DB/mydb.db')
cursor = connection.cursor()

# 1. Create the condition_occurrence table
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

cursor.execute(create_table_query)
print("Table 'condition_occurrence' created successfully.")

# 2. Insert random data into the 'condition_occurrence' table
def generate_random_data(num_records=100):
    # Get the current date to generate dates within a range
    current_date = datetime.now()

    for _ in range(num_records):
        person_id = random.randint(1, 1000)  # Assuming person IDs range from 1 to 1000
        condition_concept_id = random.randint(1, 5000)  # Random condition concept ID
        condition_type_concept_id = random.randint(1, 1000)  # Random type concept ID
        condition_status_concept_id = random.randint(1, 1000)  # Random status concept ID
        stop_reason = fake.word()  # Random stop reason
        provider_id = random.randint(1, 100)  # Random provider ID
        visit_occurrence_id = random.randint(1, 1000)  # Random visit occurrence ID
        visit_detail_id = random.randint(1, 10000)  # Random visit detail ID
        condition_source_value = fake.word()  # Random source value
        condition_source_concept_id = random.randint(1, 1000)  # Random source concept ID
        condition_status_source_value = fake.word()  # Random status source value

        # Generate random condition start and end dates/times
        condition_start_date = fake.date_this_decade()
        condition_start_datetime = fake.date_this_decade() + " " + fake.time()
        condition_end_date = fake.date_this_decade()
        condition_end_datetime = fake.date_this_decade() + " " + fake.time()

        # Insert the data into the 'condition_occurrence' table
        insert_query = '''
        INSERT INTO condition_occurrence (
            person_id, condition_concept_id, condition_start_date, 
            condition_start_datetime, condition_end_date, 
            condition_end_datetime, condition_type_concept_id, 
            condition_status_concept_id, stop_reason, provider_id, 
            visit_occurrence_id, visit_detail_id, condition_source_value, 
            condition_source_concept_id, condition_status_source_value
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        cursor.execute(insert_query, (
            person_id, condition_concept_id, condition_start_date, 
            condition_start_datetime, condition_end_date, 
            condition_end_datetime, condition_type_concept_id, 
            condition_status_concept_id, stop_reason, provider_id, 
            visit_occurrence_id, visit_detail_id, condition_source_value, 
            condition_source_concept_id, condition_status_source_value
        ))

    # Commit the changes to the database
    connection.commit()

# Call the function to generate 100 random records
generate_random_data(100)

# Close the connection to the database
connection.close()

print("Random data inserted successfully into 'condition_occurrence'.")
