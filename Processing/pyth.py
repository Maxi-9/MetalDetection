#!/usr/bin/env python
# coding: utf-8

# In[1]:


sel = 11
Fix_cal = True
GraphOut = 1  # 0 means no graphs, 1 essentials, 2 all
mag_calibration1 = [-3.5589472772441937, -4.718578808193119, -3.42343196960233]
mag_calibration2 = [-3.412272238517975, 1.1391331660352293, 0.36322967417460106]
mag_calibration3 = [-1.351673306603324, 2.8039616258067923, 0.8569762535837135]
s1x = 0.9731
s1y = 0.9663
s1z = 0.9746
s2x = 0.9788
s2y = 1.0132
s2z = 1.0474
s3x = 1.0249
s3y = 1.0234
s3z = 0.9983


# In[2]:


import sqlite3
from datetime import datetime

# Connect to the SQLite database file
# db_file_path = '/Users/schwick/jupyter/Maxdata2024-02-11/Fifth_Metal_22-13-29_data.db'
# db_file_path = '/Users/schwick/jupyter/Maxdata2024-02-11/First_21-58-18_data.db'
# db_file_path = '/Users/schwick/jupyter/Maxdata2024-02-11/Sixth_22-17-18_data.db'
# db_file_path = '/Users/schwick/jupyter/Maxdata2024-02-11/Second_22-01-27_data.db'
# db_file_path = '/Users/schwick/jupyter/Maxdata2024-02-11/Third_Metal_Incomplete_22-06-27_data.db'
db0 = "/Users/schwick/jupyter/Maxdata2024-02-11/Fourth_Metal_22-10-24_data.db"

# calibration runs
db1 = "/Users/schwick/Library/Mobile Documents/com~apple~CloudDocs/max shared/2024-02-18_20-19-30_data.db"
db2 = "/Users/schwick/Library/Mobile Documents/com~apple~CloudDocs/max shared/2024-02-18_20-30-07_data.db"
db3 = "/Users/schwick/Library/Mobile Documents/com~apple~CloudDocs/max shared/2024-02-18_20-31-40_data.db"
db4 = "/Users/schwick/Library/Mobile Documents/com~apple~CloudDocs/max shared/2024-02-18_20-32-56_data.db"


dbcal1 = "/Users/schwick/Library/Mobile Documents/com~apple~CloudDocs/max shared/2024-02-19 Data/2024-02-19_15-24-14_data.db"
dbcal2 = "/Users/schwick/Library/Mobile Documents/com~apple~CloudDocs/max shared/2024-02-19 Data/2024-02-19_15-26-46_data.db"

ndpath = "/Users/schwick/Library/Mobile Documents/com~apple~CloudDocs/max shared/2024-02-19 Data/"
nd = [
    # horizontal no metal
    "2024-02-19_14-56-35_data.db",
    "2024-02-19_14-58-34_data.db",
    "2024-02-19_14-59-32_data.db",
    # horizontal metal
    "2024-02-19_15-02-49_data.db",
    "2024-02-19_15-04-29_data.db",
    "2024-02-19_15-06-01_data.db",
    # vertical metal
    "2024-02-19_15-12-02_data.db",
    "2024-02-19_15-13-06_data.db",
    "2024-02-19_15-14-09_data.db",
    # vertical no metal
    "2024-02-19_15-15-08_data.db",
    "2024-02-19_15-15-48_data.db",
    "2024-02-19_15-16-37_data.db",
]

xxxx = "/Users/schwick/Library/Mobile Documents/com~apple~CloudDocs/max shared/2024-02-12 b4 Data/2024-02-12_21-56-56_data.db"

db_file_path = ndpath + nd[sel]
# db_file_path=xxxx


conn = sqlite3.connect(db_file_path)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Execute a SELECT query to fetch data
query = "SELECT * FROM i2c_1_32"
cursor.execute(query)

# Fetch all the rows
rows1 = cursor.fetchall()

ms1 = []
hx1 = []
hy1 = []
hz1 = []
i = 0

