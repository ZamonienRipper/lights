import numpy as np

import collections
#eventPile = collections.deque()
from hexl.deps.ADS1256 import ADS1256

class StepUpDetector:        

    def updateSensorData(self):
        self.ADCValues = np.array(self.ADC.ADS1256_GetHex()) * 5.0 / 0x7fffff
        self.dataPile.append(self.ADCValues)
        #print(self.ADCValues)

    def __init__(self):
        #self.eventPile = eventPile
        self.dataPileSize = 5
        self.sensitivity = 1
        self.dataPile = collections.deque([], maxlen=self.dataPileSize)

        self.ADC = ADS1256()
        self.ADC.ADS1256_init()
        while len(self.dataPile) < self.dataPileSize:
            self.updateSensorData()
            print(self.dataPile[-1])

    def updateEvents(self, eventPile):
        self.updateSensorData()

        delta = self.dataPile[0] - self.dataPile[-1]
        flags = np.array((delta > self.sensitivity), dtype='uint8')
        #print(f"sum of flags: {flags.sum()}")
        #print(f"flags: {flags}")
        if flags.sum():
            eventPile.append(flags)
            print(len(eventPile))
            #print(eventPile)
            #print(f"EvenPile inside updateEvents: {eventPile}")
            changes = np.where(flags == 1)[0]
            #print(f"data in: {np.around(self.dataPile, decimals = 2)}")
            for channel in changes:
                newVal = self.dataPile[-1][channel]
                #print(self.dataPile)
                for i in range(0, self.dataPileSize-1):
                    self.dataPile[i][channel] = newVal
            #print(f"data out: {np.around(self.dataPile, decimals = 2)}")






