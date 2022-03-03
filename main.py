
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
LED_INDEXES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
wait_ms = 50
INPUT_CHANNELS = 3

sensitivity = 1

sensorPile = deque([], maxlen=5)
eventsPile = deque([], maxlen=5)

ADC = ADS1256()
ADC.ADS1256_init()

def getSensorData():
    time.sleep(0.03)

    class ReadADC:
        ADCValue = np.array(ADC.ADS1256_GetAll())*5.0/0x7fffff
    return ReadADC

def sensorThread():
    global connected
    while connected:
#        print(f"SensorPile: {sensorPile}")
        sensorPile.append(getSensorData().ADCValue)


def calculateEvents():
    time.sleep(0.03)

    class calcEvents:
        d = sensorPile[0] - sensorPile[-1]
        flags = np.array((d > sensitivity))
    return calcEvents


def flagThread():
    global connected
    while connected:
        eventsPile.append(calculateEvents().flags)
        print(f"eventsPile: {eventsPile[0][-2:]}")

def action_lights():
    time.sleep(0.1)
    cooldown = 15
    previousState = np.zeros(INPUT_CHANNELS)
    countdown = np.zeros(INPUT_CHANNELS)

    while connected:

        currentState = eventsPile[-1]
        stateChange = (-previousState) * currentState

        for i, state in enumerate(stateChange):
            if state == 0:
                if countdown[i] > 1:
                    countdown[i] -= 1
                elif countdown[i] == 1:
                    setElemColor(i, (0, 0, 0))
            elif state > 0:
                setElemColor(i, (0, 255, 0))
            else:
                countdown[i] = cooldown

        print(eventsPile)
        print ("0 ADC = %lf" % (currentState[0]))
        print ("1 ADC = %lf" % (currentState[1]))
        print ("2 ADC = %lf" % (currentState[2]))
        print ("3 ADC = %lf" % (currentState[3]))
        print ("4 ADC = %lf" % (currentState[4]))
        print ("5 ADC = %lf" % (currentState[5]))
        print ("6 ADC = %lf" % (currentState[6]))
        print ("7 ADC = %lf" % (currentState[7]))
        print ("\33[9A")

def setElemColor(element, color):
	for i in LED_INDEXES[element]:
		strip.setPixelColor(i, color)
	strip.show()
	time.sleep(wait_ms / 1000.0)



# Main program logic follows:
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    try:


        global connected
        global results

        connected = True
        if 'results' not in globals():
            results = []

        first_thread = threading.Thread(target=sensorThread)
        second_thread = threading.Thread(target=flagThread)
        output_thread = threading.Thread(target=actions)
        first_thread.start()

        time.sleep(1)
        second_thread.start()
        time.sleep(1)
        output_thread.start()

#    try:
#        while True:

        

    except KeyboardInterrupt:
        connected = False
        output_thread.join()
        first_thread.join()
        second_thread.join()
#        colorWipe(strip, Color(0, 0, 0), 10)
        GPIO.cleanup()