# Process the fetched data
for row in rows1:
    if i == 0:
        ms0 = float(
            datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f").timestamp() * 1000
        )
    milliseconds = float(
        datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f").timestamp() * 1000
    )
    ms1.append(milliseconds - ms0)

    hx1.append(row[1])
    hy1.append(row[2])
    hz1.append(row[3])

    # print(i,ms1[i], hx1[i],hy1[i],hz1[i] )
    i += 1

# Close the cursor and connection
cursor.close()
conn.close()


conn = sqlite3.connect(db_file_path)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Execute a SELECT query to fetch data
query = "SELECT * FROM i2c_1_33"
cursor.execute(query)

# Fetch all the rows
rows2 = cursor.fetchall()

# Process the fetched data
ms2 = []
hx2 = []
hy2 = []
hz2 = []
i = 0

# Process the fetched data
for row in rows2:
    milliseconds = float(
        datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f").timestamp() * 1000
    )
    ms2.append(milliseconds - ms0)

    hx2.append(row[1])
    hy2.append(row[2])
    hz2.append(row[3])

    # print(i,ms2[i], hx2[i],hy2[i],hz2[i] )
    i += 1

# Close the cursor and connection
cursor.close()
conn.close()


conn = sqlite3.connect(db_file_path)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Execute a SELECT query to fetch data
query = "SELECT * FROM i2c_1_34"
cursor.execute(query)

# Fetch all the rows
rows3 = cursor.fetchall()

# Process the fetched data
ms3 = []
hx3 = []
hy3 = []
hz3 = []
i = 0

# Process the fetched data
print(ms0)
for row in rows3:
    if i == 0:
        ms0 = float(
            datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f").timestamp() * 1000
        )
    milliseconds = float(
        datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f").timestamp() * 1000
    )
    ms3.append(milliseconds - ms0)

    hx3.append(row[1])
    hy3.append(row[2])
    hz3.append(row[3])

    # print(i,ms3[i], hx3[i],hy3[i],hz3[i] )
    i += 1


# Close the cursor and connection
cursor.close()
conn.close()


# In[3]:


import matplotlib.pyplot as plt
import numpy as np

# Sample data
# time = np.linspace(0, 10, 100)        # Replace this with your actual time data
# hx_data = np.sin(time)        # Replace this with your actual hx data
# hy_data = np.cos(time)        # Replace this with your actual hy data
# hz_data = np.sin(2 * time)        # Replace this with your actual hz data

# Plotting the data
plt.figure(figsize=(10, 6))

plt.plot(ms1, hx1, label="hx1", color="r", linestyle="-")
plt.plot(ms1, hy1, label="hy1", color="g", linestyle="-")
plt.plot(ms1, hz1, label="hz1", color="b", linestyle="-")
plt.plot(ms2, hx2, label="hx2", color="r", linestyle="--")
plt.plot(ms2, hy2, label="hy2", color="g", linestyle="--")
plt.plot(ms2, hz2, label="hz2", color="b", linestyle="--")
plt.plot(ms3, hx3, label="hx3", color="r", linestyle="-.")
plt.plot(ms3, hy3, label="hy3", color="g", linestyle="-.")
plt.plot(ms3, hz3, label="hz3", color="b", linestyle="-.")

# Customize the plot
plt.title("Raw Magnetometer readings")
plt.xlabel("Time (ms)")
plt.ylabel("Magnetic Flux (µT)")
plt.legend()

# Show the plot
plt.grid(True)
if GraphOut == 2:
    plt.savefig(db_file_path + "_raw.jpg", format="jpeg", dpi=300)
plt.show()


# In[4]:


import math

# For 50 Hz resampling
rightlimit = math.ceil(max(max(ms1), max(ms2), max(ms3)) / 20) * 20
ms = np.linspace(0, rightlimit, math.ceil((rightlimit * 50 + 1) / 1000))
# print (ms)


# In[5]:


hx1_r = np.interp(ms, ms1, hx1)
hy1_r = np.interp(ms, ms1, hy1)
hz1_r = np.interp(ms, ms1, hz1)
hx2_r = np.interp(ms, ms2, hx2)
hy2_r = np.interp(ms, ms2, hy2)
hz2_r = np.interp(ms, ms2, hz2)
hx3_r = np.interp(ms, ms3, hx3)
hy3_r = np.interp(ms, ms3, hy3)
hz3_r = np.interp(ms, ms3, hz3)

