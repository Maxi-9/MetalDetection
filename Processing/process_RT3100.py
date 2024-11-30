import os
from datetime import time
from time import sleep
from typing import List

import pandas
from pandas import DataFrame

from Processing.calibrate import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import vg


def plot_data(data_frames: list, colors):
    # Plotting the data
    plt.figure(figsize=(10, 6))

    plt.plot(
        data_frames[0].index,
        data_frames[0]["Hx"],
        label="hx1",
        color="r",
        linestyle="-",
    )
    plt.plot(
        data_frames[0].index,
        data_frames[0]["Hy"],
        label="hy1",
        color="g",
        linestyle="-",
    )
    plt.plot(
        data_frames[0].index,
        data_frames[0]["Hz"],
        label="hz1",
        color="b",
        linestyle="-",
    )
    plt.plot(
        data_frames[1].index,
        data_frames[1]["Hx"],
        label="hx2",
        color="r",
        linestyle="--",
    )
    plt.plot(
        data_frames[1].index,
        data_frames[1]["Hy"],
        label="hy2",
        color="g",
        linestyle="--",
    )
    plt.plot(
        data_frames[1].index,
        data_frames[1]["Hz"],
        label="hz2",
        color="b",
        linestyle="--",
    )
    plt.plot(
        data_frames[2].index,
        data_frames[2]["Hx"],
        label="hx3",
        color="r",
        linestyle="-.",
    )
    plt.plot(
        data_frames[2].index,
        data_frames[2]["Hy"],
        label="hy3",
        color="g",
        linestyle="-.",
    )
    plt.plot(
        data_frames[2].index,
        data_frames[2]["Hz"],
        label="hz3",
        color="b",
        linestyle="-.",
    )

    # Customize the plot
    plt.title("Raw Magnetometer readings")
    plt.xlabel("Time")
    plt.ylabel("Magnetic Flux (µT)")
    # plt.legend()

    # Show the plot
    plt.grid(True)
    plt.show()


def get_rid_of_extra(data_frames: list[pandas.DataFrame]):
    # Find the intersection of all DataFrame indices
    common_index = set(data_frames[0].index)
    for df in data_frames[1:]:
        common_index.intersection_update(df.index)

    # Keep only the rows with the common index in each DataFrame
    for i, df in enumerate(data_frames):
        data_frames[i] = df[df.index.isin(common_index)]

    return data_frames


def smooth_data(df: pd.DataFrame, window_size: int = 5) -> pd.DataFrame:
    # Apply a rolling mean (moving average) to each column in the dataframe
    # with the specified window size. The default window size is 3.
    # The 'min_periods=1' argument ensures that we still get values even if there
    # are fewer than 'window_size' points at the beginning of the series.
    smoothed_df = df.rolling(window=window_size, min_periods=1, center=True).mean()

    return smoothed_df


def mat_plot_mag_together(data_frames: list[pandas.DataFrame], name):
    # Plotting the data
    plt.figure(figsize=(10, 6))

    get_rid_of_extra(data_frames)
    array_1_2 = np.subtract(data_frames[0]["Magn"], data_frames[1]["Magn"])
    array_2_3 = np.subtract(data_frames[1]["Magn"], data_frames[2]["Magn"])
    get_rid_of_extra([array_1_2, array_2_3])

    plt.plot(
        data_frames[0].index,
        array_1_2,
        label="Sensor (1-2)+(2-3)",
        color="r",
        linestyle="-",
    )


