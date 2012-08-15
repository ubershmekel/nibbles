"""
nibbles.py

A tribute to the original QBasic nibbles game in python.
"""

import random
import Tkinter
import random
import time


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
FPS = 20.0

CELL_SIZE = 20
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
            x = i * CELL_SIZE
            y = 0
            r = game.canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill="blue")
            self.rects.append(r)
        self.direction = RIGHT
        self.bind_keys()
        self.score = 0

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
        l += self.direction[0] * CELL_SIZE
        r += self.direction[0] * CELL_SIZE
        b += self.direction[1] * CELL_SIZE
        t += self.direction[1] * CELL_SIZE
        self.game.canvas.coords(tail, l, b, r, t)
        self.rects.append(tail)
        self.x, self.y = round(l), round(b)

class Apple:
    def __init__(self, game):
        self.game = game
        x, y = random.randint(0, 10) * CELL_SIZE, random.randint(0, 10) * CELL_SIZE
        l, b, r, t = x, y, x + CELL_SIZE, y + CELL_SIZE
        self.rect = game.canvas.create_rectangle(l, b, r, t, fill="red")
        self.x, self.y = round(l), round(b)

    def relocate(self):
        x, y = random.randint(0, 10) * CELL_SIZE, random.randint(0, 10) * CELL_SIZE
        l, b, r, t = x, y, x + CELL_SIZE, y + CELL_SIZE
        self.game.canvas.coords(self.rect, l, b, r, t)
        self.x, self.y = round(l), round(b)

class Game:
    def __init__(self):
        self.master = Tkinter.Tk()
        self.master.title("Nibbles")

        self.canvas = Tkinter.Canvas(self.master, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.canvas.pack()
        
        # Set focus on canvas in order to collect key-events
        self.canvas.focus_force()

        self.snake1 = Snake(self)
        self.apple = Apple(self)

    def update(self):
        self.snake1.update()
        self.canvas.update()
        
        if self.snake1.x == self.apple.x and self.snake1.y == self.apple.y:
            self.snake1.score += 1
            self.apple.relocate()
        
        # queue a refresh
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