h1mag = []
h2mag = []
h3mag = []
h12 = []
h32 = []
alpha12 = []
alpha32 = []
for i in range(len(ms)):
    h1mag.append(math.sqrt(hx1_r[i] ** 2 + hy1_r[i] ** 2 + hz1_r[i] ** 2))
    h2mag.append(math.sqrt(hx2_r[i] ** 2 + hy2_r[i] ** 2 + hz2_r[i] ** 2))
    h3mag.append(math.sqrt(hx3_r[i] ** 2 + hy3_r[i] ** 2 + hz3_r[i] ** 2))
    h12.append(abs(h1mag[i] - h2mag[i]))
    h32.append(abs(h3mag[i] - h2mag[i]))
    alpha12.append(
        180
        / math.pi
        * math.acos(
            (hx1_r[i] * hx2_r[i] + hy1_r[i] * hy2_r[i] + hz1_r[i] * hz2_r[i])
            / h1mag[i]
            / h2mag[i]
        )
    )
    alpha32.append(
        180
        / math.pi
        * math.acos(
            (hx3_r[i] * hx2_r[i] + hy3_r[i] * hy2_r[i] + hz3_r[i] * hz2_r[i])
            / h3mag[i]
            / h2mag[i]
        )
    )


# In[6]:


# Plotting the data
plt.figure(figsize=(10, 6))

plt.plot(ms, hx1_r, label="hx1_r", color="r", linestyle="-")
plt.plot(ms, hy1_r, label="hy1_r", color="g", linestyle="-")
plt.plot(ms, hz1_r, label="hz1_r", color="b", linestyle="-")
plt.plot(ms, hx2_r, label="hx2_r", color="r", linestyle="--")
plt.plot(ms, hy2_r, label="hy2_r", color="g", linestyle="--")
plt.plot(ms, hz2_r, label="hz2_r", color="b", linestyle="--")
plt.plot(ms, hx3_r, label="hx3_r", color="r", linestyle="-.")
plt.plot(ms, hy3_r, label="hy3_r", color="g", linestyle="-.")
plt.plot(ms, hz3_r, label="hz3_r", color="b", linestyle="-.")

# Customize the plot
plt.title("Common Time-base Magnetometer readings")
plt.xlabel("Time (ms)")
plt.ylabel("Magnetic Flux (µT)")
plt.legend()

# Show the plot
plt.grid(True)
if GraphOut == 2:
    plt.savefig(db_file_path + "_resample.jpg", format="jpeg", dpi=300)

plt.show()


# In[ ]:


# In[7]:


# Plotting the data
plt.figure(figsize=(10, 6))

plt.plot(ms, h1mag, label="h1_mag", color="r", linestyle="-")
plt.plot(ms, h2mag, label="h2_mag", color="g", linestyle="-")
plt.plot(ms, h3mag, label="h3_mag", color="b", linestyle="-")

# Customize the plot
plt.title("Magnetometer Magnitudes")
plt.xlabel("Time (ms)")
plt.ylabel("Magnetic Flux (µT)")
plt.legend()

# Show the plot
plt.grid(True)
if GraphOut == 2:
    plt.savefig(db_file_path + "_magnitudes.jpg", format="jpeg", dpi=300)

plt.show()


# In[8]:


# Plotting the data
plt.figure(figsize=(10, 6))

plt.plot(ms, h12, label="h12_mag", color="black", linestyle="-")
plt.plot(ms, h32, label="h32_mag", color="gray", linestyle="-.")

# Customize the plot
plt.title("Magnetometer Magnitude Differences")
plt.xlabel("Time (ms)")
plt.ylabel("Magnetic Flux (µT)")
plt.legend()

# Show the plot
plt.grid(True)
if GraphOut == 2:
    plt.savefig(db_file_path + "_diff123.jpg", format="jpeg", dpi=300)

plt.show()


# In[9]:


# Plotting the data
plt.figure(figsize=(10, 6))

