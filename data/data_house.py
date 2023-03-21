import json
import mysql.connector

# Load JSON data from file
with open('addresses.json', 'r') as f:
    data = json.load(f)

# Connect to MySQL database
connection=mysql.connector.connect(host="localhost",database="big_alley",user="root",password="Nandini@0608",auth_plugin='mysql_native_password')

# Create a cursor object to execute queries
mycursor = connection.cursor()

# Iterate over the data and insert into MySQL table
for item in data:
    sql = "INSERT INTO house (house_no,street,city,landmark,pincode,size,year_of_cons,bhk,furnishing,owner) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s,%s)"
    mycursor.execute(sql, (item['House Number'],item['Street'],item['City'],item['Landmark'],item['Pin Code'],item['size'],item['Year of cons'],item['BHK'],item['Furnishing'],item['Owner']))


# Commit changes to the database
connection.commit()

# Close the cursor and database connection
mycursor.close()
connection.close()

