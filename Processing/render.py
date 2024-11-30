import math
import threading
import time
from Sensors.WT901 import WT901, get_wtports

# Jean Joubert 14 April 2020
# Simple program to rotate cube in 3D space

import turtle
from math import sin, cos

win = turtle.Screen()
win.setup(1200, 600)
win.tracer(0)
counter = 0


def rotate(x, y, r):
    s, c = sin(r), cos(r)
    return x * c - y * s, x * s + y * c


class Cube:
    EDGES = (0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)
    VERTICES = [(-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)]

    def reset(self):
        self.EDGES = (0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)
        self.VERTICES = [(-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, 1), (1, -1, 1), (1, 1, 1),
                         (-1, 1, 1)]

    def __init__(self, sensor, offset):
        self.offset = offset
        self.counter = 0

        self.sensor = WT901(sensor, baudrate=115200)

        self.sensor.flush()
        self.row = None

    def draw(self, t, row):

        for edge in self.EDGES:
            points = []

            for vertex in edge:
                x, y, z = self.VERTICES[vertex]

                x, z = rotate(x, z, row.Yaw * math.pi / 180)  # Only this one to rotate around y
                y, z = rotate(y, z, row.Roll * math.pi / 180)  # Only this for x
                x, y = rotate(x, y, row.Pitch * math.pi / 180)  # This for z

                z += 5
                if z != 0:
                    f = 400 / (z)  # f gives size/distance (smaller value = smaller cube)

                sx, sy = x * f, y * f
                points.append(sx)
                points.append(sy)

            t.up()
            t.goto(points[0] + (1-self.offset)*350, points[1])
            t.down()
            t.goto(points[2] + (1-self.offset)*350, points[3])
            t.up()


def startRows(cube):
    cube.row = cube.sensor.get_raw_data()
    print(cube.sensor.ser.name, "... Started")
    while True:
        cube.sensor.flush()
        cube.row = cube.sensor.get_raw_data()
        time.sleep(0.02)


def main(ports):
    t = turtle.Turtle()
    t.ht()
    t.color('black')

    cubes = []
    i = 0
    for port in ports:
        curCube = Cube(port, i)
        cubes.append(curCube)
        threading.Thread(target=startRows, args=(curCube,), daemon=True).start()
        i += 1

    correction = 0
    t2 = time.time()
    while True:
        t3 = t2
        t1 = time.time()
        t.clear()
        for cube in cubes:
            if cube.row is not None:
                cube.draw(t, cube.row)
                cube.counter += 0.005
                cube.reset()

        t.up()
        t.goto(-(win.window_width() - 50) / 2, -(win.window_height() - 50) / 2)
        t.down()

        t2 = time.time()

        fps = round(1.0 / (t2 - t3), 2)

        t.write(str(fps))
        t.up()
        win.update()

        correction = (1 / 120 - (t2 - t1))


        if '-' not in str(correction):
            time.sleep(correction)


if __name__ == '__main__':
    ports = get_wtports()
    ports.sort()
    print("Ports", ports)
    main(ports)
