import os
import serial 
import time 
import sqlite3
import hashlib


try:
	ter0 = serial.Serial( port='/dev/ttyTemp',baudrate=115200,timeout=0)
	ter0.flushInput()
	print("connected to: " + ter0.portstr)

except IOError: # if port is already opened, close it and open it again and print message
	ter0.close()
	ter0.open()
	print ("Temp port was already open, was closed and opened again!")
	
conn = None
current_user_name = None
current_user_phone = None
# establishing connection with sqlite.db  
try:
    conn = sqlite3.connect('/home/pi/Epione/flask_auth/project/db.sqlite')
    print("success")
except Exception as e:
    print(e)
    print("Failed connection")
    
curr = conn.cursor()
curr.execute("SELECT * FROM User")
rows = curr.fetchall()

#hashing the data
for row in rows:
#9 refers to loggedin attribute in the tuple
#1 refers to name and 4 refers to phone number
    if row[9] == 1:
        current_user_name = row[1]
        current_user_phone = row[4]
    
print("Current User Name",current_user_name,"Current User Phone", current_user_phone)

nm = current_user_name
phn = current_user_phone

time.sleep(5)

while True:
	try:	
		b = ter0.readline().strip()
		b = b.decode("utf-8")
		if (b != ""):
			if ('Temp' in b): 
				print (b)
				x,y = b.split()
				t,s = y.split(',')
				print('Temp val: ',t)
				print('Spo2 val: ',s)
				vart="curl -i -XPOST 'http://172.18.0.2:8086/write?db=patientdata' --data-binary 'temp name=\"${nm}\",phone=\"${phn}\",x="+t+"'"
				#vart="curl -i -XPOST 'http://172.18.0.2:8086/write?db=patientdata' --data-binary 'temp x="+t+"'"
				os.system(vart)
				vars="curl -i -XPOST 'http://172.18.0.2:8086/write?db=patientdata' --data-binary 'spo2 name=\"${nm}\",phone=\"${phn}\",x="+s+"'"
				#vars="curl -i -XPOST 'http://172.18.0.2:8086/write?db=patientdata' --data-binary 'spo2 x="+s+"'"
				os.system(vars)


	except ValueError:
		print("Oops! ValueError: too many values to unpack (expected 2)")
	time.sleep(1) 
       	
ter0.close()

