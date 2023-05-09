import numpy as np
import collections
from collections import deque
import time

class RandomWalker:
    def __init__(self):
        self.colorful = False
        self.suits = 2
        self.gaming = True
        self.fields = [0,1,2,3,4,5,6,7,8,9,10,11,12]
        self.grid = {12:0, 0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0}
        self.colors = [(0,0,0), (0,255,0), (0,0,255)]
        self.inner = deque([2,1,0,5,4,3], maxlen=6)
        self.outer = [6,7,8,9,10,11]

    def randomize_grid(self):
        prev = 1
        for key in self.grid:
            if prev == 1:
                self.grid[key] = 2
                prev = 2
            elif prev == 2:
                self.grid[key] = 1
                prev = 1

    def rotate_grid(self, dir, clockwise):
        next = self.grid.copy()
        active = deque([99, 99, 99, 99], maxlen=4)
        active[0] = 12
        active[2] = dir + 6
        if self.inner.index(dir) in [0,5]:
            self.inner.rotate(2)
        pos = self.inner.index(dir)
        if clockwise:
            active[1] = self.inner[pos+1]
            active[3] = self.inner[pos-1]
        else:
            active[1] = self.inner[pos - 1]
            active[3] = self.inner[pos + 1]

        for elem in [0,0,0,0]:
            next[active[elem]] = self.grid[active[elem]+1]
            active.rotate(-1)

    def update_light(self, LightController):
        pixels = []
        colors = []
        for i, key in enumerate(self.grid.keys()):
            pixels.append(key)
            colors.append(self.colors[self.grid[key]])
        LightController.pixelsChange(pixels, colors)

    def getInput(self, gameFreq, LightController, eventPile):
        colorWheel = ((0,255,0), (127,255,0), (255,255,0), (255,127,0), (255,0,0))
        eventPile.clear()
        wait = 1
        while wait:
            if eventPile:
                direction = np.where(eventPile.popleft() == 1)[0][0]
                LightController.pixelChange(direction, (255,255,255))
                time.sleep(1)
                LightController.pixelsChange(direction, self.colors[self.grid[direction]])
                return direction
            else:
                #print(f"Warning components: wait: {wait}, floor: {np.floor(wait).astype(np.int8)}")
                #print(f"Warning color: {colorWheel[np.floor(wait).astype(np.int8)]}")
                LightController.pixelChange(self.INDICATOR_LED, colorWheel[np.floor(wait).astype(np.int8)])
                wait += gameFreq
                time.sleep(gameFreq)
        LightController.pixelOff(self.INDICATOR_LED)
        return self.INPUT_CHANNELS

    def play(self, gameFreq, LightController, eventPile):
        self.randomize_grid()
        while self.gaming:
            dir = self.getInput(gameFreq, LightController, eventPile)
            self.rotate_grid(dir, True)
            self.update_light(LightController)

