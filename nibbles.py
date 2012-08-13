"""
nibbles.py

A tribute to the original QBasic nibbles game in python.


Tim: There he is! 
King Arthur: Where? 
Tim: There! 
King Arthur: What? Behind the rabbit? 
Tim: It *is* the rabbit! 
King Arthur: You silly sod! 
Tim: What? 
King Arthur: You got us all worked up! 
Tim: Well, that's no ordinary rabbit. 
King Arthur: Ohh. 
Tim: That's the most foul, cruel, and bad-tempered rodent you ever set eyes on! 
Sir Robin: You tit! I soiled my armor I was so scared! 
Tim: Look, that rabbit's got a vicious streak a mile wide! It's a killer! 
Sir Galahad: Get stuffed! 
Tim: He'll do you up a treat, mate. 
Sir Galahad: Oh, yeah? 
Sir Robin: You manky Scots git! 
Tim: I'm warning you! 

Sir Robin: What's he do? Nibble your bum? 

Tim: He's got huge, sharp... er... He can leap about. Look at the bones! 
King Arthur: Go on, Bors. Chop his head off! 
Sir Bors: Right! Silly little bleeder. One rabbit stew comin' right up! 
"""

import random
import time
import turtle

APPLE_SIZE = 20


PLAYING = True
APPLE_LOC = None

def up():
    tod.setheading(90)

def down():
    tod.setheading(270)

def left():
    tod.setheading(180)

def right():
    tod.setheading(0)

def stop():
    global PLAYING
    PLAYING = False
    
tod = turtle.Turtle()
tod.speed(0)

screen = tod.getscreen()
cv = screen.getcanvas()
screen.title('NIBBLES')
screen.onkey(left, 'Left')
screen.onkey(up, 'Up')
screen.onkey(right, 'Right')
screen.onkey(down, 'Down')
screen.onkey(stop, 'q')
screen.listen()

L, R, B, T = -screen.window_width() // 2, screen.window_width() // 2, -screen.window_height() // 2, screen.window_height() // 2

def main():
    global APPLE_LOC
    global PLAYING
    
    while PLAYING:
        tod.forward(2)
        if APPLE_LOC is None:
            x = random.randint(L + APPLE_SIZE, R - APPLE_SIZE)
            y = random.randint(B + APPLE_SIZE, T - APPLE_SIZE)
            APPLE_LOC = x, y
            cv.create_rectangle((x, y, x + APPLE_SIZE, y + APPLE_SIZE), fill="red")
            x = x
            y = -y
        
        todx, tody = tod.xcor(), tod.ycor()
        if (L < todx < R) and (B < tody < T):
            pass
        else:
            print 'out of bounds'
            PLAYING = False
        
        if x < todx < x + APPLE_SIZE and y - APPLE_SIZE < tody < y:
            print 'got the apple'
        #print todx, tody, x, y
        #print x/screen.xscale, y/screen.yscale, todx, tody

main()
