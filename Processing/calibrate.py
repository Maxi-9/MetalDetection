import math
import sqlite3

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from numpy.linalg import inv, eig
import pickle

import plotly.graph_objects as go


def format_df_time_ms(data_frames: list):
    for df in data_frames:
        df["d_time"] = (
            pd.to_datetime(df.index, format="%Y-%m-%d %H:%M:%S.%f").astype(int)
            // 10**6
        )
        df.set_index("d_time", inplace=True)


def cut_off_extra(data_fras: list, cut_start: int = 0, cut_end: int = 0):
    # Convert the index of each DataFrame from Unix time in milliseconds to datetime64
    for df in data_fras:
        df.index = pd.to_datetime(df.index, unit="ms")

    # Calculate the start and end times for cutting
    start_time = min(df.index.min() for df in data_fras) + pd.Timedelta(
        seconds=cut_start
    )
    end_time = max(df.index.max() for df in data_fras) - pd.Timedelta(seconds=cut_end)

    # Drop the rows outside the specified start and end times
    for df in data_fras:
        df.drop(df[df.index < start_time].index, inplace=True)
        df.drop(df[df.index > end_time].index, inplace=True)


def resample(data_frames: list, target_frequency: int = 50):
    for i, df in enumerate(data_frames):
        # df.index = pd.to_datetime(df.index, unit="ms")
        df.index = pd.to_datetime(df.index, format="%Y-%m-%d %H:%M:%S.%f")
        df = (
            df.resample(f"{int(1000/target_frequency)}L")
            .mean()
            .interpolate(method="time")
        )
        data_frames[i] = df


def calibrate(list_df, Fix_cal=True):
    # Pre calculated
    mag_calibration1 = [-3.5589472772441937+1.15, -4.718578808193119+2.5, -3.42343196960233-1]
    mag_calibration2 = [-3.412272238517975, 1.1391331660352293, 0.36322967417460106]
    mag_calibration3 = [-1.351673306603324, 2.8039616258067923-2.85, 0.8569762535837135-0.5]
    """
    mag_calibration1 = [-3.5589472772441937, -4.718578808193119, -3.42343196960233]
    mag_calibration2 = [-3.412272238517975, 1.1391331660352293, 0.36322967417460106]
    mag_calibration3 = [-1.351673306603324, 2.8039616258067923, 0.8569762535837135]
    """
    s1x = 0.9731
    s1y = 0.9663
    s1z = 0.9746
    s2x = 0.9788
    s2y = 1.0132
    s2z = 1.0474
    s3x = 1.0249
    s3y = 1.0234
    s3z = 0.9983
    avs = 1

    mag_x1 = list_df[0]["Hx"].to_numpy()
    mag_y1 = list_df[0]["Hy"].to_numpy()
    mag_z1 = list_df[0]["Hz"].to_numpy()

    mag_x2 = list_df[1]["Hx"].to_numpy()
    mag_y2 = list_df[1]["Hy"].to_numpy()
    mag_z2 = list_df[1]["Hz"].to_numpy()

    mag_x3 = list_df[2]["Hx"].to_numpy()
    mag_y3 = list_df[2]["Hy"].to_numpy()
    mag_z3 = list_df[2]["Hz"].to_numpy()

    # Sensor 1
    min_x = min(mag_x1)
    max_x = max(mag_x1)
    min_y = min(mag_y1)
    max_y = max(mag_y1)
    min_z = min(mag_z1)
    max_z = max(mag_z1)

    if not Fix_cal:
        s1x = (max_x - min_x) / 2
        s1y = (max_y - min_y) / 2
        s1z = (max_z - min_z) / 2
        mag_calibration1 = [
            (max_x + min_x) / 2,
            (max_y + min_y) / 2,
            (max_z + min_z) / 2,
        ]
    print("1 Final calibration in uTesla:", mag_calibration1)

    # Sensor 2
    min_x = min(mag_x2)
    max_x = max(mag_x2)
    min_y = min(mag_y2)
    max_y = max(mag_y2)
    min_z = min(mag_z2)
    max_z = max(mag_z2)

    if not Fix_cal:
        s2x = (max_x - min_x) / 2
        s2y = (max_y - min_y) / 2
        s2z = (max_z - min_z) / 2
        mag_calibration2 = [
            (max_x + min_x) / 2,
            (max_y + min_y) / 2,
            (max_z + min_z) / 2,
        ]
    print("2 Final calibration in uTesla:", mag_calibration2)

    # Sensor 3
    min_x = min(mag_x3)
    max_x = max(mag_x3)
    min_y = min(mag_y3)
    max_y = max(mag_y3)
    min_z = min(mag_z3)
    max_z = max(mag_z3)

    if not Fix_cal:
        s3x = (max_x - min_x) / 2
        s3y = (max_y - min_y) / 2
        s3z = (max_z - min_z) / 2
        mag_calibration3 = [
            (max_x + min_x) / 2,
            (max_y + min_y) / 2,
            (max_z + min_z) / 2,
        ]
        avs = (s1x + s1y + s1z + s2x + s2y + s2z + s3x + s3y + s3z) / 9
    print("3 Final calibration in uTesla:", mag_calibration3)

    print("Average reading", avs)

    cal_mag_x1 = np.add([avs / s1x * (x - mag_calibration1[0]) for x in mag_x1], 1)
    cal_mag_y1 = [avs / s1y * (y - mag_calibration1[1]) for y in mag_y1]
    cal_mag_z1 = [avs / s1z * (z - mag_calibration1[2]) for z in mag_z1]

    cal_mag_x2 = [avs / s2x * (x - mag_calibration2[0]) for x in mag_x2]
    cal_mag_y2 = [avs / s2y * (y - mag_calibration2[1]) for y in mag_y2]
    cal_mag_z2 = [avs / s2z * (z - mag_calibration2[2]) for z in mag_z2]

    cal_mag_x3 = [avs / s3x * (x - mag_calibration3[0]) for x in mag_x3]
    cal_mag_y3 = np.add([avs / s3y * (y - mag_calibration3[1]) for y in mag_y3], -0.86)
    cal_mag_z3 = [avs / s3z * (z - mag_calibration3[2]) for z in mag_z3]

    cal_mag1 = [
        math.sqrt(cal_mag_x1[i] ** 2 + cal_mag_y1[i] ** 2 + cal_mag_z1[i] ** 2)
        for i in range(len(cal_mag_x1))
    ]
    cal_mag2 = [
        math.sqrt(cal_mag_x2[i] ** 2 + cal_mag_y2[i] ** 2 + cal_mag_z2[i] ** 2)
        for i in range(len(cal_mag_x2))
    ]
    cal_mag3 = [
        math.sqrt(cal_mag_x3[i] ** 2 + cal_mag_y3[i] ** 2 + cal_mag_z3[i] ** 2)
        for i in range(len(cal_mag_x3))
    ]

    list_df[0]["Hx"] = cal_mag_x1
    list_df[0]["Hy"] = cal_mag_y1
    list_df[0]["Hz"] = cal_mag_z1

    list_df[1]["Hx"] = cal_mag_x2
    list_df[1]["Hy"] = cal_mag_y2
    list_df[1]["Hz"] = cal_mag_z2

    list_df[2]["Hx"] = cal_mag_x3
    list_df[2]["Hy"] = cal_mag_y3
    list_df[2]["Hz"] = cal_mag_z3

    # Assuming the dataframe has a column for cal_mag1, cal_mag2, and cal_mag3
    list_df[0]["Magn"] = cal_mag1
    list_df[1]["Magn"] = cal_mag2
    list_df[2]["Magn"] = cal_mag3


