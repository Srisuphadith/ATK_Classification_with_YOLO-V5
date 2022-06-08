import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="ATK_management"

)
#print(mydb)
mycursor = mydb.cursor()

sql = "INSERT INTO image_src (student_id,image) VALUES (%s, %s)"
val = (f"{username}", "Srisuphadith")
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")