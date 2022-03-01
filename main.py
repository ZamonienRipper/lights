
import time
from rpi_ws281x import PixelStrip, Color
import argparse
from dependencies.ADS1256_package import ADS1256 as ADS1256
import RPi.GPIO as GPIO
import queue
import threading
from collections import deque
import numpy as np

# LED strip configuration:
LED_COUNT = 12         # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_INDEXES = [[0],[1,2,3],[4],[5,6,7],[8],[9,10,11]]

sensitivity = 1

sensorPile = deque([0]*5,maxlen=100)
eventsPile = deque([0]*5,maxlen=10000)

ADC = ADS1256()
ADC.ADS1256_init()

def getSensorData():
    time.sleep(1)

    class ReadADC:
        ADCValue = ADC.ADS1256_GetAll()
    return ReadADC

def sensorThread():
    global connected
    while connected:
        sensorPile.append(np.array(getSensorData()))


def calculateEvents():
    time.sleep(1)

    class calcEvents:
        d = sensorPile[4] - sensorPile[0]
        flags = (d > sensitivity)
    return calcEvents


def flagThread():
    global connected
    while connected:
        eventsPile.append(calculateEvents())

def actions():
    events = eventsPile.pop()
    print ("0 ADC = %ld"%(events[0]))
    print ("1 ADC = %ld"%(events[1]))
    print ("2 ADC = %ld"%(events[2]))
    print ("3 ADC = %ld"%(events[3]))
    print ("4 ADC = %ld"%(events[4]))
    print ("5 ADC = %ld"%(events[5]))
    print ("6 ADC = %ld"%(events[6]))
    print ("7 ADC = %ld"%(events[7]))
    print ("\33[9A")

def setElemColor(element, color):
	for i in LED_INDEXES[element]:
		strip.setPixelColor(i, color)
	strip.show()
	time.sleep(wait_ms / 1000.0)

# Main program logic follows:
#if __name__ == '__main__':

    # Create NeoPixel object with appropriate configuration.
#    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
#    strip.begin()

if __name__ == '__main__':

    try:


        global connected
        global results

        connected = True
        if 'results' not in globals():
            results = []

        first_thread = threading.Thread(target=sensorThread)
        second_thread = threading.Thread(target=flagThread)
        save_thread = threading.Thread(target=flagThread)
        first_thread.start()
        second_thread.start()
        save_thread.start()

        time.sleep(1)

        connected = False

        save_thread.join()
        first_thread.join()
        second_thread.join()

#    try:
#        while True:

        

    except KeyboardInterrupt:
#        colorWipe(strip, Color(0, 0, 0), 10)
        GPIO.cleanup()
