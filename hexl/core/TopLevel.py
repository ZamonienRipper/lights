
import time
import RPi.GPIO as GPIO
import threading
from kivy.app import App
from collections import deque
from rpi_ws281x import Color
from hexl.core.LightController import LightController
from hexl.core.StepUpDetector import StepUpDetector
from hexl.games.ActionLights import ActionLights

def detectionThread(dataFreq, detector, eventPile):
    global connected
    while connected:
        time.sleep(dataFreq)
        detector.updateEvents()
        print(f"SensorPile: {eventPile[-1]}")


class Menu(App):

    def __init__(self):

        self.dataFreq = 0.03
        self.eventPile = deque([], maxlen=100)

        self.lights = LightController()
        self.detector = StepUpDetector(self.eventPile)

        detection_thread = threading.Thread(target=detectionThread, args=(self.dataFreq, self.detector, self.eventPile))
        detection_thread.start()

    def run(self):
        try:

            global connected
            connected = True

            self.game = ActionLights(self.eventPile, self.lights)
            game_thread = threading.Thread(target=self.game.play())
            game_thread.start()

        finally:
            connected = False
            self.detection_thread.stop()
            game_thread.stop()
            self.lights.colorWipe(Color(0, 0, 0), 50)
            GPIO.cleanup()
