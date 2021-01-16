import os
import serial 
import time 
import sqlite3
import hashlib

ser = serial.Serial( port='/dev/ttyBP',baudrate=9600,timeout=0)
ser.flushInput() 
print("connected to: " + ser.portstr)

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
	
	c = ser.readline().strip()
	#print ('After stripping: ',c)
	c = c.decode("utf-8")
	#print ('-after decoding- ',c)
	time.sleep(1)
	if (c != ""):
		#print ("receiving..")
		print (c)
		s,d,p = c.split(',')
		
		print(s)
		#sys="curl -i -XPOST 'http://172.18.0.2:8086/write?db=patientdata' --data-binary 'systole x="+s+"'"
		sys="curl -i -XPOST 'http://172.18.0.2:8086/write?db=patientdata' --data-binary 'systole name=\"${nm}\",phone=\"${phn}\",x="+s+"'"
		os.system(sys)
		
		print (d)
		#dia="curl -i -XPOST 'http://172.18.0.2:8086/write?db=patientdata' --data-binary 'diastole x="+d+"'"
		dia="curl -i -XPOST 'http://172.18.0.2:8086/write?db=patientdata' --data-binary 'diastole name=\"${nm}\",phone=\"${phn}\",x="+d+"'"
		os.system(dia)
			
		print (p)
		pulse="curl -i -XPOST 'http://172.18.0.2:8086/write?db=patientdata' --data-binary 'pulse name=\"${nm}\",phone=\"${phn}\",x="+p+"'"
		#"curl -i -XPOST 'http://172.18.0.2:8086/write?db=patientdata' --data-binary 'pulse x="+p+"'"
		os.system(pulse)
	else:
		s = '125'
		d = '95'
		p = '72'
		sys="curl -i -XPOST 'http://172.18.0.2:8086/write?db=patientdata' --data-binary 'systole name=\"${nm}\",phone=\"${phn}\",x="+s+"'"
		os.system(sys)
		dia="curl -i -XPOST 'http://172.18.0.2:8086/write?db=patientdata' --data-binary 'diastole name=\"${nm}\",phone=\"${phn}\",x="+d+"'"
		os.system(dia)
		pulse="curl -i -XPOST 'http://172.18.0.2:8086/write?db=patientdata' --data-binary 'pulse name=\"${nm}\",phone=\"${phn}\",x="+p+"'"
		os.system(pulse)		

        	
ser.close()
