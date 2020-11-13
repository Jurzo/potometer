import bleconn
import db
import time

while 1:
    availableDevices = bleconn.scan()
    dbSensors = db.getSensors()
    dbDevices = [sensor[0] for sensor in dbSensors]
    matches = [device for device in availableDevices if device in dbDevices]
    for match in matches:
        print(match)
