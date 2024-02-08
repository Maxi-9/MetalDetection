import time
from datetime import datetime
import threading
from Sensors.WT901 import WT901
from Sensors.Sqlite_Adapt import *


def speedTest(device: str):
    sensor = WT901(device, baudrate=115200)
    tbName = device.replace("/dev/", "")
    timer = 120
    manager.create_table(tbName)

    time.sleep(1)

    row = sensor.get_data()
    print(sensor.ser.name, "... Started")

    i = 0
    start_time = float(time.time())
    while start_time > (float(time.time()) - timer):
        row = sensor.get_data()
        # Debug: Print data, or save to sql file
        manager.write_row(row, tbName)
        # row.printData()
        i += 1

    # Frames of Data per second
    print(device + ": " + str(i / timer) + " FPS")


now = datetime.now().strftime("%Y-%m-%d_%H-%M-%s")
dbname = f"data/{now}_data.db"
manager = sqliteManager(dbname)

ports = get_wtports()
print("Ports", ports)
threads = []
for port in ports:
    # Create a thread
    thread = threading.Thread(target=speedTest, args=(str(port),), daemon=True)

    # Start the thread
    thread.start()
    threads.append(thread)

# Wait for the thread to finish
for thread in threads:
    thread.join()

manager.stop()
