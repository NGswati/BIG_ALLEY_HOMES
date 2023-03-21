import json
import mysql.connector

# Load JSON data from file
with open('agent_details.json', 'r') as f:
    data = json.load(f)

# Connect to MySQL database
connection=mysql.connector.connect(host="localhost",database="big_alley",user="root",password="Nandini@0608",auth_plugin='mysql_native_password')

# Create a cursor object to execute queries
mycursor = connection.cursor()

# Iterate over the data and insert into MySQL table
for item in data:
    sql = "INSERT INTO agent (agent_id,phone,name,report) VALUES (%s, %s, %s,%s)"
    mycursor.execute(sql, (item['Agent ID'],item['Phone'],item['Name'],item['Report']))


# Commit changes to the database
connection.commit()

# Close the cursor and database connection
mycursor.close()
connection.close()

