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
        cur.execute("select s.name, s.mac, c.uuid from sensors s join characteristics c on s.mac = c.mac")
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

def insertDevice(mac, name):
    try:
        conn = mysql.connector.connect(**config)
        cur = conn.cursor()
        cur.execute("INSERT INTO sensors (mac, name) VALUES (%s, %s)", (mac, name))
        cur.execute("INSERT INTO characteristics (uuid, mac) VALUES (%s, %s)", ("beb5483e-36e1-4688-b7f5-ea07361b26a8", mac))
        conn.commit()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(err)
    return False

def insertReading(mac, value=-1):
    try:
        conn = mysql.connector.connect(**config)
        cur = conn.cursor()
        cur.execute("INSERT INTO reading (mac, dt, value) VALUES (%s, NOW(), %s)", (mac, value))
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
        cur.execute("""select s.name, date(r.dt), date_format(r.dt, '%H:%i'), r.value, s.mac, c.uuid 
            from sensors s 
            join characteristics c on s.mac = c.mac 
            left join reading r on r.mac = s.mac 
            order by s.name, r.dt desc
            limit 100""")
        for item in cur:
            readings.append([item[0], item[1].strftime("%d/%m/%Y"), item[2], item[3]])

        conn.close()
    except mysql.connector.Error as err:
        print(err)
    return readings

def getCurrentReadings():
    readings = []
    try:
        conn = mysql.connector.connect(**config)
        cur = conn.cursor()
        cur.execute("""select s.name, r.value, r.dt
            from sensors s 
            join reading r on r.mac = s.mac 
            where r.dt in (
                select max(dt) dt
                from reading
                group by mac
            )
            limit 5""")
        for item in cur:
            readings.append([item[0], str(item[1])])

        conn.close()
    except mysql.connector.Error as err:
        print(err)
    return readings
