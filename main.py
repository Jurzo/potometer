import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
import bleconn
import db
import sheets
import pandas as pd
import time
from waveshare_epd import epd7in5
from Screen import Screen
from Img import ImageCreator
import time as t

logging.basicConfig(level=logging.DEBUG)
logging.info("Pot-o-Meter")

screen = Screen()
img = ImageCreator()

#upload cycle in seconds
uploadCycle = 10

def updateScreen(data):
    img.initiate()
    for y, line in enumerate(data):
        img.write(line[0] + ": " + line[1], 42, (10, y*50))
    screen.draw(img.getImg())

def upload(headers, data):
    sheetDriver = sheets.SheetDriver()
    sheetDriver.createService()
    sheetDriver.clear()
    sheetDriver.addHeaders(headers)
    for i, df in enumerate(data):
        sheetDriver.Export_Data_To_Sheets(df, sheetDriver.colnum_string(i*4+1)+"2:DDD")



def todf(list):
    lastIndex = 0
    current = list[0][0]
    dataframes = []
    for i, datapoint in enumerate(list):
        if (datapoint[0] != current):
            dataframes.append(pd.DataFrame([n[1:] for n in list[lastIndex:i]], columns=["date", "time", "value"]))
            current = datapoint[0]
            lastIndex = i
        if (i == len(list) - 1):
            dataframes.append(pd.DataFrame([n[1:] for n in list[lastIndex:len(list)]], columns=["date", "time", "value"]))
    return dataframes

def checkNewDevices(found, known):
    for device in found:
        if not device['address'] in known:
            print("Adding device", device, "to database")
            db.insertDevice(device['address'], device['name'])


def main():
    updateScreen(db.getLowestReadings())
    upload(db.getNames(), todf(db.getReadings()))
    lastUpload = time.perf_counter_ns()
    while 1:
        foundDevices = bleconn.scanTool()
        foundDevices = [device for device in foundDevices if device['name'] != None]
        myFoundDevices = [device for device in foundDevices if device['name'].split(" ")[0] == "Pot-o-meter"]
        deviceNames = [device['name'] for device in myFoundDevices]
        dbSensors = db.getSensors()
        checkNewDevices(myFoundDevices, [device[1] for device in dbSensors])
        ###matches = [device for device in dbSensors if device[0] in myFoundDevices]
        dbSensors = db.getSensors()
        if myFoundDevices:
            vals = bleconn.readSensors([device for device in dbSensors if device[0] in deviceNames])
            for val in vals:
                print(val)
                db.insertReading(val[0], val[1])

        currentTime = time.perf_counter_ns()
        if currentTime - lastUpload > uploadCycle * 1000000000:
            upload(db.getNames(), todf(db.getReadings()))
            updateScreen(db.getLowestReadings())
            lastUpload = currentTime

if __name__ == '__main__':
    try:
        main()
    except IOError as e:
        logging.info(e)
    
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
    
    finally:
        screen.clear()
        t.sleep(4)
        epd7in5.epdconfig.module_exit()
        exit()
