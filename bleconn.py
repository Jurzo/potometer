import pygatt
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
                    print("connecting to address:", sensor[1])
                    device = adapter.connect(sensor[1])
                    print("reading char:", sensor[2])
                    reading = int.from_bytes('4fafc201-1fb5-459e-8fcc-c5c9c331914b', "little")
                    print('writing char')
                    device.char_write('4fafc201-1fb5-459e-8fcc-c5c9c331914b', bytes(1), wait_for_response=False)
                    print('char written')
                    values[index] = reading
                except KeyboardInterrupt:
                    exit()
                except:
                    print("Round:", i, "Failed to read from device:", sensor)
        i += 1
    adapter.stop()
    return zip([sensor[1] for sensor in sensors], values)

def scan():
    subprocess.call("./scanner.sh")
    try:
        f = open("result.txt", "r")
        lines = f.read().strip().split("\n")
        if len(lines) > 1:
            addrs = []
            for line in lines[1:len(lines)]:
                addrs.append(line.split(" ")[0])
            return addrs
    except:
        print("unable to open file")
    return []

def scanTool():
    try:
        adapter.start()
        addrs = [device for device in adapter.scan()]
        adapter.stop()
        return addrs
    except:
        print("Scan failed")
        return []
