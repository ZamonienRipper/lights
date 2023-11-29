import time
from rpi_ws281x import PixelStrip, Color
from hexl.core.LightControllerParent import LightControllerParent

# LED strip configuration:
LED_COUNT = 144        # Number of LED pixels.
LED_PIN = 21          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255   # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
#LED_INDEXES = [[0], [1, 2, 3], [4], [5, 6, 7], [8], [0, 1, 2]]
#LED_INDEXES = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [13, 14, 16, 17, 19, 20], [0], [1], [2], [3], [4], [5], [0], [1], [2], [3], [4], [5], [0], [1], [2], [3], [4]]
#LED_INDEXES = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17], [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35], [36, 37, 38], [39, 40, 41], [0], [1], [2], [3], [4], [5], [0], [1], [2], [3], [4], [5], [0], [1], [2], [3], [4]]
#LED_INDEXES = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0], [1], [2], [3], [4], [5]]
#LED_INDEXES = [[4, 5, 7, 8, 10, 11], [4], [5], [7], [8], [10], [11], [5], [7], [8], [10], [11]]
#LED_INDEXES = [[18,19,20],[21,22,23],[24,25,26],[27,28,29],[30,31,32],[33,34,35],[36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53],[54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71],[72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89],[90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107],[108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125],[126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143],[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]]
LED_INDEXES = [[21,22,23],[18,19,20],[33,34,35],[30,31,32],[27,28,29],[24,25,26],[54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71],[36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53],[126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143],[108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125],[90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107],[72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89],[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]]
LED_INDEXES = [[21,22,23],[18,19,20],[33,34,35],[30,31,32],[27,28,29],[24,25,26],[54,56,58,60,62,64,66,68,70],[36,38,40,42,44,46,48,50,52],[126,128,130,132,134,136,138,140,142],[108,110,112,114,116,118,120,122,124],[90,92,94,96,98,100,102,104,106],[72,74,76,78,80,82,84,86,88],[0,2,4,6,8,10,12,14,16]]
LED_INDEXES_OUTER = [6, 7, 8, 9, 10, 11]
LED_INDEXES_INNER = [0, 1, 2, 3, 4, 5]
wait_ms = 50

class LightController(LightControllerParent):
    def col(self, color):
        """Returns strip-readable color code from RGB components"""
        #print(f"color0: {color[0]}")
        #print(f"color1: {color[1]}")
        #print(f"color2: {color[2]}")
        return Color(color[0], color[1], color[2])

    def __init__(self):
        self.strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()
        self.bandsDict = {'outer': LED_INDEXES_OUTER, 'inner': LED_INDEXES_INNER}
        self.pixelsDict = {'outer': self.pixelList('outer'), 'inner': self.pixelList('inner')}
        self.LED_INDEXES = LED_INDEXES
        print(f"bandsDict: {self.bandsDict}")
        print(f"pixelsDict: {self.pixelsDict}")


