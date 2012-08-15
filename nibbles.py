"""
nibbles.py

A tribute to the original QBasic nibbles game in python.
"""

import random
import Tkinter
import random
import time


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_COLS, GRID_ROWS = 32, 24
FPS = 20
CELL_SIZE_X = SCREEN_WIDTH / GRID_COLS
CELL_SIZE_Y = SCREEN_HEIGHT / GRID_ROWS
UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
OPPOSITE = {UP:DOWN, LEFT:RIGHT, DOWN:UP, RIGHT:LEFT}
SNAKE_INIT_SIZE = 3
PLAYER1_KEYS = "Up", "Down", "Left", "Right"
PLAYER2_KEYS = "w", "s", "a", "d"
QUIT_KEY = "Escape"
PLAYING = True

def stop(event):
    global PLAYING
    PLAYING = False

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
        self.redraw()
    
    def redraw(self):
        self.canvas.coords(self.id, b2x(self.x), b2y(self.y), b2x(self.x + 1), b2y(self.y + 1))

class Sprite:
    def redraw(self):
        for rect in self.rects:
            rect.redraw()

class Snake(Sprite):
    def __init__(self, game, keys, x=0, y=0):
        self.game = game
        self.rects = []
        for i in range(SNAKE_INIT_SIZE):
            x = x + i
            y = y
            r = self.create_body(x, y)
            self.rects.append(r)
        self.direction = RIGHT
        self.bind_keys(keys)
        self.score = SNAKE_INIT_SIZE
        self.just_turned = False

    def create_body(self, x, y):
        return Rect(self.game.canvas, x, y, fill="#dddd00")

    def bad_direction(self, new_direction):
        if OPPOSITE[self.direction] == new_direction or self.just_turned:
            return True
        else:
            self.just_turned = True
            return False

    def up(self, event):
        if self.bad_direction(UP):
            return
        self.direction = UP

    def down(self, event):
        if self.bad_direction(DOWN):
            return
        self.direction = DOWN

    def left(self, event):
        if self.bad_direction(LEFT):
            return
        self.direction = LEFT

    def right(self, event):
        if self.bad_direction(RIGHT):
            return
        self.direction = RIGHT

    def bind_keys(self, keys):
        self.game.canvas.bind("<KeyRelease-%s>" % keys[0], self.up)
        self.game.canvas.bind("<KeyRelease-%s>" % keys[1], self.down)
        self.game.canvas.bind("<KeyRelease-%s>" % keys[2], self.left)
        self.game.canvas.bind("<KeyRelease-%s>" % keys[3], self.right)

    def update(self):
        self.just_turned = False
        tail = self.rects.pop(0)
        if self.score > len(self.rects):
            r = self.create_body(tail.x, tail.y)
            self.rects.insert(0, r)
        head = self.rects[-1]
        x, y = head.x, head.y
        # modulo to wrap
        x = (x + self.direction[0]) % GRID_COLS
        y = (y + self.direction[1]) % GRID_ROWS
        tail.moveto(x, y)
        self.rects.append(tail)
        self.x, self.y = x, y

        if self.x == self.game.apple.x and self.y == self.game.apple.y:
            self.score += 1
            self.game.apple.relocate()

class Apple(Sprite):
    def __init__(self, game):
        self.game = game
        self.x, self.y = self.random_location()
        self.rects = [Rect(game.canvas, self.x, self.y, fill="red")]

    def random_location(self):
        return random.randint(0, GRID_COLS - 1), random.randint(0, GRID_ROWS - 1)

    def relocate(self):
        self.x, self.y = self.random_location()
        self.rects[0].moveto(self.x, self.y)
    
    def update(self):
        pass

class Game:
    def __init__(self):
        self.root = Tkinter.Tk()
        self.root.title("Nibbles")
        self.root.minsize(320, 240)

        self.canvas = Tkinter.Canvas(self.root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, highlightthickness=0, bg="#F7F7F7")
        self.canvas.pack(fill=Tkinter.BOTH, expand=1)
        self.root.bind( '<Configure>', self.resize)
        self.canvas.bind("<KeyRelease-%s>" % QUIT_KEY, stop)
        
        # Set focus on canvas in order to collect key-events
        self.canvas.focus_force()

        self.snake1 = Snake(self, PLAYER1_KEYS)
        self.snake2 = Snake(self, PLAYER2_KEYS, y=GRID_ROWS - 1)
        self.apple = Apple(self)
        
        self.sprites = [self.apple, self.snake1, self.snake2]
    
    def resize(self, event):
        """
        Handle resize events so that the drawn objects adapts to the window size.
        """
        global CELL_SIZE_X, CELL_SIZE_Y
        CELL_SIZE_X = round(event.width * 1.0 / GRID_COLS)
        CELL_SIZE_Y = round(event.height * 1.0 / GRID_ROWS)
        for sprite in self.sprites:
            sprite.redraw()
    
    def update(self):
        for sprite in self.sprites:
            sprite.update()
        
        self.canvas.update()
        
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

