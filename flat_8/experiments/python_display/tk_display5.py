import random
from tkinter import *

top = Tk()
top.configure(background='black')
top.geometry("600x600")

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

def update():
    label.configure(image=bitmap_img2)
    top.update()


bitmap_img = BitmapImage(data=bitmap(600, 600), foreground="white", background="black")
bitmap_img2 = BitmapImage(data=bitmap(600, 600), foreground="white", background="black")

label = Label(image=bitmap_img)
label.pack()
top.after(2000, update)
top.mainloop()