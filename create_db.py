import mysql.connector

mydb = mysql.connector.Connect(
    host = "localhost",
    user = "root",
    password = "M@$ukust2"
)

my_cursor = mydb.cursor()

#my_cursor.execute("CREATE DATABASE Information_Capture")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)