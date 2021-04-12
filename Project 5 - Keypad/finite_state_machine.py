"""
Finite state machine
"""
from termcolor import colored
from keypad import Keypad
from led_board import LedBoard
from kpc_agent import KPCAgent


class FiniteStateMachine:
    """ Finite State Machine """

    def __init__(self):
        self.state = "S0"
        self.keypad = Keypad()
        self.keypad.setup()
        self.cump = ""
        self.kpc_agent = KPCAgent()
        self.led_board = LedBoard()
        self.led_signal = None

    def get_next_signal(self):
        """
        Gets the next signal and moves through the state machine
        """
        file = "password.txt"

        if self.state == "S0":
            print("Press any button")
            signal = self.keypad.get_next_signal()
            self.led_board.startup_show()

        if self.state == "S0" and open(file, "r").read().strip() is None:
            print("No password, enter new password")
            self.state = "S4"
            self.get_next_signal()

        if self.state == "S0" and open(file, "r").read().strip() is not None:
            self.state = "S1"
            self.get_next_signal()

        if self.state == "S1":
            print("Enter password: ")
            self.state = self.kpc_agent.input_password()
            self.get_next_signal()

        if self.state == "S2":
            self.state = self.kpc_agent.verify_login()
            self.get_next_signal()

        if self.state == "S3":
            print("Press * to change password: ")
            print("Press # to log out")
            print("Press a number from 0-5 to select LED")
            print("Then input the number of seconds to turn on")
            print("the LED for.")
            signal = self.keypad.get_next_signal()

            if signal == "*":
                self.state = "S4"

            if signal == "#":
                self.state = "S0"
                self.led_board.shutdown_show()
                self.get_next_signal()

            if signal.isdigit() and 0 <= int(signal) <= 5:
                self.led_signal = int(signal)
                self.state = "S6"
                self.get_next_signal()
            else:
                self.get_next_signal()

        if self.state == "S6":
            print("You have selected LED #", self.led_signal)
            print("Enter the amount of seconds to turn on")
            print("LED #", self.led_signal, "for")
            seconds = ""
            signal = self.keypad.get_next_signal()
            while signal != "*":
                print(signal)
                seconds += signal
                signal = self.keypad.get_next_signal()
            if seconds.isdigit():
                self.led_board.light_led(self.led_signal, int(seconds))
                #self.led_board.show_lights()
                self.state = "S3"
                self.get_next_signal()
            else:
                print("You have entered something that is not a number")
                print("Please try again")
                self.state = "S6"
                self.get_next_signal()

        if self.state == "S4":
            print(colored("Enter new password", "green"))
            self.state = self.kpc_agent.start_new_password_entry()

        if self.state == "S5":
            print(colored("Confirm password", "green"))
            self.state = self.kpc_agent.confirm_new_password_entry()

    def run(self):
        """ Loops through get_next_signal """
        while True:
            self.get_next_signal()


def main():
    """ Main """
    fsm = FiniteStateMachine()
    fsm.run()


if __name__ == "__main__":
    main()
