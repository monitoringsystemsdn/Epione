import os
import serial 
import time 
import sqlite3
import hashlib

try:
	sere = serial.Serial( port='/dev/ttyECG',baudrate=115200,timeout=0)
	sere.flushInput()
	print("connected to: " + sere.portstr)

except IOError: # if port is already opened, close it and open it again and print message
	sere.close()
	sere.open()
	print ("ECG port was already open, was closed and opened again!")
	

time.sleep(5)

# connection to the sql db.. fetch name + email_id .. hash library.. pid = hash (name+phone) column -- pid

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


while True:	
	try:
		b = sere.readline().strip()
		#print ('-->',b)
		b = b.decode("utf-8")
		if (b != ""):
			if ('ECG' in b): 
				print (b)
				x,e = b.split()
				print(e)
				var="curl -i -XPOST 'http://172.18.0.2:8086/write?db=patientdata' --data-binary 'ecg name=\"${nm}\",phone=\"${phn}\",x="+e+"'"	
							
				#var="curl -i -XPOST 'http://172.18.0.2:8086/write?db=patientdata' --data-binary 'ecg x="+e+"'"
				#var="curl -i -XPOST 'http://172.18.0.2:8086/write?db=iot' --data-binary '"+dev+" "+loc+"="+mesg+"'"
				print(var)
				os.system(var)			

	except ValueError:
		print("Oops! ValueError: too many values to unpack (expected 2)")
	time.sleep(1) 
       	

sere.close()



