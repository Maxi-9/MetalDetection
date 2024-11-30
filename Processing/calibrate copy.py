import sqlite3

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from numpy.linalg import inv, eig
import pickle

import plotly.graph_objects as go


def save_calibration(data_frames, filename):
    data = []
    for i, df in enumerate(data_frames):
        vec = ls_ellipsoid(df)
        center, axes, R = polyToParams3D(vec, printMe=False)
        data_frames[i] = apply_fit_to_data(df, center, axes, R)
        data.append((center, axes, R))

    with open(filename, "wb") as f:
        pickle.dump(data, f)


def load_calibrations(filename):
    with open(filename, "rb") as f:
        data = pickle.load(f)
    return data


def format_df_time_ms(data_frames: list):
    for df in data_frames:
        df["d_time"] = (
            pd.to_datetime(df.index, format="%Y-%m-%d %H:%M:%S.%f").astype(int)
            // 10**6
        )
        df.set_index("d_time", inplace=True)


def cut_off_extra(data_frames: list, cut_start: int = 0, cut_end: int = 0):
    start_time = min(df.index.min() for df in data_frames)
    end_time = max(df.index.max() for df in data_frames)

    for df in data_frames:
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


# Code modified from: http://juddzone.com/ALGORITHMS/least_squares_3D_ellipsoid.html
def ls_ellipsoid(df):
    xx = df["Hx"].values
    yy = df["Hy"].values
    zz = df["Hz"].values

    x = xx[:, np.newaxis]
    y = yy[:, np.newaxis]
    z = zz[:, np.newaxis]

    J = np.hstack((x * x, y * y, z * z, x * y, x * z, y * z, x, y, z))
    K = np.ones_like(x)

    JT = J.transpose()
    JTJ = np.dot(JT, J)
    InvJTJ = np.linalg.inv(JTJ)
    ABC = np.dot(InvJTJ, np.dot(JT, K))

    eansa = np.append(ABC, -1)

    return eansa


def polyToParams3D(vec, printMe):
    if printMe:
        print("\npolynomial\n", vec)

    Amat = np.array(
        [
            [vec[0], vec[3] / 2.0, vec[4] / 2.0, vec[6] / 2.0],
            [vec[3] / 2.0, vec[1], vec[5] / 2.0, vec[7] / 2.0],
            [vec[4] / 2.0, vec[5] / 2.0, vec[2], vec[8] / 2.0],
            [vec[6] / 2.0, vec[7] / 2.0, vec[8] / 2.0, vec[9]],
        ]
    )

    if printMe:
        print("\nAlgebraic form of polynomial\n", Amat)

    A3 = Amat[0:3, 0:3]
    A3inv = inv(A3)
    ofs = vec[6:9] / 2.0
    center = -np.dot(A3inv, ofs)
    if printMe:
        print("\nCenter at:", center)

    Tofs = np.eye(4)
    Tofs[3, 0:3] = center
    R = np.dot(Tofs, np.dot(Amat, Tofs.T))
    if printMe:
        print("\nAlgebraic form translated to center\n", R, "\n")

    R3 = R[0:3, 0:3]
    R3test = R3 / R3[0, 0]
    if printMe:
        print("normed \n", R3test)
    s1 = -R[3, 3]
    R3S = R3 / s1
    (el, ec) = eig(R3S)

    recip = 1.0 / np.abs(el)
    axes = np.sqrt(recip)
    if printMe:
        print("\nAxes are\n", axes, "\n")

    inve = inv(ec)
    if printMe:
        print("\nRotation matrix\n", inve)
    return (center, axes, inve)


def printAns3D(center, axes, R, df):
    xin = df["Hx"].values
    yin = df["Hy"].values
    zin = df["Hz"].values

    print("\nCenter at  %10.4f,%10.4f,%10.4f" % (center[0], center[1], center[2]))
    print("Axes gains %10.4f,%10.4f,%10.4f " % (axes[0], axes[1], axes[2]))
    print(
        "Rotation Matrix\n%10.5f,%10.5f,%10.5f\n%10.5f,%10.5f,%10.5f\n%10.5f,%10.5f,%10.5f"
        % (
            R[0, 0],
            R[0, 1],
            R[0, 2],
            R[1, 0],
            R[1, 1],
            R[1, 2],
            R[2, 0],
            R[2, 1],
            R[2, 2],
        )
    )

    xc = xin - center[0]
    yc = yin - center[1]
    zc = zin - center[2]

    L = np.diag([1 / axes[0], 1 / axes[1], 1 / axes[2]])
    M = np.dot(R.T, np.dot(L, R))
    print("\nTransformation Matrix\n", M)

    [xm, ym, zm] = np.dot(M, [xc, yc, zc])
    rm = np.sqrt(xm * xm + ym * ym + zm * zm)

    print("\nAverage Radius  %10.4f (truth is 1.0)" % (np.mean(rm)))
    print("Stdev of Radius %10.4f\n " % (np.std(rm)))

    return


def plot_3d(data_frames: list):
    for df in data_frames:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

        ax.scatter(df["Hx"], df["Hy"], df["Hz"])

        ax.set_xlabel("Hx")
        ax.set_ylabel("Hy")
        ax.set_zlabel("Hz")

        plt.show()


def apply_fit_to_data(df, center, axes, R):
    # Subtract the center
    df["Hx"] -= center[0]
    df["Hy"] -= center[1]
    df["Hz"] -= center[2]

    # Apply the rotation
    # df[['Hx', 'Hy', 'Hz']] = np.dot(R, df[['Hx', 'Hy', 'Hz']].values.T).T

    # Apply the scaling
    df['Hx'] /= axes[0]
    df['Hy'] /= axes[1]
    df['Hz'] /= axes[2]

    return df

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
