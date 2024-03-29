import random
import time
from tkinter import *
import fonts








def bitmap(_img_data):
    start = f"""
    #define im_width 400
    #define im_height 240
    static char im_bits[] = {{
    """
    end = """
    };
    """
    img_data_string = ""
    for y in range(240):
        for x in range(50):
            img_data_string = img_data_string + ('%02X' % int('{:08b}'.format(_img_data[y][x])[::-1], 2))
    img_data_string = '0x' + ',0x'.join(img_data_string[i:i + 2] for i in range(0, len(img_data_string), 2))

    return start+img_data_string+end

def characters(_img_data):

    start_y = 4
    start_x = 20
    for row in range(29):
        for y in range(8):
            for x in range(8):
                _img_data[y+start_y+row*8][x+start_x] = fonts.ibm_int[y + x * 8 + row * 64]

    return _img_data


class Display:
    tk = None
    label = None
    bitmap_img = None

    img_data: list[[int]] = [[0 for x in range(50)] for y in range(240)]

    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background='black')
        self.tk.geometry("400x240")

        for y in range(240):
            for x in range(50):
                self.img_data[y][x] = random.getrandbits(8)

        bitmap_img_data = bitmap(self.img_data)

        self.bitmap_img = BitmapImage(data=bitmap_img_data, foreground="white", background="black")

        self.label = Label(image=self.bitmap_img)
        self.label.pack()
        self.tk.update()

    def update(self, _img_data):
        bitmap_img_data = bitmap(_img_data)

        self.bitmap_img = BitmapImage(data=bitmap_img_data, foreground="white", background="black")
        self.label.configure(image=self.bitmap_img)
        self.tk.update()

    def done(self):
        self.tk.mainloop()


if __name__ == '__main__':
    img_data: list[[int]] = [[0 for x in range(400)] for y in range(240)]
    display = Display()
    while True:
        time.sleep(0.01)
        for y in range(240):
            for x in range(50):
                img_data[y][x] = random.getrandbits(8)
        img_data = characters(img_data)
        display.update(img_data)