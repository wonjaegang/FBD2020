from tkinter import *
import time

WIDTH = 1200
HEIGHT = 800
SIZE = 50
tk = Tk()
canvas = Canvas(tk, width=WIDTH, height=HEIGHT, bg="grey")
canvas.pack()
color = 'black'

uinput = input("1~15: ")
uinput = int(uinput)
uinput *= 50
uinput = HEIGHT-uinput


class Ball:
    def __init__(self):
        self.shape = canvas.create_rectangle(
            [0, HEIGHT, SIZE, HEIGHT-SIZE], fill=color)
        self.speedx = 0  # changed from 3 to 9
        self.speedy = -10  # changed from 3 to 9
        self.active = True
        self.move_active()

    def ball_update(self):
        canvas.move(self.shape, self.speedx, self.speedy)
        pos = canvas.coords(self.shape)
        if pos[3] <= uinput:
            self.speedy = 0

    def move_active(self):
        if self.active:
            self.ball_update()
            tk.after(40, self.move_active)  # changed from 10ms to 30ms


ball = Ball()
tk.mainloop()
