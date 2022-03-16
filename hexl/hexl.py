
import time
import RPi.GPIO as GPIO
import threading
from collections import deque
from rpi_ws281x import Color
import numpy as np
import hexl

dataFreq = 0.03

eventPile = deque([], maxlen=100)

lights = hexl.core.LightController.LightController()
detector = hexl.core.StepUpDetector.StepUpDetector(eventPile)

game = hexl.games.ActionLights.ActionLights(eventPile, lights)

game.play

def detectionThread():
    global connected
    while connected:
        time.sleep(dataFreq)
        detector.updateEvents()
        print(f"SensorPile: {eventPile[-1]}")

def gameThread():
    game.play()


# Main program logic follows:
if __name__ == '__main__':
    try:

        global connected
        global results

        connected = True
        if 'results' not in globals():
            results = []

        detection_thread = threading.Thread(target=detectionThread)
        game_thread = threading.Thread(target=gameThread)
        detection_thread.start()
        game_thread.start()

    except KeyboardInterrupt:
        connected = False

    finally:
        connected = False
        detection_thread.join()
        game_thread.join()
        lights.colorWipe(Color(0, 0, 0), 50)
        GPIO.cleanup()
