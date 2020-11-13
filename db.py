import mysql.connector

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
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        conn.close()
    return sensors

def insertReading(uuid, value=-1):
    try:
        conn = mysql.connector.connect(**config)
        cur = conn.cursor()
        if value == -1:
            cur.execute("INSERT INTO reading (uuid, dt) VALUES (%s, NOW())", (uuid))
        else:
            cur.execute("INSERT INTO reading (uuid, dt, value) VALUES (%s, NOW(), %s)", (uuid, value))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        conn.close()
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
            order by r.dt""")
        for item in cur:
            readings.append(item)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        conn.close()
    return readings