plt.plot(ms, alpha12, label="alpha12_mag", color="r", linestyle="-")
plt.plot(ms, alpha32, label="alpha32_mag", color="g", linestyle="-")

# Customize the plot
plt.title(f"Angle between vectors (degree) {nd[sel]}")
plt.xlabel("Time (ms)")
plt.ylabel("Angle (degree)")
plt.legend()

# Show the plot
plt.grid(True)
if GraphOut == 2:
    plt.savefig(db_file_path + "_angles.jpg", format="jpeg", dpi=300)

plt.show()


# # Calibration

# In[10]:


from matplotlib.animation import FuncAnimation
import time

get_ipython().run_line_magic("matplotlib", "notebook")
from matplotlib.animation import FuncAnimation
import datetime
import matplotlib.dates as mdates

avs = 1
print(db_file_path)
mag_x1 = np.copy(hx1_r)
mag_y1 = np.copy(hy1_r)
mag_z1 = np.copy(hz1_r)
mag_x2 = np.copy(hx2_r)
mag_y2 = np.copy(hy2_r)
mag_z2 = np.copy(hz2_r)
mag_x3 = np.copy(hx3_r)
mag_y3 = np.copy(hy3_r)
mag_z3 = np.copy(hz3_r)

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
    mag_calibration1 = [(max_x + min_x) / 2, (max_y + min_y) / 2, (max_z + min_z) / 2]
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
    mag_calibration2 = [(max_x + min_x) / 2, (max_y + min_y) / 2, (max_z + min_z) / 2]
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
    mag_calibration3 = [(max_x + min_x) / 2, (max_y + min_y) / 2, (max_z + min_z) / 2]
    avs = (s1x + s1y + s1z + s2x + s2y + s2z + s3x + s3y + s3z) / 9
print("3 Final calibration in uTesla:", mag_calibration3)

print("Average reading", avs)

cal_mag_x1 = [avs / s1x * (x - mag_calibration1[0]) for x in mag_x1]
cal_mag_y1 = [avs / s1y * (y - mag_calibration1[1]) for y in mag_y1]
cal_mag_z1 = [avs / s1z * (z - mag_calibration1[2]) for z in mag_z1]

cal_mag_x2 = [avs / s2x * (x - mag_calibration2[0]) for x in mag_x2]
cal_mag_y2 = [avs / s2y * (y - mag_calibration2[1]) for y in mag_y2]
cal_mag_z2 = [avs / s2z * (z - mag_calibration2[2]) for z in mag_z2]

cal_mag_x3 = [avs / s3x * (x - mag_calibration3[0]) for x in mag_x3]
cal_mag_y3 = [avs / s3y * (y - mag_calibration3[1]) for y in mag_y3]
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

print("Cal Factors")
print(f"s1x = {s1x/avs:.4f} s1y = {s1y/avs:.4f} s1z = {s1z/avs:.4f}")
print(f"s2x = {s2x/avs:.4f} s2y = {s2y/avs:.4f} s2z = {s2z/avs:.4f}")
print(f"s3x = {s3x/avs:.4f} s3y = {s3y/avs:.4f} s3z = {s3z/avs:.4f}")


# In[11]:


# Plotting the data
plt.figure(figsize=(10, 6))

plt.plot(ms, cal_mag1, label="h1_cal_mag", color="r", linestyle="-")
plt.plot(ms, h1mag, label="h1_mag", color="r", linestyle="-.")
plt.plot(ms, cal_mag2, label="h2_cal_mag", color="g", linestyle="-")
plt.plot(ms, h2mag, label="h2_mag", color="g", linestyle="-.")
plt.plot(ms, cal_mag3, label="h3_cal_mag", color="b", linestyle="-")
plt.plot(ms, h3mag, label="h3_mag", color="b", linestyle="-.")

# Customize the plot
plt.title("Calibrated Magnetometer Magnitudes")
plt.xlabel("Time (ms)")
plt.ylabel("Magnetic Flux (µT)")
plt.legend()

# Show the plot
plt.grid(True)
if GraphOut == 2:
    plt.savefig(db_file_path + "_magnitudes.jpg", format="jpeg", dpi=300)

