import bleconn
import db
import time

while 1:
    availableDevices = bleconn.scan()
    dbSensors = db.getSensors()
    matches = [device for device in dbSensors if device[0] in availableDevices]
    for match in matches:
        print(match)
