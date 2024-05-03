from collections import deque
from threading import Event
import hexl
from hexl.games.ActionLights import ActionLights
from hexl.games.Memory import Memory
from hexl.games.HexClock import HexClock
from hexl.games.DebugMode import DebugMode
from hexl.games.Hush import Hush
from hexl.games.RandomWalker import RandomWalker
from hexl.core.ThreadWithException import thread_with_exception
import numpy as np
import tkinter as tk
import math
import queue
import time
from hexl.core.LightSimulator import LightSimulator

import pkgutil

for game in pkgutil.iter_modules(hexl.games.__path__):
    print(game.name)


class Simulator:
    def button_click(self, i):
        tmp = np.array([0, 0, 0, 0, 0, 0], dtype="uint8")
        tmp[i - 1] = 1
        print(f"clicked button {i-1}")
        self.eventPile.append(tmp)

    def process_color_changes(self):
        field_index, rgb = self.color_change_queue.get()
        color = "#%02x%02x%02x" % rgb  # Convert RGB to hex
        self.canvas.itemconfig(self.color_fields[field_index], fill=color)

    def __init__(self, canvas_size=500, canvas_center=250):

        global connected
        connected = True

        self.games = {
            "ActionLights": ActionLights(),
            "Memory": Memory(),
            "HexClock": HexClock(),
            "DebugMode": DebugMode(),
            "Hush": Hush(),
            "RandomWalker": RandomWalker(),
        }

        # Game variables
        self.stop_threads = Event()
        self.gameFreq = 0.05
        self.eventPile = deque([], maxlen=5)
        self.color_change_queue = queue.Queue()
        self.lights = LightSimulator(self.color_change_queue)
        self.next_game = "Hush"

        # GUI setup
        self.window = tk.Tk()
        self.window.title("Color Window")
        self.window.geometry(f"{canvas_size}x{canvas_size}")
        self.canvas_size = canvas_size

        self.canvas = tk.Canvas(
            self.window, width=canvas_size, height=canvas_size, bg="white"
        )
        self.canvas.pack()

        # Create circular color fields in correposponding positions as the physical device
        self.color_fields = []
        for i in range(13):
            x = canvas_center + 0.17 * canvas_size * math.cos(2 * math.pi * i / 6)
            y = canvas_center + 0.17 * canvas_size * math.sin(2 * math.pi * i / 6)
            if i < 6:
                radius = 20
            elif i < 12:
                x = (x - canvas_center) * 2 + canvas_center
                y = (y - canvas_center) * 2 + canvas_center
                radius = 30
            else:
                x, y, radius = canvas_center, canvas_center, 35
            field = self.canvas.create_oval(
                x - radius, y - radius, x + radius, y + radius, fill="black"
            )
            self.canvas.create_text(x, y, text=i, fill="white")
            self.canvas.pack()
            self.color_fields.append(field)

        # Create buttons in the positions of the physical device
        self.buttons = []
        for i in range(
            1, 7
        ):  # strange indexing required to match the physical device where LED 0 is not aligned with button 0
            x = canvas_center + 0.45 * canvas_size * math.cos(2 * math.pi * (i - 1) / 6)
            y = canvas_center + 0.45 * canvas_size * math.sin(2 * math.pi * (i - 1) / 6)
            button = tk.Button(
                self.window, text=f"BTN{i-1}", command=lambda i=i: self.button_click(i)
            )
            self.canvas.create_window(
                x, y, window=button
            )  # Place the button on the canvas
            self.buttons.append(button)

        # Add controls for selecting and restarting the game
        self.game_selection = tk.StringVar(self.window)
        self.game_selection.set(list(self.games.keys())[4])  # Set the default selection

        def update_game_selection():
            self.next_game = self.game_selection.get()

        self.game_selection.trace_add("write", update_game_selection)

        game_list = tk.OptionMenu(self.window, self.game_selection, *self.games.keys())
        game_list.config(width=12)  # Set the width of the option menu button
        self.canvas.create_window(self.canvas_size - 50, 10, window=game_list)
        self.buttons.append(game_list)

        def restart_game():
            self.game_thread.raise_exception()
            for led in self.lights.LED_INDEXES:
                print(led)
                self.color_change_queue.put((led[0], (0, 0, 0)))
            self.start_game()

        restart_button = tk.Button(self.window, text="Next Game", command=restart_game)
        restart_button.config(width=15)  # Set the width of the restart button
        self.canvas.create_window(self.canvas_size - 50, 40, window=restart_button)
        self.buttons.append(restart_button)

        # Start a thread that checks the queue and performs color changes
        def colorUpdateThread():
            global connected
            while connected:
                self.process_color_changes()

        self.colorUpdateThread = thread_with_exception(target=colorUpdateThread)
        self.colorUpdateThread.setDaemon(True)
        self.colorUpdateThread.start()

    def start_game(self):

        def gameThread(game, gameFreq, lights, eventPile):
            global connected
            while connected:
                time.sleep(1)
                game.play(gameFreq, lights, eventPile)

        try:

            def stop_game():
                print("stopping game")
                connected = False
                self.colorUpdateThread.raise_exception()
                print("closed colorThread")
                self.game_thread.raise_exception()
                print("closed gameThread")
                self.window.destroy()

            self.game = self.games[self.next_game]

            self.game_thread = thread_with_exception(
                target=gameThread,
                args=(self.game, self.gameFreq, self.lights, self.eventPile),
            )
            self.game_thread.setDaemon(True)

            q_button = tk.Button(self.window, text="Quit", command=stop_game)
            q_button.config(width=15)
            self.canvas.create_window(50, 10, window=q_button)
            self.buttons.append(q_button)

            self.game_thread.start()

            self.window.mainloop()

        except KeyboardInterrupt:
            print("Keyboard Interrupt called")

        finally:
            connected = False
            self.colorUpdateThread.raise_exception()
            self.game_thread.raise_exception()
            print("Everything is clean and wiped now. Goodbye")

    def run(self):
        self.start_game()
