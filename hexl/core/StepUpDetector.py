import numpy as np

import collections
eventPile = collections.deque()
from hexl.deps.ADS1256 import ADS1256

class StepUpDetector(eventPile):

    dataPileSize = 5
    sensitivity = 1
    dataPile = collections.deque([], maxlen=dataPileSize)

    ADC = ADS1256()
    ADC.ADS1256_init()

    def updateSensorData(self):
        ADCValues = np.array(self.ADC.ADS1256_GetHex()) * 5.0 / 0x7fffff
        self.dataPile.append(ADCValues)

    def __init__(self):
        while len(self.dataPile) < self.dataPileSize:
            self.updateSensorData()

    def updateEvents(self):
        self.updateSensorData()

        delta = self.dataPile[0] - self.dataPile[-1]
        flags = np.array((delta > self.sensitivity), dtype='uint8')
        if flags.sum:
            eventPile.append(flags)
            changes = np.where(flags == 1)[0]
            for channel in changes:
                newVal = self.dataPile[0][channel]
                for i in self.dataPile[1:]:
                    self.dataPile[i][channel] = newVal







