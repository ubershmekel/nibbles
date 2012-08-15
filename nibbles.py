"""
nibbles.py

A tribute to the original QBasic nibbles game in python.
"""

import Tkinter
import random
import time


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
FPS = 20.0

SNAKE_SIZE = 20
UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
PLAYING = True
APPLE_LOC = None

def stop(event):
    global PLAYING
    PLAYING = False

class Rect:
    def __init__(self, x, y, size, color, canvas):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        

class Snake:
    def __init__(self, game):
        self.game = game
        self.rects = []
        for i in range(3):
            x = i * SNAKE_SIZE
            y = 0
            r = game.canvas.create_rectangle(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill="blue")
            self.rects.append(r)
        self.direction = RIGHT
        self.bind_keys()

    def up(self, event):
        self.direction = UP

    def down(self, event):
        self.direction = DOWN

    def left(self, event):
        self.direction = LEFT

    def right(self, event):
        self.direction = RIGHT

    def bind_keys(self):
        self.game.canvas.bind("<KeyRelease-Up>", self.up)
        self.game.canvas.bind("<KeyRelease-Down>", self.down)
        self.game.canvas.bind("<KeyRelease-Right>", self.right)
        self.game.canvas.bind("<KeyRelease-Left>", self.left)
        self.game.canvas.bind("<KeyRelease-q>", stop)

    def update(self):
        tail = self.rects.pop(0)
        head = self.rects[-1]
        l, b, r, t = self.game.canvas.coords(head)
        l += self.direction[0] * SNAKE_SIZE
        r += self.direction[0] * SNAKE_SIZE
        b += self.direction[1] * SNAKE_SIZE
        t += self.direction[1] * SNAKE_SIZE
        self.game.canvas.coords(tail, l, b, r, t)
        self.rects.append(tail)


class Game:
    def __init__(self):
        self.master = Tkinter.Tk()
        self.master.title("Nibbles")

        self.canvas = Tkinter.Canvas(self.master, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.canvas.pack()
        
        # Set focus on canvas in order to collect key-events
        self.canvas.focus_force()

        self.player1 = Snake(self)
        
    def update(self):
        self.player1.update()
        self.canvas.update()
        
        if PLAYING:
            self.canvas.after(int(1000.0 / FPS), self.update)
        else:
            print('Game Over')
            exit()
    
    def start(self):
        self.update()
        self.master.mainloop()
     
    
game = Game()
game.start()

