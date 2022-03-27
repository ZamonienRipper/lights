import time
import datetime

class HexClock:
    def __init__(self):
        self.colorfull = False
        self.indexMap = [[0], [0, 1], [1], [1, 2], [2], [2, 3], [3], [3, 4], [4], [4, 5], [5], [5, 0]]

    def play(self, gameFreq, LightController, eventPile):
        minuteColor = (255,255,255)
        hourColor = (255,255,255)

        while True:
            now = datetime.datetime.now()

            nowHour = round(now.hour % 12)
            nowMinute = round(now.minute / 5)

            hourLEDs = self.indexMap[nowHour]
            minuteLEDs = self.indexMap[nowMinute]

            LightController.bandChange('inner', hourLEDs, [hourColor]*len(hourLEDs))
            LightController.bandChange('outer', minuteLEDs, [minuteColor]*len(minuteLEDs))

            time.sleep(5)

