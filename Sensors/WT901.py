import struct
import time
from datetime import datetime

import serial
from serial.tools import list_ports

from Sensors import Data


class RawWT901(Data.BaseTable):
    """
    Class that just takes the time from the base class and does nothing with it
    """

    @staticmethod
    def create_str(table_name):
        return f"CREATE TABLE {table_name} (d_time TEXT, hex_value TEXT)"

    def add_str(self, table_name):
        return f"INSERT INTO {table_name} (d_time, hex_value) VALUES ('{self.d_time}', '{self.hex_value}')"

    def __init__(self, d_time: str, hex_value: str):
        super().__init__(d_time)
        self.hex_value = hex_value


class WT901:
    # class vars

    @staticmethod
    def get_ports():
        ports = list(list_ports.comports())
        return [p.device for p in ports if "usbserial" or "ttyUSB" in p.device]

    def __init__(self, port, baudrate):
        self.ser = serial.Serial()
        self.name = port.replace("/dev/", "")
        self.port = port

        # Vars
        self.ser.port = port  # '/dev/tty.usbserial-130'
        self.ser.baudrate = baudrate
        self.ser.parity = "N"
        self.ser.bytesize = 8
        self.ser.timeout = 1

        # initialize
        self.initialize_serial()

    # --->
    # ---> Initialize
    # --->

    def initialize_serial(self):
        # Initialize your serial communication
        # This part is needed so that the reading can start reliably.
        self.ser.open()

        time.sleep(1)
        self.ser.reset_input_buffer()

    # --->
    # ---> Serial Processing
    # --->

    def get_raw_data(self) -> RawWT901:
        readData = ""

        while readData != "5551":
            readData = self.ser.read(size=2).hex()

        cur_time = datetime.now()

        while len(readData) != 88:
            readData += self.ser.read(size=2).hex()

        return RawWT901(str(cur_time), readData)

    # --->
    # ---> Other
    # --->
    def flush(self):
        self.ser.flushInput()

    def get_next_data(self) -> RawWT901:
        self.flush()
        return self.get_raw_data()

    @staticmethod
    def convertInt(input_value, num_bits=16):
        """Calculates a two's complement integer from the given input value's bits"""
        mask = 2 ** (num_bits - 1)
        return -(input_value & mask) + (input_value & ~mask)

    @classmethod
    def structure_data(cls, rawData: RawWT901):
        unpacked = struct.unpack(">" + "B" * 44, bytes.fromhex(rawData.hex_value))

        # Now data is a tuple containing all your values, which you can use as needed
        (
            StartAddress_1,
            StartAddress_A,
            AxL,
            AxH,
            AyL,
            AyH,
            AzL,
            AzH,
            TL_A,
            TH_A,
            SUM_A,
            StartAddress_2,
            StartAddress_w,
            wxL,
            wxH,
            wyL,
            wyH,
            wzL,
            wzH,
            TL_w,
            TH_w,
            SUM_w,
            StartAddress_3,
            StartAddress_ypr,
            RollL,
            RollH,
            PitchL,
            PitchH,
            YawL,
            YawH,
            VL,
            VH,
            SUM_ypr,
            StartAddress_4,
            StartAddress_mag,
            HxL,
            HxH,
            HyL,
            HyH,
            HzL,
            HzH,
            TL_mag,
            TH_mag,
            SUM_mag,
        ) = unpacked

        # Acceleration output
        Ax = float(cls.convertInt((AxH << 8) | AxL) / 32768.0 * 16.0)
        Ay = float(cls.convertInt((AyH << 8) | AyL) / 32768.0 * 16.0)
        Az = float(cls.convertInt((AzH << 8) | AzL) / 32768.0 * 16.0)
        # T_A = float(cls.convertInt((TH_A << 8) | TL_A) / 100.0)

        # Angular velocity output
        Wx = float(cls.convertInt((wxH << 8) | wxL) / 32768.0 * 2000.0)
        Wy = float(cls.convertInt((wyH << 8) | wyL) / 32768.0 * 2000.0)
        Wz = float(cls.convertInt((wzH << 8) | wzL) / 32768.0 * 2000.0)
        # T_w = float(cls.convertInt((TH_w << 8) | TL_w) / 100.0)

        # Angle output
        Roll = float(cls.convertInt((RollH << 8) | RollL) / 32768.0 * 180.0)
        Pitch = float(cls.convertInt((PitchH << 8) | PitchL) / 32768.0 * 180.0)
        Yaw = float(cls.convertInt((YawH << 8) | YawL) / 32768.0 * 180.0)

        # Magnetic output
        Hx = float(cls.convertInt(HxH << 8) | HxL)
        Hy = float(cls.convertInt(HyH << 8) | HyL)
        Hz = float(cls.convertInt(HzH << 8) | HzL)
        # T_mag = float(cls.convertInt((TH_mag << 8) | TL_mag) / 100.0)

        d_time = rawData.d_time

        return Data.F9DataFrame(
            Ax, Ay, Az, Wx, Wy, Wz, Roll, Pitch, Yaw, Hx, Hy, Hz, d_time
        )
