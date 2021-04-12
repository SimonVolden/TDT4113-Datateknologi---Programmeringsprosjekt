""" LEDBOARD charlieplexing class
    With this class, we can simulate how to light 6 LEDs with 3 pins
"""
import time

from GPIOSimulator_v5 import GPIOSimulator


class LedBoard:
    """ledBoard main class """

    def __init__(self):
        self.gpio = GPIOSimulator() # start the simulator instance
        self.states = [ # the state of each led, given by the index
            [1, 0, -1], #light up led0, pin 0 has state 0, pin 1 has state 0 and pin 2 has state -1
            [0, 1, -1],
            [-1, 1, 0],
            [-1, 0, 1],
            [1, -1, 0],
            [0, -1, 1]
        ]


    def show_lights(self):
        """ Shows if each led is on or off """
        self.gpio.show_leds_states()

    def all_off(self):
        """ turns off all leds """
        self.set_pin(0, -1)
        self.set_pin(1, -1)
        self.set_pin(2, -1)

    def set_pin(self, pin, pin_state):
        """ sets each pin, is used to turn a led on or off """
        if pin_state == -1:
            self.gpio.setup(pin, self.gpio.IN)
        else:
            self.gpio.setup(pin, self.gpio.OUT)
            self.gpio.output(pin, pin_state)

    def light_led(self, led_num, duration=None):
        """ light a specified led for a specified duration, then turns them all off"""
        state = self.states[led_num]
        for i in range(0,3):
            self.set_pin(i, state[i])
        self.show_lights()
        if duration is not None:
            time.sleep(duration)
        self.all_off()

    def startup_show(self):
        """ startup sequence, twinkle up and down """
        self.flash_all(1)
        time.sleep(0.3)
        self.light_led(3,0.3)

    def shutdown_show(self):
        """ shutdown sequence, twinkle down and up """
        self.light_led(3,0.3)
        time.sleep(0.3)
        self.flash_all(1)

    def flash_all(self, k):
        """ flash all led, implemented by twinkling in a rapid succession """
        for _ in range(k*5):
            for i in range(0,6):
                self.light_led(i, 0.03)

    def twinkle(self, k):
        """ twinkle all lights in a slower succession """
        for _ in range(k):
            for i in range(0,6):
                self.light_led(i, 0.16)

def main():
    """ the main function """
    try:
        led = LedBoard()
        led.all_off()
        led.show_lights()
        led.light_led(3)
        led.show_lights()
        print("startup")
        led.startup_show()
        print("shutdown")
        led.shutdown_show()
        print("flash")
        led.flash_all(1)
        print("twinkle")
        led.twinkle(0.5)
        led.light_led(3,3)
        led.flash_all(1)
        #led.light_led(0, 2)
        led.twinkle(4)
        print("done")
    except KeyboardInterrupt:
        print("Keyboard interrupt; quit the program.")
    finally:
        led.gpio.cleanup()


if __name__ == "__main__":
    main()
