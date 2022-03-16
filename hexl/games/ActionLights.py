import time
import numpy as np
from rpi_ws281x import Color

import collections
eventPile = collections.deque()
from hexl.core.LightController import LightController

class ActionLights(eventPile, LightController):

    INPUT_CHANNELS = 6
    COOLDOWN = 15
    previousState = np.zeros(INPUT_CHANNELS, dtype=np.int8)
    countdown = np.zeros(2, dtype=np.uint8)

    def play(self):
        while True:
            time.sleep(0.25)
            if len(eventPile) > 0:
                newEvent = eventPile.pop()
                changes = np.where(newEvent == 1)[0]
                for channel in changes:
                    self.countdown[channel] = self.COOLDOWN
            for channel, state in enumerate(self.countdown):
                if state > 0:
                    if state == 15:
                        LightController.pixelChange(channel, Color(255, 0, 0))
                    elif state == 10:
                        LightController.pixelChange(channel, Color(255, 100, 0))
                    elif state == 6:
                        LightController.pixelChange(channel, Color(150, 200, 0))
                    elif state == 1:
                        LightController.pixelOff(channel)

                countdown -= 1



