import math
import random
import tkinter
import time


class Display:

    # bitmap: list[int][int] =

    bitmap: list[[int]] = [[0] * 240] * 400
    canvas = None
    images: list[tkinter.PhotoImage] = []
    image_container = None
    image: tkinter.PhotoImage
    image2: tkinter.PhotoImage

    def __init__(self, t):
        self.image = tkinter.PhotoImage(width=400, height=240)
        self.bitmap = [[random.getrandbits(1) for y in range(240)] for x in range(400)]

        for x in range(len(self.bitmap)):
            for y in range(len(self.bitmap[x])):
                self.image.put("#fff" if self.bitmap[x][y] == 1 else "#000", (x, y))

        self.canvas = tkinter.Canvas(t, width=400, height=240, highlightthickness=0)
        self.canvas.pack()
        self.image_container = self.canvas.create_image(0, 0, image=self.image, anchor=tkinter.NW)
        tk.update()
        self.update()

    def update(self):


        bitmap = [[random.getrandbits(1) for y in range(240)] for x in range(400)]

        image = tkinter.PhotoImage(width=400, height=240)

        self.images.append(image)


        image_index = len(self.images)-1
        # for x in range(400):
        #     for y in range(240):
        #         self.images[image_index].put("#fff" if bitmap[x][y] == 1 else "#000", (x, y))

        start_time = time.time()
        for i in range(400 * 240):
            self.images[image_index].put("#fff" if random.getrandbits(1) == 1 else "#000", (i % 400, math.floor(i/400)))
        self.canvas.itemconfig(self.image_container, image=self.images[image_index])
        print("%s seconds" % (time.time() - start_time))

        # time.sleep(1)
        tk.update()
        self.update()


tk = tkinter.Tk()
tk.title("cpu")
tk.geometry("400x240")
tk.configure(background='black')
display = Display(tk)
tk.mainloop()
