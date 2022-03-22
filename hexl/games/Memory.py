import time
import numpy as np
from rpi_ws281x import Color


# import collections
# eventPile = collections.deque()
# from hexl.core.LightController import LightController

class Memory:
    def __init__(self):
        self.INPUT_CHANNELS = 6
        self.TIMEOUT = 5
        self.LIVES = 3
        self.LEVEL = 1

    def generateSequence(self):
        self.sequence = np.random.randint(0, self.INPUT_CHANNELS, self.LEVEL)

    def displaySequence(self, LightController):
        time.sleep(1)
        for val in self.sequence:
            time.sleep(.4)
            LightController.pixelChange(val, (0,0,255))
            time.sleep(.8)
            LightController.pixelOff(val)

    def awaitInput(self, gameFreq, LightController, eventPile):
        colorWheel = ((0,255,0), (127,255,0), (255,255,0), (255,127,0), (255,0,0))
        eventPile.clear()
        wait = 0
        while wait < self.TIMEOUT:
            if eventPile:
                guess = np.where(eventPile.popleft() == 1)[0][0]
                LightController.pixelOff(6)
                return guess
            else:
                wait += gameFreq
                time.sleep(gameFreq)
                LightController.pixelChange(6, colorWheel[np.floor(wait)])
        LightController.pixelOff(6)
        return self.INPUT_CHANNELS

    def readInput(self, gameFreq, LightController, eventPile):
        for val in self.sequence:
            guess = self.awaitInput(gameFreq, eventPile)
            if guess == val:
                LightController.pixelChange(val, (0, 255, 0))
            else:
                LightController.pixelChange(val, (255, 0, 0))
                self.LIVES -= 1
                time.sleep(1)
                break
        self.LEVEL += 1
        self.LEVEL_COMPLETE = True


    def play(self, gameFreq, LightController, eventPile):

        while self.LIVES > 0:
            self.generateSequence(self)
            self.LEVEL_COMPLETE = False
            while not self.LEVEL_COMPLETE & self.LIVES > 0:
                self.displaySequence(self, LightController)
                self.readInput(self, gameFreq, LightController, eventPile)
        if self.LEVEL == 10:
            LightController.celebrate()
        else:
            LightController.death()


