import pygatt
import time

adapter = pygatt.GATTToolBackend()

def readSensors(sensors):
    values = [-1]*len(sensors)
    maxTries = 10
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
                    print("Failed to read from device: ", sensor)
        i += 1
    adapter.stop()
    return values

def scan():
    
