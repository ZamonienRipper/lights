import numpy as np
import collections
import time

class RandomWalker:
    def __init__(self):
        self.colorfull = False
        self.multiMode = False
        self.grid = {12:[0,1,2,3,4,5], 0:[1,5,6,12], 1:[0,2,7,12], 2:[1,3,8,12], 3:[2,4,9,12], 4:[3,5,10,12], 5:[4,0,11,12], 6:[0,7,11], 7:[1,6,8], 8:[2,7,9], 9:[3,8,10], 10:[4,9,11], 11:[5,6,10]}
        self.tail = [(255,255,255), (0,255,255), (0,50,255), (0,0,255)]
        self.tail = [(255,255,255), (255,255,0), (255,128,0), (255,0,0)] 
        self.history = collections.deque([0, 0], maxlen=2)
        self.inner = [0,1,2,3,4,5]
        self.outer = [6,7,8,9,10,11]
        self.walker = collections.deque([], maxlen=len(self.tail))
        for elem in self.tail:
            self.walker.append(12)
        print(self.walker)

    def getRing(self, id):
        if id == 12:
            return 0
        elif id < 6:
            return 1
        else:
            return 2

    def options(self):
        now = self.walker[-1]
        last = self.walker[-2]
        options = self.grid[now]
        if last in options:
            options.remove(last)
        return options
        

    def move(self, options):
        return np.random.choice(options)

    def iterate(self):

        options = self.options()
        next = self.move(options)

        self.walker.append(next)

    def play(self, gameFreq, LightController, eventPile):
        direction = 0
        eventPile.clear()

        while True:

            self.iterate()
            LightController.pixelsChange(self.walker, self.tail)
            time.sleep(1)

            if eventPile:
                LightController.colorWipe((0, 0, 0))
                break