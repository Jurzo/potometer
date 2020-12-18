import pygatt
import subprocess

def readSensors(sensors):
    adapter = pygatt.GATTToolBackend()
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
                    device = adapter.connect('24:6F:28:9D:B9:16')
                    print("reading char:", sensor[2])
                    reading = int.from_bytes(device.char_read('beb5483e-36e1-4688-b7f5-ea07361b26a8'), "little")
                    print('writing char')
                    device.char_write('beb5483e-36e1-4688-b7f5-ea07361b26a8', bytes(1), wait_for_response=False)
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
    adapter = pygatt.GATTToolBackend()
    try:
        adapter.start()
        addrs = [device for device in adapter.scan()]
        adapter.stop()
        return addrs
    except:
        print("Scan failed")
        return []


if __name__ == '__main__':
    adapter = pygatt.GATTToolBackend()
    adapter.start()
    device = adapter.connect('24:6F:28:9D:B9:16')
    reading = int.from_bytes(device.char_read('beb5483e-36e1-4688-b7f5-ea07361b26a8'), "little")
    print('writing char')
    device.char_write('beb5483e-36e1-4688-b7f5-ea07361b26a8', bytes(1), wait_for_response=False)
    adapter.stop()