def plot_3d(data_frames: list):
    for df in data_frames:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

        ax.scatter(df["Hx"], df["Hy"], df["Hz"])

        ax.set_xlabel("Hx")
        ax.set_ylabel("Hy")
        ax.set_zlabel("Hz")

        plt.show()


def plot_df(data_frames: list, colors: dict):
    fig = go.Figure()
    for i, df in enumerate(data_frames):
        for col, color in colors.items():
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df[col],
                    mode="lines",
                    name=f"{col}_df{i+1}",
                    line=dict(color=color),
                )
            )

    fig.show()


def scale_df(df, scale_val=46.933):
    # Calculate the current magnitude
    average_magnitude = np.sqrt(df["Hx"] ** 2 + df["Hy"] ** 2 + df["Hz"] ** 2).mean()

    # Calculate the scaling factor
    scaling_factor = scale_val / average_magnitude
    print(scaling_factor)
    return scaling_factor


def main(conn: sqlite3.Connection):
    data_frames = []  # Create an empty list to store the DataFrames
    for table_name in table_names:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        df.set_index("d_time", inplace=True)
        data_frames.append(df)

    resample(data_frames)
    format_df_time_ms(data_frames)

    cut_off_extra(data_frames)
    plot_3d(data_frames)

    # Fit here
    save_calibration(data_frames, "ellipsoid_params.pkl")

    calibration_data = load_calibrations("ellipsoid_params.pkl")
    for i, (df, (center, axes, R)) in enumerate(zip(data_frames, calibration_data)):
        data_frames[i] = apply_fit_to_data(df, center, axes, R)

    print(data_frames)
    plot_3d(data_frames)
    plot_df(data_frames, colors={"Hx": "red", "Hy": "green", "Hz": "blue"})


if __name__ == "__main__":
    conn = sqlite3.connect(
        "/Users/max/Library/Mobile Documents/com~apple~CloudDocs/max shared/2024-02-19 Data/2024-02-19_15-26-46_data.db"
    )
    table_names = ["i2c_1_32", "i2c_1_33", "i2c_1_34"]
    main(conn)
    print("done")
    conn.close()
