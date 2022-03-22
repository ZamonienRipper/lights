import time
from rpi_ws281x import PixelStrip, Color

# LED strip configuration:
LED_COUNT = 12        # Number of LED pixels.
LED_PIN = 21          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 10  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_INDEXES = [[0], [1, 2, 3], [4], [5, 6, 7], [8], [9, 10, 11]]
LED_INDEXES = [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11]]
wait_ms = 50

class LightController:
    def col(self, color):
        #print(f"color0: {color[0]}")
        #print(f"color1: {color[1]}")
        #print(f"color2: {color[2]}")
        return Color(color[0], color[1], color[2])

    def __init__(self):
        self.strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()

    def pixelChange(self, pixel, color):
        for led in LED_INDEXES[pixel]:
            self.strip.setPixelColor(led, self.col(color))
        self.strip.show()

    def pixelsChange(self, pixels, colors):
        #print(f"pixels: {pixels}")
        #print(f"colors: {colors}")
        for i, pixel in enumerate(pixels):
            for led in LED_INDEXES[pixel]:
                self.strip.setPixelColor(led, self.col(colors[i]))
        self.strip.show()

    def pixelOff(self, pixel):
        for led in LED_INDEXES[pixel]:
            self.strip.setPixelColor(led, Color(0, 0, 0))
        self.strip.show()

    def colorWipe(self, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, self.col(color))
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def celebrate(self):
        celebrationColors = ((0,255,0),(0,0,255),(0,255,0),(0,0,255),(0,255,0),(0,0,255),(0,0,0))
        for color in celebrationColors:
            self.colorWipe(color)

    def death(self):
        deathColors = ((255,0,0),(0,0,0),(255,0,0),(0,0,0),(255,0,0),(0,0,0),(255,0,0),(0,0,0))
        for color in deathColors:
            self.colorWipe(color)

