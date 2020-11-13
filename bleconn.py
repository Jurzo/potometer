import pygatt
import time
import db

adapter = pygatt.GATTToolBackend()

def readSensors(sensors):
    values = [-1]*len(sensors)
    maxTries = 1000
    i = 0
    adapter.start()
    while i < maxTries:
        for index, value in enumerate(values):
            if value == -1:
                sensor = sensors[index]
                try:
                    device = adapter.connect(sensor[0])
                    reading = int.from_bytes(device.char_read(sensor[1]), "little")
                    values[index] = reading
                except KeyboardInterrupt:
                    exit()
                except:
                    print("Round:", i, "Failed to read from device: ", sensor)
        i += 1
    adapter.stop()

    return values

print(readSensors(db.getSensors()))
