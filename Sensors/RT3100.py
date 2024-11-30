from datetime import datetime

from Sensors import Data

import time
import board
import rm3100
import smbus2

from Sensors.Data import MagDataFrame


# for the RT3100 breakout board
class RT3100:
    def __init__(self, port: str, addr: int = 0x20) -> None:
        self.i2c = None
        self.name = f'{port.replace("/dev/", "").replace("-","_")}_{addr}'
        self.port = port
        self.rm = None

        self.initialize_serial(addr=addr)

    def initialize_serial(self, addr: int):
        # Initialize your serial communication
        # This part is needed so that the reading can start reliably.
        self.i2c = board.I2C()
        self.rm = rm3100.RM3100_I2C(self.i2c, i2c_address=addr)
        time.sleep(1)
        self.rm.start_continuous_reading()

    def close(self):
        self.rm.stop()

    def flush(self):
        # DNE
        pass

    def get_next_data(self) -> MagDataFrame:
        time.sleep(self.rm.measurement_time / 1.1)
        self.rm.get_next_reading()
        cur_time = datetime.now()
        reading = self.rm.magnetic
        return MagDataFrame(reading[0], reading[1], reading[2], str(cur_time))

    @classmethod
    def get_ports(cls, i2c_port: int = 1):
        try:
            bus = smbus2.SMBus(i2c_port)
        except OSError:
            return []
        addr_list = []
        for device in range(128):
            try:
                bus.write_quick(device)
                addr_list.append(device)
                # print(f"Device found at address {hex(device)}")

            except OSError:
                pass

        return addr_list
