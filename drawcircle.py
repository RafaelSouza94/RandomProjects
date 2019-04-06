#!/usr/bin/python3

import math
import turtle

def draw_circle_turtle(x, y, r):
    # remove the virtual pen from the virtual paper
    turtle.up()
    # position the turtle, or pen
    turtle.setpos(x + r, y)
    # put the virtual pen back on the virtual paper
    turtle.down()

    for i in range(0, 365, 5):
        a = math.radians(i)
        turtle.setpos(x + r*math.cos(a), y + r*math.sin(a))

draw_circle_turtle(300, 300, 150)
turtle.mainloop()
