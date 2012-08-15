"""
nibbles.py

A tribute to the original QBasic nibbles game in python.
"""

import random
import Tkinter
import random
import time


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_COLS, GRID_ROWS = 20, 20
FPS = 30

CELL_SIZE_X = SCREEN_WIDTH / GRID_COLS
CELL_SIZE_Y = SCREEN_HEIGHT / GRID_ROWS
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

def b2x(x):
    return x * CELL_SIZE_X

def b2y(y):
    return y * CELL_SIZE_Y

class Rect:
    def __init__(self, canvas, x, y, *args, **kwargs):
        self.canvas = canvas
        self.id = canvas.create_rectangle(b2x(x), b2y(y), b2x(x + 1), b2y(y + 1), *args, **kwargs)
        self.x = x
        self.y = y
    
    def moveto(self, x, y):
        self.x = x
        self.y = y
        self.canvas.coords(self.id, b2x(x), b2y(y), b2x(x + 1), b2y(y + 1))

class Snake:
    def __init__(self, game):
        self.game = game
        self.rects = []
        for i in range(3):
            x = i
            y = 0
            r = Rect(game.canvas, x, y, fill="blue")
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
        x, y = head.x, head.y
        # modulo to wrap
        x = (x + self.direction[0]) % GRID_COLS
        y = (y + self.direction[1]) % GRID_ROWS
        tail.moveto(x, y)
        self.rects.append(tail)
        self.x, self.y = x, y

class Apple:
    def __init__(self, game):
        self.game = game
        self.x, self.y = self.random_location()
        self.rect = Rect(game.canvas, self.x, self.y, fill="red")

    def random_location(self):
        return random.randint(0, GRID_COLS - 1), random.randint(0, GRID_ROWS - 1)

    def relocate(self):
        self.x, self.y = self.random_location()
        self.rect.moveto(self.x, self.y)

class Game:
    def __init__(self):
        self.root = Tkinter.Tk()
        self.root.title("Nibbles")
        self.root.minsize(320, 240)
        #self.root.pack_propagate(0)

        self.canvas = Tkinter.Canvas(self.root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, highlightthickness=0)
        self.canvas.pack(fill=Tkinter.BOTH, expand=1)
        
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        
        # Set focus on canvas in order to collect key-events
        self.canvas.focus_force()

        self.snake1 = Snake(self)
        self.apple = Apple(self)
        
        self.root.bind( '<Configure>', self.resize)
    
    def resize(self, event):
        """
        Handle resize events so that the drawn objects adapts to the window size.
        """
        global CELL_SIZE_X, CELL_SIZE_Y
        CELL_SIZE_X = round(self.canvas.winfo_width() * 1.0 / GRID_COLS)
        CELL_SIZE_Y = round(self.canvas.winfo_height() * 1.0 / GRID_ROWS)
        x_scale = event.width * 1.0 / self.width
        y_scale = event.height * 1.0 / self.height
        self.height = event.height
        self.width = event.width
        self.canvas.scale(Tkinter.ALL, 0, 0, x_scale, y_scale)
    
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
        self.root.mainloop()
     
    
game = Game()
game.start()

