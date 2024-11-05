import sqlite3
from faker import Faker

# Connect to the database (it will be created if it doesn't exist)
connection = sqlite3.connect('DB/mydb.db')

# Create a cursor object to execute SQL commands
cursor = connection.cursor()

# Initialize Faker
fake = Faker()

# SQL command to create the 'concept' table
create_table_query = '''
CREATE TABLE IF NOT EXISTS concept (
    concept_id INTEGER PRIMARY KEY,
    concept_name VARCHAR(600),
    domain_id VARCHAR(64),
    vocabulary_id VARCHAR(200),
    concept_class_id VARCHAR(64),
    standard_concept VARCHAR(1),
    concept_code VARCHAR(100),
    valid_start_date DATE,
    valid_end_date DATE,
    invalid_reason VARCHAR(1)
)
'''

# Execute the command to create the table
cursor.execute(create_table_query)

# Generate and insert 100 records
for _ in range(100):
    concept_id = fake.unique.random_int(min=1, max=1000)
    concept_name = fake.word()  # Generate a single word for concept name
    domain_id = fake.word()
    vocabulary_id = fake.word()
    concept_class_id = fake.word()
    standard_concept = fake.random_element(elements=('Y', 'N'))  # Randomly 'Y' or 'N'
    concept_code = fake.bothify(text='??-####')  # Format example like 'AB-1234'
    valid_start_date = fake.date_this_century()
    valid_end_date = fake.date_between(start_date=valid_start_date)
    invalid_reason = fake.random_element(elements=(None, 'D'))  # Either None or 'D'

    cursor.execute('''
    INSERT INTO concept (concept_id, concept_name, domain_id, vocabulary_id, concept_class_id, standard_concept, concept_code, valid_start_date, valid_end_date, invalid_reason)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (concept_id, concept_name, domain_id, vocabulary_id, concept_class_id, standard_concept, concept_code, valid_start_date, valid_end_date, invalid_reason))

# Commit the changes
connection.commit()

# Verify the insertions by selecting some rows
cursor.execute('SELECT * FROM concept LIMIT 5')
results = cursor.fetchall()

# Close the connection
connection.close()

# Print the results
print("Sample records from the 'concept' table:")
for row in results:
    print(row)
