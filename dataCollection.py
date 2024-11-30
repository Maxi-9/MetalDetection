import time
from datetime import datetime
import threading
from typing import Optional

from Sensors import Data
from Sensors.RT3100 import RT3100
from Sensors.WT901 import WT901, RawWT901
from Sensors.Sqlite_Adapt import *


# Has purpose of collecting data, while being able to start, stop and pause data collection
# Also only meant to have one instance at a time
class DataCollector:
    def __init__(self):
        self.threadStarted = None
        self.dbname = ""
        self.threads = None
        self.manager = None
        self.isCollecting = False
        self.isPaused = False

    def collect_RT3100(self, addr: int, port: str = "/dev/i2c-1"):
        sensor = RT3100(port, addr=addr)
        tbName = sensor.name

        self.manager.write_data(Data.MagDataFrame.create_str(tbName), tbName)

        time.sleep(1)

        print(sensor.port, "... RT3100 Started")

        while self.isCollecting:
            if self.isPaused:
                time.sleep(0.1)
                continue
            raw_row = sensor.get_next_data()
            self.manager.write_data(raw_row.add_str(tbName), tbName)

    def collect_WT901(self, device: str):
        sensor = WT901(device, baudrate=115200)
        tbName = sensor.name

        self.manager.write_data(RawWT901.create_str(tbName), tbName)

        time.sleep(1)
        raw_row = sensor.get_raw_data()
        print(sensor.port, "... WT901 Started")

        while self.isCollecting:
            if self.isPaused:
                time.sleep(0.1)
                continue
            raw_row = sensor.get_next_data()
            # Debug: Print data, or save to sql file
            self.manager.write_data(raw_row.add_str(tbName), tbName)

            # row.printData()

    def startDataCollect(self):
        self.manager.write_data(Data.Marker.create_str("marker"), "marker")

        if self.isCollecting:
            raise Exception("Already Running")

        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.dbname = f"../data/{now}_data.db"
        self.manager = sqliteManager(self.dbname)

        self.isCollecting = True
        self.isPaused = False

        ports = WT901.get_ports()
        print("Ports", ports)
        self.threads = []

        for port in ports:
            # Create a thread
            thread = threading.Thread(
                target=self.collect_WT901, args=(str(port),), daemon=True
            )

            # Start the thread
            thread.start()
            self.threads.append(thread)

        # Start RT3100 sensors:
        # ... (rest of the function remains unchanged)

        ports = RT3100.get_ports()
        print("I2C Ports", ports)

        for port in ports:
            # Create a thread
            thread = threading.Thread(
                target=self.collect_RT3100,
                args=(port,),
                daemon=True,
            )

            # Start the thread
            thread.start()
            self.threads.append(thread)

        self.threadStarted = time.perf_counter()

    def stopDataCollect(self):
        if not self.isCollecting:
            raise Exception("Data Not collecting")

        self.isCollecting = False
        self.isPaused = False

        # Wait for the thread to finish
        for thread in self.threads:
            thread.join()

        self.manager.stop()

        self.threads = None
        self.manager = None
        self.isCollecting = False
        self.isPaused = False

    def pauseDataCollect(self):
        if not self.isCollecting:
            raise Exception("Data Not collecting")

        if self.isPaused:
            raise Exception("Already Paused")

        self.isPaused = True

    def unpauseDataCollect(self):
        if not self.isCollecting:
            raise Exception("Data Not collecting")

        if not self.isPaused:
            raise Exception("Already Unpaused")

        self.isPaused = False

    def makeMarker(self, m_time: str):
        marker = Data.Marker(m_time)
        # self.manager.write_data(marker.add_str("marker"), "marker")
