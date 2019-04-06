#!/usr/bin/python3

import math
import turtle
import sys, random, argparse
import numpy as np
from PIL import Image
from datetime import datetime
from fractions import gcd

class Spiro:
    def __init__(self, xc, yx, col, R, r, l):

        self.t = turtle.Turtle()
        self.t.shape('turtle')
        self.step = 5
        self.drawing_complete = False

        self.setparams(xc, yx, col, R, r, l)

        self.restart()

    def setparams(self, xc, yc, col, R, r, l):

        self.xc = xc
        self.yc = yc
        self.R = int(R)
        self.r = int(r)
        self.l = l
        self.col = col

        gcd_val = gcd(self.r, self.R)
        self.n_rot = self.r // gcd_val
        self.k = r / float(R)
        self.t.color(*col)
        self.a = 0

    def restart(self):

        self.drawing_complete = False
        self.t.showturtle()
        self.t.up()
        R, k, l = self.R, self.k, self.l
        a = 0.0
        x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = R*((1-k)*math.sin(a) + l*k*math.sin((1-k)*a/k))
        self.t.setpos(self.xc + x, self.yc + y)
        self.t.down()

    def draw(self):

        R, k, l = self.R, self.k, self.l
        for i in range(0, 360 * self.n_rot + 1, self.step):
            a = math.radians(i)
            x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
            y = R*((1-k)*math.sin(a) + l*k*math.sin((1-k)*a/k))
            self.t.setpos(self.xc + x, self.yc + y)
        self.t.hideturtle()

    def update(self):

        if self.drawing_complete:
            return

        self.a += self.step

        R, k, l = self.R, self.k, self.l
        a = math.radians(self.a)
        x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = R*((1-k)*math.sin(a) + l*k*math.sin((1-k)*a/k))
        self.t.setpos(self.xc + x, self.yc + y)
        if self.a >= 360 * self.n_rot:
            self.drawing_complete = True
            self.t.hideturtle()

    def clear(self):
        self.t.clear()

class SpiroAnimator:
        def __init__(self, N):

            self.deltaT = 10
            self.width = turtle.window_width()
            self.height = turtle.window_height()
            self.spiros = []
            for i in range(N):
                self.deltaT = 10
                rparams = self.gen_random_params()
                spiro = Spiro(*rparams)
                self.spiros.append(spiro)
                turtle.ontimer(self.update, self.deltaT)

        def gen_random_params(self):

            width, height = self.width, self.height
            R = random.randint(50, min(width, height) // 2)
            r = random.randint(10, 9 * R // 10)
            l = random.uniform(0.1, 0.9)
            xc = random.randint(-width // 2, width // 2)
            yc = random.randint(-height // 2, height // 2)
            col = (random.random(),
                   random.random(),
                   random.random())

            return (xc, yc, col, R, r, l)

        def restart(self):

            for spiro in self.spiros:
                spiro.clear()
                rparams = self.gen_random_params()
                spiro.setparams(*rparams)
                spiro.restart()

        def update(self):

            n_complete = 0
            for spiro in self.spiros:
                spiro.update()
                if spiro.drawing_complete:
                    n_complete += 1
            if n_complete == len(self.spiros):
                self.restart()
            turtle.ontimer(self.update, self.deltaT)

        def toggle_turtles(self):

            for spiro in self.spiros:
                if spiro.t.isvisible():
                    spiro.t.hideturtle()
                else:
                    spiro.t.showturtle()


def save_drawing():

    turtle.hideturtle()
    date_str = (datetime.now().strftime("%d%b%Y-%H%M%S"))
    filename = "spiro-{}".format(date_str)
    print("Saving drawing to {}.eps/png".format(filename))
    canvas = turtle.getcanvas()
    canvas.postscript(file = filename + '.eps')
    Image.save(filename + '.png', 'png')
    turtle.showturtle()

def main():

    print("Generating spirograph...")
    desc_str = """This program draws Spirographs using the Turtle module. When run with no arguments, it draws random spirographs.

    Terminology:

    R: radius of outer circle
    r: radius of inner circle
    l: ratio of hole distance to r
    """
    parser = argparse.ArgumentParser(description = desc_str)
    parser.add_argument('--sparams', nargs=3, dest='sparams', required=False, help="The three arguments in sparams: R, r, l.")

    args = parser.parse_args()
    turtle.setup(width=0.8)
    turtle.shape('turtle')
    turtle.title("Spirographs")
    turtle.onkey(save_drawing, "s")
    turtle.listen()

    turtle.hideturtle()

    if args.sparams:
        params = [float(x) for x in args.sparams]
        col = (0.0, 0.0, 0.0)
        spiro = Spiro(0, 0, col, *params)
        spiro.draw()
    else:
        spiro_anim = SpiroAnimator(4)
        turtle.onkey(spiro_anim.toggle_turtles, "t")
        turtle.onkey(spiro_anim, "space")
    turtle.mainloop()

if __name__ == '__main__':
    main()
