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
FPS = 15
CELL_SIZE_X = SCREEN_WIDTH / GRID_COLS
CELL_SIZE_Y = SCREEN_HEIGHT / GRID_ROWS
UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
OPPOSITE = {UP:DOWN, LEFT:RIGHT, DOWN:UP, RIGHT:LEFT}
SNAKE_INIT_SIZE = 3
PLAYER1_KEYS = "Up", "Down", "Left", "Right"
PLAYER2_KEYS = "w", "s", "a", "d"
PLAYER1_COLOR = "#dddd00"
PLAYER2_COLOR = "#00aa22"
BG_COLOR = "#e7e7e7"
SCORE_BG_COLOR = "#2a2a2a"
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
    def __init__(self, game, keys, initx=0, inity=0, color=PLAYER1_COLOR):
        self.game = game
        self.rects = []
        self.color = color
        self.score = 0
        self.deaths = 0 
        self.initx = initx
        self.inity = inity
        self.size = SNAKE_INIT_SIZE
        self.init_body()
        self.direction = RIGHT
        self.bind_keys(keys)
        self.just_turned = False

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
        self.game.canvas.bind("<KeyPress-%s>" % keys[0], self.up)
        self.game.canvas.bind("<KeyPress-%s>" % keys[1], self.down)
        self.game.canvas.bind("<KeyPress-%s>" % keys[2], self.left)
        self.game.canvas.bind("<KeyPress-%s>" % keys[3], self.right)

    def update(self):
        self.just_turned = False
        tail = self.rects.pop(0)
        if self.size > len(self.rects):
            r = self.create_joint(tail.x, tail.y)
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
            self.size += 1
            self.game.apple.relocate()
            self.game.update_score()
        
        if (x, y) in self.game.causes_of_death:
            self.die()
            self.game.update_score()
    
    def create_joint(self, x, y):
        return Rect(self.game.canvas, x, y, fill=self.color)
    
    def init_body(self):
        for r in self.rects:
            self.game.canvas.delete(r.id)
            self.rects = []
        
        r = self.create_joint(self.initx, self.inity)
        self.rects.append(r)
    
    def die(self):
        self.deaths += 1
        self.direction = RIGHT
        self.size = SNAKE_INIT_SIZE
        self.init_body()
        print 'ouch!'
    
    def score_str(self):
        return "Apples: %d  Deaths: %d" % (self.score, self.deaths)
        
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

        # score board
        # The frame is needed to bunch the labels in one row. The scoreboard
        # is packed first as to avoid the canvas hiding it when shrinking
        # the window.
        frame = Tkinter.Frame(self.root, bg=SCORE_BG_COLOR)
        self.score1_svar = Tkinter.StringVar()
        l = Tkinter.Label(frame, textvariable=self.score1_svar, fg=PLAYER1_COLOR, bg=SCORE_BG_COLOR)
        l.pack(side=Tkinter.LEFT, expand=False)
        self.label1 = l
        self.score2_svar = Tkinter.StringVar()
        l = Tkinter.Label(frame, textvariable=self.score2_svar, fg=PLAYER2_COLOR, bg=SCORE_BG_COLOR)
        l.pack(side=Tkinter.RIGHT)
        self.label2 = l
        frame.pack(fill=Tkinter.X)

        # play area
        self.canvas = Tkinter.Canvas(self.root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, highlightthickness=0, bg=BG_COLOR)
        self.canvas.pack(fill=Tkinter.BOTH, expand=True)

        self.root.bind('<Configure>', self.resize)
        self.canvas.bind("<KeyRelease-%s>" % QUIT_KEY, stop)
        
        # Set focus on canvas in order to collect key-events
        self.canvas.focus_force()

        self.snake1 = Snake(self, PLAYER1_KEYS)
        self.snake2 = Snake(self, PLAYER2_KEYS, inity=GRID_ROWS - 1, color=PLAYER2_COLOR)
        self.apple = Apple(self)
        
        self.sprites = [self.apple, self.snake1, self.snake2]
        self.update_score()
    
    def update_score(self):
        self.score1_svar.set(self.snake1.score_str())
        self.score2_svar.set(self.snake2.score_str())
    
    def resize(self, event):
        """
        Handle resize events so that the drawn objects adapts to the window size.
        """
        global CELL_SIZE_X, CELL_SIZE_Y
        if event.widget == self.canvas:
            CELL_SIZE_X = round(event.width * 1.0 / GRID_COLS)
            CELL_SIZE_Y = round(event.height * 1.0 / GRID_ROWS)
            for sprite in self.sprites:
                sprite.redraw()
    
    def update(self):
        self.causes_of_death = set([(r.x, r.y) for r in self.snake1.rects] + [(r.x, r.y) for r in self.snake2.rects])
        
        for sprite in self.sprites:
            sprite.update()
        
        # queue a refresh
        if PLAYING:
            self.canvas.after(int(1000.0 / FPS), self.update)
        else:
            print('Game Over')
            print('Player1 %d, Player2 %d' % (self.snake1.score - self.snake1.deaths, self.snake2.score - self.snake2.deaths))
            exit()
    
    def start(self):
        self.update()
        self.root.mainloop()
     
if __name__ == "__main__":    
    game = Game()
    game.start()

