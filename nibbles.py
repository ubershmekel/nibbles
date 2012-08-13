import time
import turtle

PLAYING = True

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
screen.onkey(left, 'Left')
screen.onkey(up, 'Up')
screen.onkey(right, 'Right')
screen.onkey(down, 'Down')
screen.onkey(stop, 'q')
screen.listen()

def main():
    while PLAYING:
        tod.forward(1)
    

main()
