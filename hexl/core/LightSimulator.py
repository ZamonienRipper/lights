import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw
import math
from hexl.core.LightControllerParent import LightControllerParent
from hexl.deps.ADS1256 import ADS1256

LED_INDEXES = [[0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[1],[0],[1],[1],[1],[2],[1],[3]]
LED_INDEXES_OUTER = [6, 7, 8, 9, 10, 11]
LED_INDEXES_INNER = [0, 1, 2, 3, 4, 5]
wait_ms = 50

class Window:
    def __init__(self, canvas_size=500, canvas_center=250):
        self.window = tk.Tk()
        self.window.title("Color Window")
        self.window.geometry(f"{canvas_size+100}x{canvas_size+100}")
        
        self.buffer = [0, 0, 0, 0, 0, 0, 0]

        self.canvas = tk.Canvas(self.window, width=canvas_size, height=canvas_size, bg="white")
        self.canvas.pack()

        self.color_fields = []
        for i in range(13):
            x = canvas_center + 0.2 * canvas_size * math.cos(2 * math.pi * i / 6)
            y = canvas_center + 0.2 * canvas_size * math.sin(2 * math.pi * i / 6)
            if i < 6:
                radius = 20
            elif i < 12:
                x = (x-canvas_center) * 2 + canvas_center
                y = (y-canvas_center) * 2 + canvas_center
                radius = 30
            else:
                x, y, radius = canvas_center, canvas_center, 35
            field = self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill="white")
            self.color_fields.append(field)

        # Create a round image for the buttons
        image = Image.new('L', (50, 50))
        draw = ImageDraw.Draw(image)
        draw.ellipse((0, 0, 50, 50), fill='white')
        self.button_image = tk.PhotoImage(image)

        self.buttons = []
        for i in range(7):
            x = canvas_center + 0.4 * canvas_size * math.cos(2 * math.pi * i / 6)
            y = canvas_center + 0.4 * canvas_size * math.sin(2 * math.pi * i / 6)
            button = tk.Button(self.window, image=self.button_image, command=lambda i=i: self.button_click(i))
            self.canvas.create_window(x, y, window=button)  # Place the button on the canvas
            self.buttons.append(button)

        self.buffer_button = tk.Button(self.window, text="Read Buffer", command=self.display_buffer)
        self.buffer_button.pack()

        self.text_box = tk.Text(self.window, height=2, width=30)
        self.text_box.pack()

    def button_click(self, i):
        self.buffer[i] = 1
        messagebox.showinfo("Button Clicked", f"Button {i+1} has been clicked")

    def change_color(self, field_index, rgb):
        color = "#%02x%02x%02x" % rgb  # Convert RGB to hex
        self.canvas.itemconfig(self.color_fields[field_index], fill=color)

    def read_buffer(self):
        buffer_values = self.buffer.copy()
        self.buffer = [0, 0, 0, 0, 0, 0, 0]
        return buffer_values

    def display_buffer(self):
        buffer_values = self.read_buffer()
        print(buffer_values)  # Print to terminal
        self.text_box.delete(1.0, tk.END)  # Clear text box
        self.text_box.insert(tk.END, str(buffer_values))  # Display in text box

    def run(self):
        self.window.mainloop()
      
    def setPixelColor(self, led, color):
        pass

class LightSimulator(LightControllerParent):
  
    def col(self, color):
        """Convert RGB to hex"""
        return "#%02x%02x%02x" % color
      
    def __init__(self, canvas_size=500, canvas_center=250):
        self.strip = Window()
        self.strip.run()
        self.bandsDict = {'outer': LED_INDEXES_OUTER, 'inner': LED_INDEXES_INNER}
        self.pixelsDict = {'outer': self.pixelList('outer'), 'inner': self.pixelList('inner')}
        self.LED_INDEXES = LED_INDEXES
        print(f"bandsDict: {self.bandsDict}")
        print(f"pixelsDict: {self.pixelsDict}")

