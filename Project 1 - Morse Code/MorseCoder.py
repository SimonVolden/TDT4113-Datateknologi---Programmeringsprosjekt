""" Template for Project 1: Morse code """

from GPIOSimulator_v1 import *
GPIO = GPIOSimulator()
GPIO.setup(PIN_BTN, GPIO.IN, GPIO.PUD_DOWN)
from datetime import datetime
import time
FMT = '%H:%M:%S.%f'

MORSE_CODE = {'.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd', '.': 'e', '..-.': 'f', '--.': 'g',
              '....': 'h', '..': 'i', '.---': 'j', '-.-': 'k', '.-..': 'l', '--': 'm', '-.': 'n',
              '---': 'o', '.--.': 'p', '--.-': 'q', '.-.': 'r', '...': 's', '-': 't', '..-': 'u',
              '...-': 'v', '.--': 'w', '-..-': 'x', '-.--': 'y', '--..': 'z', '.----': '1',
              '..---': '2', '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7',
              '---..': '8', '----.': '9', '-----': '0'}

class MorseDecoder():
    """ Morse code class """
    def __init__(self):
        """ initialize your class """
        #Variables for keeping track of time between presses and duration of the press
        self.timeStartPress = ""
        self.timeStopPress = ""
        self.timePauseStart = ""
        self.timePauseStop = ""

        #List for keeping track of the last 3 signals (1 or 0)
        #to reduce the chance that an incorrect bit gets processed
        self.lastThreeSignals = []

        #Boolean to confirm that the button is pressed
        self.pressed = None
        #Boolean to keep track of if the current signal is fully processed or not
        #Is False if spacebar has been pressed but not released, and True if when released
        self.finishedSignal = False
        #Boolean to keep track of the pause betwwen presses,
        #is False after space is released, and True when space is pressed again.
        self.pauseFinished = None

        #Keeps track of the current symbol (string of . and -)
        self.currentSymbol = ""
        #Keeps tracks of current word (string of letters)
        self.currentWord = ""
        #Keeps track of all the words written
        self.currentSentence = ""
        #Variable used for testing, stores all letters written
        self.letters = []

    def read_one_signal(self):
        """ read a signal from Raspberry Pi """
        if self.finishedSignal == True:
            self.finishedSignal = False

            #Gets the duration of the press as a string
            tdelta = str(datetime.strptime(self.timeStopPress, FMT)
                         - datetime.strptime(self.timeStartPress, FMT))
            self.restartTime()
            seconds = float(tdelta[5:])

            #If the duration of the press is less than 0.4 seconds, it is a (.)
            if seconds < 0.4:
                #print(tdelta)
                #print(float(tdelta[5:]))
                self.process_signal(".")
                return "."

            #If it is between 0.4 and 2.0 seconds, its a (-)
            if (seconds < 2.0 and seconds > 0.4):
                #print(tdelta)
                #print(seconds)
                self.process_signal("-")
                return "-"

            else:
                return ""

        if self.pauseFinished == True:

            #Gets the duration of the pause between presses
            tdelta = str(datetime.strptime(self.timePauseStop, FMT) - datetime.strptime(self.timePauseStart, FMT))
            seconds = float(tdelta[5:])
            self.restartPause()

            #If the pause is less than 1. second, its a pause between (.) and (-)
            if (seconds < 1.0):
                return ""

            #If the pause is between 1.0 and 3.0 seconds its the end of a symbol (letter or number)
            if (seconds > 1.0 and seconds < 3.0):
                print("symbol end")
                self.handle_symbol_end()

            #If the pause is longer than 3.0 seconds, its the end of a word    
            if (seconds > 3.0):
                print("word end")
                self.handle_symbol_end()
                self.handle_word_end() 
                 
        else:
            return ""

    def restartTime(self):
        self.timeStartPress = ""
        self.timeStopPress = ""
    
    def restartPause(self):
        self.timePauseStart = ""
        self.timePauseStop = ""
        self.pauseFinished = None

    def decoding_loop(self):
        """ the main decoding loop """

        while(True):

            #time between each loop
            time.sleep(0.01)
            #Gets the state of the spacebar
            state = str(GPIO.input(PIN_BTN))

            #Updates lastThreeSignals with the current state
            if (len(self.lastThreeSignals) < 3):
                self.lastThreeSignals.append(state)

            else:
                self.lastThreeSignals.pop(0)
                self.lastThreeSignals.append(state)

            #Checks if the last three signals are "1" (spacebar pressed) and that the timer for the press hasn't already started
            if (self.lastThreeSignals == ["1", "1", "1"] and self.timeStartPress == "" ):

                #Gets the the current time in the format "HH:MM:SS.000000" to get an accurate time between space down and space up
                self.timeStartPress = str(datetime.now())[11:]

                self.pressed = True
                #Sets the variable finishedSignal false, as this is the start of the signal
                self.finishedSignal = False
                
                #Checks if the pause timer has been started, if so, it stops it and sets pauseFinished as True
                if (self.timePauseStart != ""):
                    self.timePauseStop = str(datetime.now())[11:]
                    self.pauseFinished = True

            #Checks if the last three signals are "0", and if the spacebar has been pressed in the current signal cycle
            #This is to make sure that it doesnt start when there is a long sequence of zeroes.
            if (self.lastThreeSignals == ["0", "0", "0"] and self.pressed == True):
                #Gets the current time
                self.timeStopPress = str(datetime.now())[11:]
                #Sets pressed as false, so ready for a new cycle
                self.pressed = False
                #The current signal is finished, so it sets finishedSignal as True
                self.finishedSignal = True

                #Starts the pause timer, to keep track of how long the pause is
                self.timePauseStart = str(datetime.now())[11:]
                #pauseFinished = False, as this is the start of the pause
                self.pauseFinished = False

            #Prints the current signal, if its not blank, to make it easier for the user to see the input
            signal = self.read_one_signal()
            if (signal != ""): 
                print(signal)


    def process_signal(self, signal):
        """ handle the signals using corresponding functions """
        self.currentSymbol = self.currentSymbol + signal

    def update_current_symbol(self, signal):
        """ append the signal to current symbol code """
        self.currentSymbol = self.currentSymbol + signal

    def handle_symbol_end(self):
        """ process when a symbol ending appears """
        if (MORSE_CODE.__contains__(self.currentSymbol)):
            self.currentWord = self.currentWord + MORSE_CODE[self.currentSymbol]
            self.letters.append(MORSE_CODE[self.currentSymbol])
        else:
            print("No such symbol")
        self.currentSymbol = ""

    def handle_word_end(self):
        """ process when a word ending appears """
        self.currentSentence = self.currentSentence + " " + self.currentWord
        self.currentWord = ""

    def handle_reset(self):
        """ process when a reset signal received """
        self.timeStartPress = ""
        self.timeStopPress = ""
        self.timePauseStart = ""
        self.timePauseStop = ""
        self.lastThreeSignals = []
        self.pressed = None
        self.finishedSignal = False
        self.pauseFinished = None
        self.currentSymbol = ""
        self.currentWord = ""
        self.currentSentence = ""

    def show_message(self):
        """ print the decoded message """
        print(self.currentSentence)

def main():
    """ the main function """
    try:
        m = MorseDecoder()
        m.decoding_loop()
    except KeyboardInterrupt:
        print("Keyboard interrupt: quit the program")
    finally:
        #Makes sure that the last symbol is finished
        if (m.timePauseStart != ""):
            m.timePauseStop = str(datetime.now())[11:]
            m.pauseFinished = True
            m.read_one_signal()

        #Prints the current word, the current sentence and all written letters after the loop
        print(m.currentWord)
        print(m.currentSentence)
        #print(m.letters)
        GPIO.cleanup()



if __name__ == "__main__":
    main()

