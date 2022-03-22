import time
import RPi.GPIO as GPIO
import threading
from collections import deque
from rpi_ws281x import Color
from hexl.core.LightController import LightController
from hexl.core.StepUpDetector import StepUpDetector
from hexl.games.ActionLights import ActionLights
from hexl.games.Memory import Memory
from hexl.core.ThreadWithException import thread_with_exception
import numpy as np

def detectionThread(dataFreq, detector, eventPile):
    global connected
    while connected:
        time.sleep(dataFreq)
        detector.updateEvents(eventPile)
        #print(f"eventPile: {eventPile[-1]}")

def gameThread(game, gameFreq, lights, eventPile):
    game.play(gameFreq, lights, eventPile)

class Hexl():

    def __init__(self):

        global connected
        connected = True
        
        np.set_printoptions(linewidth=200)
            
        self.dataFreq = 0.03
        self.gameFreq = 0.1
        self.eventPile = deque([], maxlen=5)
        self.noGameRunning = True
        self.lights = LightController()
        self.detector = StepUpDetector()

        self.detection_thread = thread_with_exception(target=detectionThread, args=(self.dataFreq, self.detector, self.eventPile))
        
    def selectMode(self):
        gameWheel = ((255, 215), (230, 230, 250), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0))
        self.eventPile.clear()
        self.lights.pixelsChange([0, 1, 2, 3, 4, 5], gameWheel)
        while True:
            if self.eventPile:
                nextGame = np.where(self.eventPile.popleft() == 1)[0][0]
                self.lights.pixelOff(nextGame)
                return nextGame
            else:
                time.sleep(self.gameFreq)


    def run(self):
        try:
            
            self.detection_thread.start()
            
            while True:
                
                if self.noGameRunning:
                    nextGame = self.selectMode()
                    if nextGame == 0:
                        self.game = ActionLights()
                    elif nextGame == 1:
                        self.game = Memory()
                    elif nextGame == 2:
                        self.game = ActionLights()
                    elif nextGame == 3:
                        self.game = Memory()
                    elif nextGame == 4:
                        self.game = ActionLights()
                    elif nextGame == 5:
                        self.game = Memory()
                        
                    self.game_thread = thread_with_exception(
                        target=gameThread, args=(
                            self.game, self.gameFreq, self.lights, self.eventPile))

                    self.game_thread.start()
                    self.noGameRunning = False
                    time.sleep(2)
                else:
                    if self.game_thread.is_alive():
                        time.sleep(2)
                    else:
                        self.noGameRunning = True
        
        except KeyboardInterrupt:
            print("Keyboard Interrupt called")
            GPIO.cleanup()

        finally:
            connected = False
            self.detection_thread.raise_exception()
            self.detection_thread.join()
            self.game_thread.raise_exception()
            self.game_thread.join()
            self.lights.colorWipe(Color(0, 0, 0), 50)
            GPIO.cleanup()
            print("Everything is clean and wiped now. Goodbye")
