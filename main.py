import bleconn
import db
import sheets
import pandas as pd
import time

#upload cycle in seconds
uploadCycle = 600

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

def main():
    upload(db.getNames(), todf(db.getReadings()))
    lastUpload = time.perf_counter_ns()
    while 1:
        availableDevices = bleconn.scanTool()
        dbSensors = db.getSensors()
        readings = db.getReadings()
        matches = [device for device in dbSensors if device[0] in availableDevices]
        if matches:
            vals = bleconn.readSensors(matches)
            for i in range(len(matches)):
                print(matches[i])
                print(vals[i])
                db.insertReading(matches[i][1], vals[i])

        currentTime = time.perf_counter_ns()
        if currentTime - lastUpload > uploadCycle * 1000000000:
            upload(db.getNames(), todf(db.getReadings()))
            lastUpload = currentTime

if __name__ == '__main__':
    main()
