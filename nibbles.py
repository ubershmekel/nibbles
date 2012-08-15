"""
nibbles.py

A tribute to the original QBasic nibbles game in python.
"""

import Tkinter
import random
import time


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
FPS = 30.0

UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
SNAKE_SIZE = 20
PLAYING = True
APPLE_LOC = None

def stop(event):
    global PLAYING
    PLAYING = False

class Snake:
    def __init__(self, game):
        self.game = game
        x, y = 0, 0
        self.r = game.canvas.create_rectangle(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill="blue")
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
        self.game.canvas.move(self.r, self.direction[0], self.direction[1])


class Game:
    def __init__(self):
        self.master = Tkinter.Tk()

        self.canvas = Tkinter.Canvas(self.master, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.canvas.pack()
        
        # Set focus on canvas in order to collect key-events
        self.canvas.focus_force()

        self.player1 = Snake(self)
        
    def update(self):
        self.player1.update()
        self.canvas.update()
    
#l = canvas.create_line(0, 0, 200, 100)
#canvas.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))

game = Game()

while PLAYING:
    time.sleep(1.0 / FPS)
    game.update()

