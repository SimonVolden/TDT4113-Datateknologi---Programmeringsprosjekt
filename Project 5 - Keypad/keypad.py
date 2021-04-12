"""
Keypad
"""
import time
from GPIOSimulator_v5 import GPIOSimulator

#Pins
PIN_KEYPAD_ROW_0 = 3
PIN_KEYPAD_ROW_1 = 4
PIN_KEYPAD_ROW_2 = 5
PIN_KEYPAD_ROW_3 = 6

PIN_KEYPAD_COL_0 = 7
PIN_KEYPAD_COL_1 = 8
PIN_KEYPAD_COL_2 = 9

class Keypad:
    """A simulated keypad"""

    def __init__(self):
        self.gpio = GPIOSimulator()
        self.key_coord = {(0, 0): '1',
                          (0, 1): '2',
                          (0, 2): '3',
                          (1, 0): '4',
                          (1, 1): '5',
                          (1, 2): '6',
                          (2, 0): '7',
                          (2, 1): '8',
                          (2, 2): '9',
                          (3, 0): '*',
                          (3, 1): '0',
                          (3, 2): '#'}

    def setup(self):
        """Setup"""
        self.gpio.setup(PIN_KEYPAD_ROW_0, self.gpio.OUT)
        self.gpio.setup(PIN_KEYPAD_ROW_1, self.gpio.OUT)
        self.gpio.setup(PIN_KEYPAD_ROW_2, self.gpio.OUT)
        self.gpio.setup(PIN_KEYPAD_ROW_3, self.gpio.OUT)

        self.gpio.setup(PIN_KEYPAD_COL_0, self.gpio.IN, state=self.gpio.LOW)
        self.gpio.setup(PIN_KEYPAD_COL_1, self.gpio.IN, state=self.gpio.LOW)
        self.gpio.setup(PIN_KEYPAD_COL_2, self.gpio.IN, state=self.gpio.LOW)

    def do_polling(self):
        """Check what key is pressed"""
        for i in range(3, 7):
            time.sleep(0.01)
            self.gpio.output(i, self.gpio.HIGH)
            for j in range(7, 10):
                if self.gpio.input(j) == self.gpio.HIGH:
                    # print((i-3, j-7))
                    return i - 3, j - 7

            self.gpio.output(i, self.gpio.LOW)
        return None

    def get_next_signal(self):
        """Loop until a key is pressed and released"""
        polling = None

        while True:
            temp_polling = self.do_polling()
            if temp_polling is not None:
                polling = temp_polling
                while self.do_polling() is not None:
                    pass
            if polling is not None:
                break

        return self.key_coord.get(polling)


def main():
    """Main"""
    keypad = Keypad()
    keypad.setup()
    print(keypad.get_next_signal())


if __name__ == "__main__":
    FILE = "password.txt"
    print(open(FILE, "r").read().strip() == "123")
    #main()
