import math
import random
from tkinter import *
import time


def bitmap(width, height):
    start = f"""
    #define im_width {width}
    #define im_height {height}
    static char im_bits[] = {{
    """
    end = """
    };
    """
    values = '%02X' % random.getrandbits(8 * width * height)
    values = '0x' + ',0x'.join(values[i:i + 2] for i in range(0, len(values), 2))
    return start+values+end


class Display:

    label = None

    def __init__(self, t):
        bitmap_img = BitmapImage(data=bitmap(600, 600), foreground="white", background="black")
        self.label = Label(image=bitmap_img)
        self.label.pack()
        tk.update()

    def update(self):
        bitmap_img = BitmapImage(data=bitmap(600, 600), foreground="white", background="black")
        self.label.configure(image=bitmap_img)

        tk.update()


tk = Tk()
tk.title("cpu")
tk.geometry("600x600")
tk.configure(background='black')
display = Display(tk)
while True:
    time.sleep(0.5)
    display.update()