def calculate_angle(
    vectors1: pd.DataFrame, vectors2: pd.DataFrame, vectors3: pd.DataFrame
) -> list[DataFrame]:
    # Initialize lists to store calculated values
    h1mag = []
    h2mag = []
    h3mag = []
    h12 = []
    h32 = []
    h13 = []
    alpha12 = []
    alpha32 = []
    alpha13 = []

    # Iterate over the rows of the input DataFrames
    for i in range(len(vectors1)):
        hx1_r = vectors1.iloc[i, vectors1.columns.get_loc("Hx")]
        hy1_r = vectors1.iloc[i, vectors1.columns.get_loc("Hy")]
        hz1_r = vectors1.iloc[i, vectors1.columns.get_loc("Hz")]
        hx2_r = vectors2.iloc[i, vectors2.columns.get_loc("Hx")]
        hy2_r = vectors2.iloc[i, vectors2.columns.get_loc("Hy")]
        hz2_r = vectors2.iloc[i, vectors2.columns.get_loc("Hz")]
        hx3_r = vectors3.iloc[i, vectors3.columns.get_loc("Hx")]
        hy3_r = vectors3.iloc[i, vectors3.columns.get_loc("Hy")]
        hz3_r = vectors3.iloc[i, vectors3.columns.get_loc("Hz")]

        # Calculate magnitudes of vectors
        h1mag.append(math.sqrt(hx1_r**2 + hy1_r**2 + hz1_r**2))
        h2mag.append(math.sqrt(hx2_r**2 + hy2_r**2 + hz2_r**2))
        h3mag.append(math.sqrt(hx3_r**2 + hy3_r**2 + hz3_r**2))

        # Calculate differences in magnitudes
        h12.append(abs(h1mag[i] - h2mag[i]))
        h32.append(abs(h3mag[i] - h2mag[i]))
        h13.append(abs(h1mag[i] - h3mag[i]))

        # Calculate angles between vectors
        alpha12.append(
            180
            / math.pi
            * math.acos(
                (hx1_r * hx2_r + hy1_r * hy2_r + hz1_r * hz2_r) / h1mag[i] / h2mag[i]
            )
        )
        alpha32.append(
            180
            / math.pi
            * math.acos(
                (hx3_r * hx2_r + hy3_r * hy2_r + hz3_r * hz2_r) / h3mag[i] / h2mag[i]
            )
        )
        alpha13.append(
            180
            / math.pi
            * math.acos(
                (hx1_r * hx3_r + hy1_r * hy3_r + hz1_r * hz3_r) / h1mag[i] / h3mag[i]
            )
        )

    # Create a DataFrame with the calculated angles
    # Create separate DataFrames for each angle
    angles_df_12 = pd.DataFrame({"Angle": alpha12}, index=vectors1.index)
    angles_df_32 = pd.DataFrame({"Angle": alpha32}, index=vectors1.index)
    angles_df_13 = pd.DataFrame({"Angle": alpha13}, index=vectors1.index)

    return [angles_df_12, angles_df_32, angles_df_13]


def mat_plot_angles(data_frames: list[pandas.DataFrame], disc, file_name, loc=None):
    # Plotting the data

    get_rid_of_extra(data_frames)
    plt.figure(figsize=(10, 6))

    # Calculate the angles for the three combinations
    angles = calculate_angle(data_frames[0], data_frames[1], data_frames[2])

    angles = [smooth_data(angle) for angle in angles]
    # print(angles[0])
    plt.plot(
        angles[0].index,
        angles[0]["Angle"],
        label="Sensor 1-2",
        color="r",
        linestyle="-",
    )
    plt.plot(
        angles[1].index,
        angles[1]["Angle"],
        label="Sensor 2-3",
        color="g",
        linestyle="-",
    )
    plt.plot(
        angles[2].index,
        angles[2]["Angle"],
        label="Sensor 1-3",
        color="b",
        linestyle="-",
    )

    # Customize the plot
    plt.title(f"Angles: {disc}: {file_name.replace('.db','')}")
    plt.xlabel("Time")
    plt.ylabel("Angle (degrees)")
    plt.legend()

    # Show the plot
    plt.grid(True)
    if loc:
        jpg_name = f"{loc}{disc}/angles{file_name.replace('.db','')}.jpg"
        print(f"Saving plot to {jpg_name}")
        plt.savefig(jpg_name, format="jpeg", dpi=300)
    plt.show()


