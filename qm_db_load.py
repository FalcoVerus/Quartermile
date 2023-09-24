import mysql.connector as mysql
import csv
import os

#Creating lists
qm_list = list()
file_list = list()

#Connecting to the DB
qmdb = mysql.connect(
  host="localhost",
  user="falco",
  password="Falco@1",
  database="qm"
)
qmcursor = qmdb.cursor()

#Reading in the files
file_list = [os.path.abspath(os.path.join('.\\qm_csv_files', f)) for f in os.listdir(path='.\\qm_csv_files')]

#Optional table re-creation
qmcursor.execute("DROP TABLE car_data")
qmcursor.execute("CREATE TABLE car_data (id INT AUTO_INCREMENT PRIMARY KEY, brand VARCHAR(255), model VARCHAR(255), spec VARCHAR(255), accel VARCHAR(255), et VARCHAR(255))")


#Filling up a list from the files
for file in file_list:
  with open(file) as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
      if len(row) == 4:
        row.append(row[3]) 
        row[3] = 'not know'
      elif row[0] == 'Brand': pass
      elif row[4] == '': qm_list.append({'Brand':row[0], 'Model':row[1], 'Spec':row[2], '0-100':'not know', 'ET':row[3]})
      else: qm_list.append({'Brand':row[0], 'Model':row[1], 'Spec':row[2], '0-100':row[3], 'ET':row[4]})
      
#Filling up the table
for item in qm_list:
  #sql = "INSERT INTO car_data(brand, model, spec, accel, et) VALUES (?, ?, ?, ?, ?)"
  sql = "INSERT INTO car_data(brand, model, spec, accel, et) VALUES (%s, %s, %s, %s, %s)"
  val = item['Brand'], item['Model'], item['Spec'], item['0-100'], item['ET']
  qmcursor.execute(sql, val)
qmdb.commit()

#qmresult = qmcursor.fetchall()

#for x in qmresult:
 #   print(x)