plt.show()


# In[12]:


h12_cal = []
alpha12_cal = []
h32_cal = []
alpha32_cal = []

for i in range(len(ms)):
    h12_cal.append(abs(cal_mag1[i] - cal_mag2[i]))
    h32_cal.append(abs(cal_mag3[i] - cal_mag2[i]))
    alpha12_cal.append(
        180
        / math.pi
        * math.acos(
            (
                cal_mag_x1[i] * cal_mag_x2[i]
                + cal_mag_y1[i] * cal_mag_y2[i]
                + cal_mag_z1[i] * cal_mag_z2[i]
            )
            / cal_mag1[i]
            / cal_mag2[i]
        )
    )
    alpha32_cal.append(
        180
        / math.pi
        * math.acos(
            (
                cal_mag_x3[i] * cal_mag_x2[i]
                + cal_mag_y3[i] * cal_mag_y2[i]
                + cal_mag_z3[i] * cal_mag_z2[i]
            )
            / cal_mag3[i]
            / cal_mag2[i]
        )
    )


# In[13]:


# Plotting the data
plt.figure(figsize=(10, 6))

plt.plot(ms, alpha12, label="alpha12_mag", color="r", linestyle="--")
plt.plot(ms, alpha32, label="alpha32_mag", color="g", linestyle="--")
plt.plot(ms, alpha12_cal, label="alpha12_cal", color="r", linestyle="-")
plt.plot(ms, alpha32_cal, label="alpha32_cal", color="g", linestyle="-")

# Customize the plot
plt.title("Angle between vectors")
plt.xlabel("Time (ms)")
plt.ylabel("Angle (degree)")
plt.legend()

# Show the plot
plt.grid(True)
if GraphOut > 0:
    plt.savefig(db_file_path + "_angles.jpg", format="jpeg", dpi=300)

plt.show()


# In[14]:


fig, ax = plt.subplots(1, 1)
ax.set_aspect(1)

# Clear all axis
ax.cla()

# Display the now calibrated data
ax.scatter(cal_mag_x3, cal_mag_y3, color="r")
ax.scatter(cal_mag_y3, cal_mag_z3, color="g")
ax.scatter(cal_mag_z3, cal_mag_x3, color="b")
fig.show()


# In[15]:


# Plotting the data
plt.figure(figsize=(10, 6))

plt.plot(ms, alpha12_cal, label="alpha12_cal", color="r", linestyle="-")
plt.plot(ms, alpha32_cal, label="alpha32_cal", color="g", linestyle="-")

# Customize the plot
plt.title(f"Angle between vectors        {nd[sel]}")
plt.xlabel("Time (ms)")
plt.ylabel("Angles (degrees)")
plt.legend()

# Show the plot
plt.grid(True)
if GraphOut > 0:
    plt.savefig(db_file_path + "_cal_angles.jpg", format="jpeg", dpi=300)

plt.show()


# In[16]:


# Plotting the data
plt.figure(figsize=(10, 6))

plt.plot(ms, cal_mag1, label="h1_cal_mag", color="r", linestyle="-")
plt.plot(ms, cal_mag2, label="h2_cal_mag", color="g", linestyle="-")
plt.plot(ms, cal_mag3, label="h3_cal_mag", color="b", linestyle="-")

# Customize the plot
plt.title(f"Calibrated Magnetometer Magnitudes        {nd[sel]}")
plt.xlabel("Time (ms)")
plt.ylabel("Magnetic Flux (µT)")
plt.legend()

# Show the plot
plt.grid(True)
if GraphOut > 0:
    plt.savefig(db_file_path + "cal_magnitudes.jpg", format="jpeg", dpi=300)

plt.show()


# In[17]:


fig, ax = plt.subplots(1, 1)
ax.set_aspect(1)


# Clear all axis
ax.cla()

# Display the sub-plots
ax.scatter(mag_x1, mag_y1, color="r")
ax.scatter(mag_y1, mag_z1, color="g")
ax.scatter(mag_z1, mag_x1, color="b")


# In[18]:


