import time
import numpy as np
from collections import deque

class DebugMode:
    def __init__(self):
        self.INPUT_CHANNELS = 6
        self.COOLDOWN = 15
        self.previousState = np.zeros(self.INPUT_CHANNELS, dtype=np.int8)
        self.countdown = np.zeros(self.INPUT_CHANNELS, dtype=np.uint8)
        
    def play(self, gameFreq, LightController, eventPile):
        def decrement(array):
            result = np.array(np.sqrt((array-1)*array),dtype=np.uint8)
            return result
        history = deque([0,0, self.INPUT_CHANNELS], maxlen=3)
        print("Welcome to Debug Mode\n")
        print("Explain\n")
        #print('ENTERING GAME')
        while True:
            time.sleep(gameFreq)
            inputs = input("Input pixels to light up/turn off\n")
            if inputs == "exit":
                LightController.colorWipeFast((0, 0, 0), 10)
                break
            split = inputs.split(" ")
            on = split[0]
            ons = on.split(",")
            for on in ons:
                LightController.pixelChange(int(on), (255, 255, 255))
            if len(split) > 1:
                off = split[1]
                offs = off.split(",")
                for off in offs:
                    LightController.pixelChange(int(off), (0, 0, 0))
            if len(split) > 2:
                blue = split[2]
                blues = blue.split(",")
                for blue in blues:
                    LightController.pixelChange(int(blue), (0, 0, 255))
