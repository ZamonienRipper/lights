from abc import ABC, abstractmethod
import time

class LightControllerParent:
    """Parent class for LightController and LightSimulator"""
    
    def __init__(self):
        self.strip = None
        self.bandsDict = {}
        self.pixelsDict = {}
        self.LED_INDEXES = []
        
    @abstractmethod
    def col(self, color):
        pass
      
    def pixelList(self, band):
        """Create list of all pixels in specified band"""
        targets = self.bandsDict[band]
        pixels = []
        for target in targets:
            pixels.append(self.LED_INDEXES[target])
        pixelList = [item for sublist in pixels for item in sublist]
        return pixelList
        
    def pixelChange(self, pixel, color):
        """Cahnge color of one specified pixel"""
        for led in self.LED_INDEXES[pixel]:
            self.strip.setPixelColor(led, self.col(color))
        self.strip.show()

    def pixelsChange(self, pixels, colors):
        """Change color of specified pixels"""
        #print(f"pixels: {pixels}")
        #print(f"colors: {colors}")
        for i, pixel in enumerate(pixels):
            for led in self.LED_INDEXES[pixel]:
                self.strip.setPixelColor(led, self.col(colors[i]))
        self.strip.show()

    def bandChange(self, band, pixels, colors, wipeFirst=True):
        """Change color of all pixels in specified band"""
        targets = self.bandsDict[band]
        if wipeFirst:
            self.bandOff(band, active=False)
        for i, pixel in enumerate(pixels):
            for led in self.LED_INDEXES[targets[pixel]]:
                self.strip.setPixelColor(led, self.col(colors[i]))
        self.strip.show()

    def pixelOff(self, pixel, active=True):
        """Turn off specified pixel"""
        for led in self.LED_INDEXES[pixel]:
            self.strip.setPixelColor(led, self.col((0, 0, 0)))
        if active:
            self.strip.show()

    def bandOff(self, band, active=True):
        """Turn off all pixels in specified band"""
        targets = self.pixelsDict[band]
        for led in targets:
            self.strip.setPixelColor(led, self.col((0, 0, 0)))
        if active:
            self.strip.show()

    def colorWipe(self, color, wait_ms=50):
        """Wipe color across display a LED at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, self.col(color))
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def colorWipeFast(self, color, wait_ms=150):
        """Wipe color across display a pixel at a time"""
        for pixel in self.LED_INDEXES:
            print(f"Turing on LEDs {pixel}")
            for led in pixel:
                self.strip.setPixelColor(led, self.col(color))
            self.strip.show()
            time.sleep(wait_ms / 1000.0)
            
    def offWipeFast(self, wait_ms=150):
        """Turn off display a pixel at a time"""
        for i, indeces in enumerate(self.LED_INDEXES):
            print(f"Turing off pixel {i}, which contains leds {indeces}")
            self.pixelOff(i)
            time.sleep(wait_ms / 1000.0)

    def celebrate(self):
        """Wipe festive colors across display a pixel at a time"""
        celebrationColors = ((0,255,0),(0,0,255),(0,255,0),(0,0,255),(0,0,0))
        for color in celebrationColors:
            self.colorWipeFast(color)

    def death(self):
        """Wipe ominous colors across display a pixel at a time"""
        deathColors = ((255,0,0),(0,0,0),(255,0,0),(0,0,0))
        for color in deathColors:
            self.colorWipeFast(color)