outstr = []
mystr = (
    "N \tms \tHx1 \tHy1 \tHz1 \tHx2 \tHy2 \tHz2 \tHx3 \tHy3 \tHz3 \tH1mag \tH2mag \tH3mag \tH12diff \tH32diff "
    "\talpha12 \talpha32"
)
mystr += "\tHx1_cal \tHy1_cal \tHz1_cal \tHx2_cal \tHy2_cal \tHz2_cal \tHx3_cal \tHy3_cal \tHz3_cal \tH1mag_cal \tH2mag_cal \tH3mag_cal \tH12diff_cal \tH32diff_cal \talpha12_cal \talpha32_cal"
outstr.append(mystr)
for i in range(len(ms)):
    mystr = f"{i}\t{ms[i]}\t{hx1_r[i]:.4f}\t{hy1_r[i]:.4f}\t{hz1_r[i]:.4f}\t{hx2_r[i]:.4f}\t{hy2_r[i]:.4f}\t{hz2_r[i]:.4f}\t{hx3_r[i]:.4f}\t{hy3_r[i]:.4f}\t{hz3_r[i]:.4f}"
    mystr += f"\t{h1mag[i]:.4f}\t{h2mag[i]:.4f}\t{h3mag[i]:.4f}\t{h12[i]:.4f}\t{h32[i]:.4f}\t{alpha12[i]:.4f}\t{alpha32[i]:.4f}"
    mystr += f"\t{cal_mag_x1[i]:.4f}\t{cal_mag_y1[i]:.4f}\t{cal_mag_z1[i]:.4f}\t{cal_mag_x2[i]:.4f}\t{cal_mag_y2[i]:.4f}\t{cal_mag_z2[i]:.4f}\t{cal_mag_x3[i]:.4f}\t{cal_mag_y3[i]:.4f}\t{cal_mag_z3[i]:.4f}"
    mystr += f"\t{cal_mag1[i]:.4f}\t{cal_mag2[i]:.4f}\t{cal_mag3[i]:.4f}\t{h12_cal[i]:.4f}\t{h32_cal[i]:.4f}\t{alpha12_cal[i]:.4f}\t{alpha32_cal[i]:.4f}"
    outstr.append(mystr)

file_path = db_file_path + ".dat"

cal_mag_x3, cal_mag_y3

# Open the file in write mode ('w')
with open(file_path, "w") as file:
    file.writelines("\n".join(outstr))


# In[19]:


# Plotting the data
plt.figure(figsize=(10, 6))

plt.plot(ms, cal_mag_x1, label="hx1_r", color="r", linestyle="-")
plt.plot(ms, cal_mag_y1, label="hy1_r", color="g", linestyle="-")
plt.plot(ms, cal_mag_z1, label="hz1_r", color="b", linestyle="-")
plt.plot(ms, cal_mag_x2, label="hx2_r", color="r", linestyle="--")
plt.plot(ms, cal_mag_y2, label="hy2_r", color="g", linestyle="--")
plt.plot(ms, cal_mag_z2, label="hz2_r", color="b", linestyle="--")
plt.plot(ms, cal_mag_x3, label="hx3_r", color="r", linestyle="-.")
plt.plot(ms, cal_mag_y3, label="hy3_r", color="g", linestyle="-.")
plt.plot(ms, cal_mag_z3, label="hz3_r", color="b", linestyle="-.")

# Customize the plot
plt.title("Common Time-base Magnetometer readings")
plt.xlabel("Time (ms)")
plt.ylabel("Magnetic Flux (µT)")
plt.legend()

# Show the plot
plt.grid(True)

plt.show()


# In[20]:


print(db_file_path)


# In[21]:


import matplotlib.pyplot as plt
import numpy as np

# Generate some example data
x = np.linspace(0, 2 * np.pi, 10)  # ms
y = 0 * ms
u = np.cos(x)  # x-component of vectors
v = np.sin(2 * x)  # y-component of vectors

# Create a vector plot using quiver
plt.quiver(ms, y, u, v, scale=5, color="blue", width=0.01)

# Customize the plot
plt.title("Vector Plot")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.grid(True)

# Show the plot
plt.show()


# In[ ]:
