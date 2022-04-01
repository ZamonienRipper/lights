import time
import numpy as np

class Memory:
    def __init__(self):
        self.INPUT_CHANNELS = 3
        self.TIMEOUT = 5
        self.LIVES = 3
        self.LEVEL = 1
        self.VAL_ON = 1.2
        self.VAL_OFF = .5
        self.LINGER = .75
        self.WAIT = 0.75

    def generateSequence(self):
        self.sequence = np.random.randint(0, self.INPUT_CHANNELS, self.LEVEL)

    def displaySequence(self, LightController):
        time.sleep(1)
        for val in self.sequence:
            time.sleep(self.VAL_OFF)
            LightController.pixelChange(val, (0,0,255))
            time.sleep(self.VAL_ON)
            LightController.pixelOff(val)

    def awaitInput(self, gameFreq, LightController, eventPile):
        colorWheel = ((0,255,0), (127,255,0), (255,255,0), (255,127,0), (255,0,0))
        eventPile.clear()
        wait = 0
        while wait < self.TIMEOUT:
            if eventPile:
                guess = np.where(eventPile.popleft() == 1)[0][0]
                LightController.pixelOff(6)
                print("Correct sequence input!")
                return guess
            else:
                #print(f"Warning components: wait: {wait}, floor: {np.floor(wait).astype(np.int8)}")
                #print(f"Warning color: {colorWheel[np.floor(wait).astype(np.int8)]}")
                LightController.pixelChange(6, colorWheel[np.floor(wait).astype(np.int8)])
                wait += gameFreq
                time.sleep(gameFreq)
        LightController.pixelOff(6)
        print("No input given. Timeout reached")
        return self.INPUT_CHANNELS

    def readInput(self, gameFreq, LightController, eventPile):
        incorrect = 0
        for val in self.sequence:
            guess = self.awaitInput(gameFreq, LightController, eventPile)
            if guess == self.INPUT_CHANNELS:
                LightController.pixelChange(val, (255, 0, 0))
                print("No input given. Timeout reached")
                self.LIVES -= 1
                incorrect = 1
                time.sleep(1)
                LightController.colorWipe((255,0,0))
                LightController.colorWipe((0,0,0))
                time.sleep(1)
            elif guess == val:
                LightController.pixelChange(val, (0, 255, 0))
                print("Correct sequence value")
                time.sleep(self.LINGER)
                LightController.pixelOff(val)
            else:
                LightController.pixelsChange([guess, val], [(255,0,0), (0,255,0)])
                print("Incorrect sequence input! Lost 1 life")
                self.LIVES -= 1
                incorrect = 1
                time.sleep(1)
                LightController.colorWipe((255,0,0))
                LightController.colorWipe((0,0,0))
                time.sleep(1)
                break
        if not incorrect:
            self.LEVEL += 1
            self.LEVEL_COMPLETE = True


    def play(self, gameFreq, LightController, eventPile):

        while self.LIVES > 0:
            self.generateSequence()
            print(f"Current sequence is: {self.sequence}")
            self.LEVEL_COMPLETE = False
            while (not self.LEVEL_COMPLETE) & (self.LIVES > 0):
                print(f"About to display sequence.")
                print(f"Current lives: {self.LIVES}")
                print(f"Current level: {self.LEVEL}")
                self.displaySequence(LightController)
                time.sleep(self.WAIT)
                print(f"Ready for input. Repeat the pattern")
                self.readInput(gameFreq, LightController, eventPile)
        if self.LEVEL == 10:
            print("You reached level 10!!")
            LightController.celebrate()
        else:
            print("Game over")
            LightController.death()


