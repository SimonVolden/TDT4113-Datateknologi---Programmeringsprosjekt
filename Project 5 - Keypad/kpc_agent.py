"""
KPC Agent
Manages the keypad
"""

from keypad import Keypad
from led_board import LedBoard


class KPCAgent:
    """
    Agent class
    """

    def __init__(self):
        self.keypad = Keypad()
        self.keypad.setup()
        self.new_password = ""
        self.confirm_password = ""
        self.cump = ""
        self.led_board = LedBoard()

    def start_new_password_entry(self):
        """
        Makes a new password
        """
        self.new_password = ""
        signal = self.keypad.get_next_signal()
        while signal != "*":
            print(signal)
            self.new_password += signal
            signal = self.keypad.get_next_signal()
        if len(self.new_password) < 4:
            print("New password must have a length of 4 or more")
            return "S4"
        return "S5"

    def confirm_new_password_entry(self):
        """
        Checks if you have entered the same password before changing
        """
        self.confirm_password = ""
        signal = self.keypad.get_next_signal()

        while signal != "*":
            print(signal)
            self.confirm_password += signal
            signal = self.keypad.get_next_signal()

        if self.confirm_password == self.new_password:
            print("You have successfully changed password")
            self.keypad.password = self.new_password

            file = "password.txt"
            with open(file, "w") as file_to_write:
                file_to_write.write(self.new_password)
            return "S3"

        print("Passwords do not match")
        return "S3"

    def input_password(self):
        """
        Input password
        """
        self.cump = ""
        signal = self.keypad.get_next_signal()
        while signal != "*":
            print(signal)
            self.cump += signal
            signal = self.keypad.get_next_signal()
        return "S2"

    def verify_login(self):
        """
        Checks if password input is correct
        """
        file = "password.txt"
        if self.cump == open(file, "r").read().strip():
            # print("Correct Password!")
            self.led_board.twinkle(1)
            return "S3"

        # print("Incorrect Password!")
        self.led_board.flash_all(1)
        return "S1"
