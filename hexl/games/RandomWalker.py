import numpy as np
import collections
import time

class RandomWalker:
    def __init__(self):
        self.colorfull = False
        self.multiMode = False
        self.tail = [(0,0,255), (0,128,255), (0,255,255), (255,255,255)]
        self.history = np.zeros(2)
        self.state[-1] = 1
        self.inner = [1,2,3,4,5,6]
        self.outer = [7,8,9,10,11,12]
        self.walker = collections.deque([], maxlen=self.len(self.tail))
        for elem in self.tail:
            self.walker.append(0)
        print(self.walker)

    def getRing(self, id):
        if id == 0:
            return 0
        elif id < 7:
            return 1
        else:
            return 2

    def options(self):
        now = self.history[0]
        last = self.history[1]
        if now == 0:
            if last == 1:
                return self.inner.remove(self.walker[1])
            else:
                return self.inner
        elif now == 1:
            if last == 0:
                return [-1, +1, +6]
            elif last == 1:
                return [-6, self.walker[0]-self.walker[1], +6]
            else:
                return [-6, -1, +1]
        else:
            if last == 1:
                return [-1, +1]
            else:
                return [-6, self.walker[0]-self.walker[1]]

    def move(self, pos, dir):
        if pos == 0:
            return pos + dir
        elif pos == 1:
            if dir == -1:
                return 6
            else:
                return pos + dir
        elif pos == 6:
            if dir == +1:
                return 1
            else:
                return pos + dir
        elif pos == 7:
            if dir == -1:
                return 12
            else:
                return pos + dir
        elif pos == 12:
            if dir == +1:
                return 7
            else:
                return pos + dir
        else:
            return pos + dir

    def iterate(self):
        direction = np.random.choice(self.options())
        next = self.move(self.walker[0], direction)
        self.walker.append(next)

    def play(self, gameFreq, LightController, eventPile):

        eventPile.clear()

        while True:

            self.iterate()
            LightController.pixelsChange(self.walker, self.tail)
            time.sleep(.5)

            if eventPile:
                LightController.colorWipe((0, 0, 0))
                break