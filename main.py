import bleconn
import db
import time

while 1:
    availableDevices = bleconn.scan()
    dbDevices = db.getSensors()
    matches = [device for device in availableDevices if device in dbDevices]
    for match in matches:
        print(match)
