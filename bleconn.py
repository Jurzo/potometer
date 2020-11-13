import pygatt
import time
import subprocess

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
                    print("Round:", i, "Failed to read from device: ", sensor)
        i += 1
    adapter.stop()
    return values

def scan():
    subprocess.call("./scanner.sh")
    try:
        f = open("result.txt", "r")
        lines = f.read().strip().split("\n")
        if len(lines) > 1:
            return lines[1:len(lines)]
    except:
        print("unable to open file")
    return []
