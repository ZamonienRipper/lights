import collections
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw
import math
import queue
import numpy as np
from hexl.core.LightControllerParent import LightControllerParent
import threading

LED_INDEXES = [[0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13]]
LED_INDEXES_OUTER = [6, 7, 8, 9, 10, 11]
LED_INDEXES_INNER = [0, 1, 2, 3, 4, 5]
wait_ms = 50

class SimulatorStrip:
    def __init__(self, color_change_queue, LED_INDEXES):
        self.LED_INDEXES = LED_INDEXES
        self.color_change_queue = color_change_queue
        
    def setPixelColor(self, field_index, rgb):
        self.color_change_queue.put((field_index, rgb))
        
    def show(self):
        pass

    def numPixels(self):
        return len(self.LED_INDEXES)

class LightSimulator(LightControllerParent):
  
    def col(self, color):
        """Convert RGB to hex"""
        return color
      
    def __init__(self, color_change_queue=[], canvas_size=500, canvas_center=250):
        self.LED_INDEXES = LED_INDEXES
        self.bandsDict = {'outer': LED_INDEXES_OUTER, 'inner': LED_INDEXES_INNER}
        self.pixelsDict = {'outer': self.pixelList('outer'), 'inner': self.pixelList('inner')}
        self.strip = SimulatorStrip(color_change_queue, self.LED_INDEXES)

