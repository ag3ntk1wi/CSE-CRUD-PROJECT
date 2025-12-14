import mysql.connector
import requests
import json

# Connect to the MySQL database
conn = mysql.connector.connect(
host="localhost", # Database host (e.g., localhost)
user="root", # Your MySQL username
password="root", # Your MySQL password
database="malatecselec" # Database name
)
# Create a cursor object to interact with the database
cursor = conn.cursor(dictionary=True)

# Execute the SQL query
cursor.execute("SELECT * FROM student")
# Fetch all rows
rows = cursor.fetchall()
# Display raw data from the database
print(rows)

# Convert the MySQL data into a JSON string
json_data = json.dumps({"student": rows}, indent=4)
# Display the JSON output
print(json_data)

# Parse the JSON string back into a Python object
parsed_data = json.loads(json_data)
# Loop through each student and display their info
for student in parsed_data["student"]:
    print("ID:", student["id"])
    print("First Name:", student["last_name"])
    print("Last Name:", student["first_name"])
    print("Middle Name:", student["middle_name"])
    print("Age:", student["age"])
    print("Block:", student["block"])
    print("Year:", student["year"])
    print("Instructor ID:", student["instructor_id"])
    print("Program ID:", student["program_id"])

with open("student.json", "w") as file:
    file.write(json_data)

cursor.close()
conn.close()