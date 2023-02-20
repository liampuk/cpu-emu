import random
import time
from tkinter import *

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

class Display():

    tk = None
    label = None
    img_data = None

    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background='black')
        self.tk.geometry("400x240")

        bitmap_img = BitmapImage(data=bitmap(400, 240), foreground="white", background="black")

        self.label = Label(image=bitmap_img)
        self.label.pack()
        self.tk.update()

    def update(self):
        bitmap_img = BitmapImage(data=bitmap(400, 240), foreground="white", background="black")
        self.label.configure(image=bitmap_img)
        self.tk.update()


if __name__ == '__main__':
    display = Display()
    for i in range(100):
        # time.sleep(1)
        display.update()