def mat_plot_mag(data_frames: list[pandas.DataFrame], disc, file_name, loc=None):
    # Plotting the data
    plt.figure(figsize=(10, 6))

    get_rid_of_extra(data_frames)
    array_1_2 = np.subtract(data_frames[0]["Magn"], data_frames[1]["Magn"])
    array_2_3 = np.subtract(data_frames[1]["Magn"], data_frames[2]["Magn"])
    array_1_3 = np.subtract(data_frames[0]["Magn"], data_frames[2]["Magn"])
    get_rid_of_extra([array_1_2, array_2_3, array_1_3])

    arrays = [smooth_data(angle) for angle in [array_1_2, array_2_3, array_1_3]]
    plt.plot(
        data_frames[0].index,
        arrays[0],
        label="Sensor 1-2",
        color="r",
        linestyle="-",
    )
    plt.plot(
        data_frames[1].index,
        arrays[1],
        label="Sensor 2-3",
        color="g",
        linestyle="-",
    )
    plt.plot(
        data_frames[2].index,
        arrays[2],
        label="Sensor 1-3",
        color="b",
        linestyle="-",
    )

    # Customize the plot
    plt.title(f"Magnitude differences: {disc}: {file_name.replace('.db','')}")
    plt.xlabel("Time")
    plt.ylabel("Magnetic Flux (µT)")
    plt.legend()

    # Show the plot
    plt.grid(True)

    # save file to loc
    if loc:
        jpg_name = f"{loc}{disc}/mag{file_name.replace('.db','')}.jpg"
        print(f"Saving plot to {jpg_name}")
        plt.savefig(jpg_name, format="jpeg", dpi=300)

    plt.show()


def plot_mag(data_frames: list):
    fig = go.Figure()

    line_styles = [
        "solid",
        "dash",
        "dot",
        "dashdot",
    ]  # Define different line styles for each dataset
    for i, df in enumerate(data_frames):
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["Magn"],
                mode="lines",
                line=dict(color="blue", dash=line_styles[i % len(line_styles)]),
                name=f"{i}th sensor",
            )
        )

    fig.update_layout(
        xaxis_title="X Label", yaxis_title="Y Label", title="Magnitude", showlegend=True
    )

    fig.show()


def signaltonoise(a, axis=0, ddof=0):
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m / sd)


def plot_df(data_frames: list, colors: dict):
    fig = go.Figure()
    line_styles = [
        "solid",
        "dash",
        "dot",
        "dashdot",
    ]  # Define different line styles for each dataset

    for i, df in enumerate(data_frames):
        style = line_styles[i % len(line_styles)]

        for j, (col, color) in enumerate(colors.items()):
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df[col],
                    line=dict(color=color, dash=style),
                    mode="lines",
                    name=f"{col}_df{i+1}",
                )
            )

    fig.show()


