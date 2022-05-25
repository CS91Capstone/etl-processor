import json
import mysql.connector

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

# FILL TABLES WITH DATA
################################################################
# Establish database connection
mydb = mysql.connector.connect(
  host="test-db.csfyol1ukmqu.us-west-2.rds.amazonaws.com",
  user="capstone",
  password="capstonepassword",
  database="capstone"
)

mycursor = mydb.cursor()

# Create SQL statement and execute
statement = "SELECT campsite_id,campsite_longitude,campsite_latitude FROM Campsites"
mycursor.execute(statement)

# Put results into newTable
newTable = mycursor.fetchall()

# Add data from new table into people table in other database
statement = "INSERT INTO Campsites_Coordinates (campsite_id, campsite_longitude,campsite_latitude) VALUES (%s, %s, %s)"
for row in newTable:
  mycursor.execute(statement, row)
  mydb.commit()
  

####### 
# Create SQL statement and execute
statement = "SELECT campsite_id,campsite_type,type_of_use FROM Campsites"
mycursor.execute(statement)

# Put results into newTable
newTable = mycursor.fetchall()

# Add data from new table into people table in other database
statement = "INSERT INTO Campsites_Type (campsite_id, campsite_type,type_of_use) VALUES (%s, %s, %s)"
for row in newTable:
  mycursor.execute(statement, row)
  mydb.commit()


#######
# Create SQL statement and execute
statement = "SELECT campsite_id,facility_id,campsite_name FROM Campsites"
mycursor.execute(statement)

# Put results into newTable
newTable = mycursor.fetchall()

# Add data from new table into people table in other database
statement = "INSERT INTO Campsites_Name (campsite_id, facility_id, campsite_name) VALUES (%s, %s, %s)"
for row in newTable:
  mycursor.execute(statement, row)
  mydb.commit()


#######
# Create SQL statement and execute
statement = "SELECT campsite_id,campsite_accessible,campsite_reservable FROM Campsites"
mycursor.execute(statement)

# Put results into newTable
newTable = mycursor.fetchall()

# Add data from new table into people table in other database
statement = "INSERT INTO Campsites_Access (campsite_id, campsite_accessible, campsite_reservable) VALUES (%s, %s, %s)"
for row in newTable:
  mycursor.execute(statement, row)
  mydb.commit()
