class BaseTable:
    @staticmethod
    def create_str(table_name):
        raise NotImplementedError

    def add_str(self, table_name):
        raise NotImplementedError

    def __init__(self, d_time: str):
        self.d_time = d_time


class F9DataFrame(BaseTable):
    """
    Class for 9 degrees of freedom(plus magnetometer) sensor data(but also works for less)
    """

    def create_str(self, table_name):
        return f"CREATE TABLE {table_name} (d_time TEXT, Ax REAL, Ay REAL, Az REAL, Wx REAL, Wy REAL, Wz REAL, Roll REAL, Pitch REAL, Yaw REAL, Hx REAL, Hy REAL, Hz REAL)"

    def add_str(self, table_name):
        return f"INSERT INTO {table_name} (d_time, Ax, Ay, Az, Wx, Wy, Wz, Roll, Pitch, Yaw, Hx, Hy, Hz) VALUES ('{self.d_time}', {self.Ax}, {self.Ay}, {self.Az}, {self.Wx}, {self.Wy}, {self.Wz}, {self.Roll}, {self.Pitch}, {self.Yaw}, {self.Hx}, {self.Hy}, {self.Hz})"

    def __init__(
        self,
        Ax,
        Ay,
        Az,
        Wx,
        Wy,
        Wz,
        Roll,
        Pitch,
        Yaw,
        Hx,
        Hy,
        Hz,
        d_time,
        round_data=3,
    ):
        """
        Create data structure
        :param round: Rounds all the data
        """

        # Acceleration output
        self.Ax = round(Ax, round_data)
        self.Ay = round(Ay, round_data)
        self.Az = round(Az, round_data)

        # Angular velocity output
        self.Wx = round(Wx, round_data)
        self.Wy = round(Wy, round_data)
        self.Wz = round(Wz, round_data)

        # Angle output
        self.Roll = round(Roll, round_data)
        self.Pitch = round(Pitch, round_data)
        self.Yaw = round(Yaw, round_data)

        # Magnetic output
        self.Hx = round(Hx, round_data)
        self.Hy = round(Hy, round_data)
        self.Hz = round(Hz, round_data)

        super().__init__(d_time)


class MagDataFrame(BaseTable):
    """
    Class for only magnetometer sensor data
    """

    @staticmethod
    def create_str(table_name):
        return f"CREATE TABLE {table_name} (d_time TEXT, Hx REAL, Hy REAL, Hz REAL)"

    def add_str(self, table_name):
        return f"INSERT INTO {table_name} (d_time, Hx, Hy, Hz) VALUES ('{self.d_time}', {self.Hx}, {self.Hy}, {self.Hz})"

    def __init__(
        self,
        Hx,
        Hy,
        Hz,
        d_time,
        round_data=3,
    ):
        """
        Create data structure
        :param round: Rounds all the data
        """

        # Magnetic output
        self.Hx = round(Hx, round_data)
        self.Hy = round(Hy, round_data)
        self.Hz = round(Hz, round_data)

        super().__init__(d_time)


class Marker(BaseTable):
    """
    Class that just takes the time from the base class and does nothing with it
    """

    @staticmethod
    def create_str(table_name):
        return f"CREATE TABLE {table_name} (d_time TEXT)"

    def add_str(self, table_name):
        return f"INSERT INTO {table_name} (d_time) VALUES ('{self.d_time}')"

    def __init__(self, d_time):
        super().__init__(d_time)
