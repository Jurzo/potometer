import bleconn
import db
import time
import sheets
import pandas as pd


def upload():
    sheetDriver = sheets.SheetDriver()
    sheetDriver.createService()
    sheetDriver.read()
    if sheetDriver.rows == 0:

        


while 1:
    availableDevices = bleconn.scanTool()
    dbSensors = db.getSensors()
    print(db.getReadings())
    matches = [device for device in dbSensors if device[0] in availableDevices]
    if matches:
        vals = bleconn.readSensors(matches)
        for i in range(len(matches)):
            print(matches[i])
            print(vals[i])
            db.insertReading(matches[i][1], vals[i])
