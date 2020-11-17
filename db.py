import mysql.connector
import pandas as pd
import datetime

config = {
  'user': 'raspi',
  'password': 'raspi',
  'host': '192.168.0.140',
  'port': 3306,
  'database': 'potometer',
  'raise_on_warnings': True
}

def getSensors():
    sensors = []
    try:
        conn = mysql.connector.connect(**config)
        cur = conn.cursor()
        cur.execute("select s.mac, c.uuid from sensors s join characteristics c on s.mac = c.mac")
        for item in cur:
            sensors.append(item)
        
        conn.close()
    except mysql.connector.Error as err:
        print(err)
    return sensors

def getNames():
    names = []
    try:
        conn = mysql.connector.connect(**config)
        cur = conn.cursor()
        cur.execute("select name from sensors")
        for item in cur:
            names.append(item[0])
        
        conn.close()
    except mysql.connector.Error as err:
        print(err)
    return names

def insertReading(uuid, value=-1):
    try:
        conn = mysql.connector.connect(**config)
        cur = conn.cursor()
        if value == -1:
            cur.execute("INSERT INTO reading (uuid, dt) VALUES (%s, NOW())", (uuid))
        else:
            cur.execute("INSERT INTO reading (uuid, dt, value) VALUES (%s, NOW(), %s)", (uuid, value))
        conn.commit()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(err)
    return False

def getReadings():
    readings = []
    try:
        conn = mysql.connector.connect(**config)
        cur = conn.cursor()
        cur.execute("""select s.name, date(r.dt), hour(r.dt), r.value, s.mac, c.uuid 
            from sensors s 
            join characteristics c on s.mac = c.mac 
            left join reading r on r.uuid = c.uuid 
            order by s.name, r.dt desc
            limit 100""")
        for item in cur:
            readings.append([item[0], item[1].strftime("%d/%m/%Y"), item[2], item[3]])

        conn.close()
    except mysql.connector.Error as err:
        print(err)
    return readings

