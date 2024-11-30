import socket
import threading
import time
from datetime import datetime
from enum import Enum

from dataCollection import DataCollector
import json
import os
import subprocess
import traceback

# Device password the one hosting server:
devicePass = "blank1"  # Used for shutdown func below


def shutdown():
    try:
        subprocess.run(
            ["sudo", "-S", "shutdown", "-h", "now"],
            check=True,
            input=f"{devicePass}\n",
            encoding="utf-8",
        )
    except subprocess.CalledProcessError as e:
        print(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}")


# Class that represents settings(used for only sending to client)
class dataSettings:
    def __init__(self, dataCollect: DataCollector, send_fps):
        self.dbName = dataCollect.dbname
        self.isDataCollecting = dataCollect.isCollecting
        self.shouldSendFPS = send_fps
        self.isPaused = dataCollect.isPaused
        if send_fps and dataCollect.manager is not None:
            self.fps = json.dumps(dataCollect.manager.get_fps())

    def to_json(self):
        return json.dumps(self.__dict__)


class SendTypes(Enum):
    FPS = "fps"
    Error = "error"
    Requested = "requested"
    Success = "success"
    Closing = "closing"


class socketServer:
    def send_settings(self, dataCollect: DataCollector):
        setting = dataSettings(dataCollect, self.shouldSendFPS)
        self.send_data(SendTypes.Requested, setting.to_json())

    # only for received "command"s
    def process_command(self, command: str):
        if command == "startDataCollect":
            self.data_collector.startDataCollect()
        elif command == "stopDataCollect":
            self.data_collector.stopDataCollect()
        elif command == "pauseDataCollect":
            self.data_collector.pauseDataCollect()
        elif command == "unpauseDataCollect":
            self.data_collector.unpauseDataCollect()
        elif command == "sendfps":
            self.shouldSendFPS = True
        elif command == "stopSendfps":
            self.shouldSendFPS = False
        elif command == "request":
            self.send_settings(self.data_collector)
        elif command == "shutdown":
            self.send_data(SendTypes.Closing, "now")
            shutdown()
        else:
            self.send_data(SendTypes.Error, f"Unknown command: {command}")
            return

    def received_action(self, data: str):
        print(f"Received: {data}")
        try:
            # Parse the JSON data
            json_data = json.loads(data)
            d_type = json_data.get("type")
            data = json_data.get("data")

            if d_type == "command":
                self.process_command(data)
            elif d_type == "marker":
                # self.data_collector.makeMarker(data)
                pass
            else:
                self.send_data(SendTypes.Error, f"Unknown command type: {d_type}")
                return

            self.send_data(SendTypes.Success, f"{d_type} Successful: {data}")
        except Exception as e:
            print(e.__str__())
            raise e
            # self.send_data(SendTypes.Error, str(e))  # send the error to the client

    def send_data(self, sType: SendTypes, data: str):
        if self.client_socket is not None:
            m_json = json.dumps({"type": sType.value, "data": data})
            print(f"Sent: {m_json}")
            self.client_socket.sendall(m_json.encode("utf-8"))  # Send the data

    def __init__(self):
        self.client_socket = self.client_address = None

        self.shouldSendFPS = False
        self.data_collector = DataCollector()  # create the dataCollector object

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server_socket.bind(("0.0.0.0", 12345))  # use 'localhost' for LAN
        self.server_socket.listen(1)

    def start_sending_updates(self):
        last_time = time.perf_counter()
        while self.server_socket is not None:
            if time.perf_counter() > last_time + 1:
                last_time = time.perf_counter()
                self.send_settings(self.data_collector)
            time.sleep(0.1)

    # Starts server synchronous
    def start_server(self):
        threading.Thread(target=self.start_sending_updates, daemon=True).start()

        print("Server started. Waiting for connections...")
        try:
            while True:
                self.client_socket, self.client_address = self.server_socket.accept()
                print(f"Client {self.client_address} connected.")

                while True:
                    try:
                        data = self.client_socket.recv(1024).decode("utf-8")
                    except ConnectionResetError:
                        print("Error: Connection was broken!")
                        data = None

                    if not data:  # client disconnected
                        print(f"Client {self.client_address} disconnected.")
                        break

                    self.received_action(data)

                self.client_socket.close()
                self.client_socket = None
                self.client_address = None

        except KeyboardInterrupt:
            print("Closing Server...")
            self.send_data(SendTypes.Closing, "now")
            self.client_socket.close()
            self.server_socket.close()

            self.server_socket = None
            self.client_socket = None
            self.client_address = None


if __name__ == "__main__":
    server = socketServer()
    server.start_server()
