import time
import numpy as np

class Memory:
    def __init__(self):
        self.INPUT_CHANNELS = 6
        self.INDICATOR_LED = 12
        self.TIMEOUT = 5
        self.LIVES = 3
        self.LEVEL = 1
        self.WIN = 11
        self.VAL_ON = 1
        self.VAL_OFF = 0.5
        self.LINGER = 0.25
        self.WAIT = 0.75

    def generateSequence(self):
        self.sequence = np.random.randint(0, self.INPUT_CHANNELS, self.WIN)

    def displaySequence(self, LightController):
        time.sleep(self.WAIT)
        for val in self.sequence[:self.LEVEL]:
            time.sleep(self.VAL_OFF)
            LightController.pixelChange(val + self.INPUT_CHANNELS, (0,0,255))
            time.sleep(self.VAL_ON)
            LightController.pixelOff(val + self.INPUT_CHANNELS)

    def awaitInput(self, gameFreq, LightController, eventPile):
        colorWheel = ((0,255,0), (127,255,0), (255,255,0), (255,127,0), (255,0,0))
        eventPile.clear()
        wait = 0
        while wait < self.TIMEOUT:
            if eventPile:
                guess = np.where(eventPile.popleft() == 1)[0][0]
                LightController.pixelOff(self.INDICATOR_LED)
                print("Correct sequence input!")
                return guess
            else:
                #print(f"Warning components: wait: {wait}, floor: {np.floor(wait).astype(np.int8)}")
                #print(f"Warning color: {colorWheel[np.floor(wait).astype(np.int8)]}")
                LightController.pixelChange(self.INDICATOR_LED, colorWheel[np.floor(wait).astype(np.int8)])
                wait += gameFreq
                time.sleep(gameFreq)
        LightController.pixelOff(self.INDICATOR_LED)
        print("No input given. Timeout reached")
        return self.INPUT_CHANNELS

    def readInput(self, gameFreq, LightController, eventPile):
        incorrect = 0
        for val in self.sequence[:self.LEVEL]:
            guess = self.awaitInput(gameFreq, LightController, eventPile)
            if guess == self.INPUT_CHANNELS:
                LightController.pixelChange(val, (255, 0, 0))
                print("No input given. Timeout reached")
                self.LIVES -= 1
                incorrect = 1
                time.sleep(self.WAIT)
                LightController.colorWipeFast((255,0,0))
                LightController.offWipeFast()
                time.sleep(self.WAIT)
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
                time.sleep(.1)
                LightController.colorWipeFast((255,0,0))
                LightController.offWipeFast()
                time.sleep(self.WAIT)
                break
        if not incorrect:
            self.LEVEL += 1
            self.LEVEL_COMPLETE = True


    def play(self, gameFreq, LightController, eventPile):
        self.generateSequence()
        while self.LIVES > 0:
            
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
            if self.LEVEL == self.WIN:
                print("You completed level 10!!")
                LightController.celebrate()
                break
        print("Game over")
        LightController.death()


