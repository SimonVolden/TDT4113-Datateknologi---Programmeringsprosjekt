from datetime import datetime
import time
from GPIOSimulator_v1 import *
GPIO = GPIOSimulator()
GPIO.setup(PIN_BTN, GPIO.IN, GPIO.PUD_DOWN)

lastThreeSignals = []



for i in range(2000):

    
    time.sleep(0.3)
    state = str(GPIO.input(PIN_BTN))

                lastThreeSignals.append(state)

    else:
        lastThreeSignals.pop(0)
        lastThreeSignals.append(state)

    print(state)
    print(lastThreeSignals)


print(str(datetime.now())[11:])
