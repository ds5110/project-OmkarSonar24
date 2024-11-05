import sqlite3

# Connect to the database (it will be created if it doesn't exist)
connection = sqlite3.connect('DB/mydb.db')

# Create a cursor object to execute SQL commands
cursor = connection.cursor()

# SQL command to create the 'student' table
create_table_query = '''
CREATE TABLE IF NOT EXISTS concept (
    concept_id INT4 primary key,
    concept_name varchar(600),
    domain_id varchar(64),
    vocabulary_id varchar(200),
    concept_class_id varchar(64),
    standard_concept varchar(1),
    concept_code varchar(100),
    valid_start_date date,
    valid_end_date date,
    invalid_reason varchar(1)
)
'''

# Execute the command
cursor.execute(create_table_query)

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Table 'concept' created successfully.")