def main(
    conn: sqlite3.Connection,
    disc,
    file_name,
    calibration="calibration.pkl",
    graph_dir=None,
        line=""
):
    if graph_dir is not None:
        # create folder if it doeNS't exist
        if not os.path.exists(f"{graph_dir}{disc}"):
            os.makedirs(f"{graph_dir}{disc}")

    data_frames = []  # Create an empty list to store the DataFrames
    table_names = ["i2c_1_32", "i2c_1_33", "i2c_1_34"]
    for table_name in table_names:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        df.set_index("d_time", inplace=True)
        data_frames.append(df)

    resample(data_frames)
    format_df_time_ms(data_frames)

    # plot_3d(data_frames)
    # plot_df(data_frames, colors={"Hx": "red", "Hy": "green", "Hz": "blue"})
    # Fit here
    # plot_data(data_frames, colors=["red", "green", "blue"])
    calibrate(data_frames)
    # plot_mag(data_frames)


    maxi = []
    for df in data_frames:
        for col in df.columns:
            if col == "Magn":
                continue
            ston = signaltonoise(df[col])
            maxi.append(abs(ston))
            print(signaltonoise(df[col]), col)
    # average

    print(sum(maxi) / len(maxi))


    # # plot_df(data_frames, colors={"Hx": "red", "Hy": "green", "Hz": "blue"})
    # dupe = [frame.copy() for frame in data_frames]
    # mat_plot_mag(dupe, disc, file_name, loc=None)
    # uinput = input("Cut of start/end: ")
    # dupe = data_frames.copy()
    # split = []
    # while uinput != "":
    #     # print(f"Cutting off {uinput}: current len {len(dupe["Angle"])}")
    #
    #     split = uinput.split(",")
    #     cut_off_extra(dupe, cut_start=int(split[0]), cut_end=int(split[1]))
    #     mat_plot_mag(dupe, disc, file_name, loc=None)
    #     uinput = input("Cut of start/end: ")
    #     dupe = [frame.copy() for frame in data_frames]
    #
    #     # file.write(",".join(split) + "\n")

    sleep(0.1)
    dupe = [frame.copy() for frame in data_frames]
    uinput = line
    dupe = data_frames.copy()
    split = []
    # print(f"Cutting off {uinput}: current len {len(dupe["Angle"])}")

    split = uinput.split(",")
    cut_off_extra(dupe, cut_start=int(split[0]), cut_end=int(split[1]))

    # file.write(",".join(split) + "\n")

    mat_plot_mag(dupe, disc, file_name, loc=graph_dir)
    mat_plot_angles(dupe, disc, file_name, loc=graph_dir)

    # mat_plot_mag(, name)
    # plot_data(data_frames, colors=["red", "green", "blue"])

    # plot_df(data_frames, colors={"Hx": "red", "Hy": "green", "Hz": "blue"})


def process(file_full, disc, file_name,line=""):
    # Extract the file name from the path
    # file_name = os.path.basename(file_full)

    # Concatenate with the run name

    conn = sqlite3.connect(file_full)

    main(conn, disc, file_name, graph_dir=file_full.replace(file_name, ""),line=line)
    print("done")
    conn.close()


"""
Keyword convention:
- Metal: Metal pan in middle of run
- Upside down: Metal pan upside down in middle of run(with bottom of pan on the top)
- EW: Parallel with East West direction(Default)
- NS: Parallel with South North direction
- Pauses: Pauses over metal with sensor 1 over the pan, then 2, then 3.
- Control: No metal
- HH: Horizontal Hold(default)
- VH: Vertical Hold
- HM: Horizontal motion, moving left to right(default)
- VM: Vertical motion, moving up, down, and back up
- PM: Parallel motion
- PerpM: Perpendicular motion(default)
"""
if __name__ == "__main__":
    # process(loc = "/Users/max/Library/Mobile Documents/com~apple~CloudDocs/data/2024-03-10_16-46-54_data.db", run_name="Horizontal Paced with Metal")

    var = {
        "Metal": [
            "2024-03-10_16-46-54_data.db",
            "2024-03-10_16-49-48_data.db",
            "2024-03-10_16-51-03_data.db",
        ],
        "Metal Upside Down": [
            "2024-03-10_16-55-43_data.db",
            "2024-03-10_17-04-00_data.db",
        ],
        "Metal with Pauses": ["2024-03-10_17-07-01_data.db"],
        "Metal PM with Pauses": ["2024-03-10_17-09-21_data.db"],
        "Metal EW VM": ["2024-03-10_17-20-36_data.db"],
        "Metal NS VM": ["2024-03-10_17-23-27_data.db"],
        "Control": [
            "2024-03-10_17-26-01_data.db",
            "2024-03-10_17-27-20_data.db",
            "2024-03-10_17-29-00_data.db",
        ],
    }

    base_directory = "/Users/max/Library/Mobile Documents/com~apple~CloudDocs/data/"
    with open("file.txt", "r") as file:
        for run_name, files in var.items():
            for file_name in files:
                file_location = base_directory + file_name
                # try:

                process(file_full=file_location, disc=run_name, file_name=file_name, line = file.readline())
                # except Exception as e:
                #   print(f"Error with {file_name}, Error: {e}")
