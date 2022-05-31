# -*- coding: utf-8 -*-
from graphics import *
from math import sqrt
from random import randint
from numpy import mean as mean
# test for acceptable length, else tell user to try again
cont = True
while cont == True:
    length = int(input("Enter the length (200-1000): "))
    if length in range(200, 1001):
        cont = False
    else: 
        print("your values are out of range, please enter a value between 200 and 1000: ")


# Create graphics window
win = GraphWin('Night', length, length)

""" Write your code here """

#night sky

#generate black screen that spans the size of the window
p0_night = Point(0, 0)
p1_night = Point(length, length)

night_sky = Rectangle(p0_night, p1_night)
night_sky.setFill('black')
night_sky.setOutline('black')
night_sky.draw(win)

#stars; loop through 100 iterations, generating random points between (0,0) and (length, length)
for i in range(100):
    p = Point(randint(0, length), randint(0, length))
    p.setFill('white')
    p.draw(win)

#ground
gScY = (2/3) * length #ground starting coordinate y, starts from 2/3 the y axis
p0_ground = Point(0, gScY) 
p1_ground = Point(length, length) #spans the lower third of the window

ground = Rectangle(p0_ground, p1_ground)
ground.setFill('green')
ground.setOutline('green')
ground.draw(win)

#House

#house base

#house base starting coordinate y
#from length, y starting coordinate goes up a third and then up a sixth
bScY = length - ((1/3)*length + (1/6)*length) 
p0_base = Point((1/3)*length, bScY) #x coordinate starts 1/3 of the way in
p1_base = Point((2/3)*length, gScY) #x final coordinate starts at 2/3 the length

base = Rectangle(p0_base, p1_base)
base.setFill('grey')
base.setOutline('grey')
base.draw(win)

#house roof

#roof tip coordinate y; subtracts the ground, the house and then half the house height
rTcY = length - bScY - length*(1/12) 

p0_roof = Point((1/3)*length, bScY) #same start as p0_base
p1_roof = Point((2/3)*length, bScY) #same end as p1_base
p2_roof = Point((1/2)*length, rTcY) #midpoint between p0 and p1

roof = Polygon([p0_roof, p1_roof, p2_roof])
roof.setFill('darkred')
roof.setOutline('darkred')
roof.draw(win)

#house windows

'''first window'''
#p0_win is the top coord for the first window; generate coordinate starting from 1/5 house length and 1/3 the house height
x0, y0 = (1/3)*length + (1/15)*length, (1/2)*length + (1/18)*length
p0_win = Point(x0, y0)
#p1_win is the bottom coord for the first window; generate coordinate starting from 2/5 house length and 2/3 the house height
x1, y1 = (1/3)*length + (2/15)*length, (1/2)*length + (1/9)*length
p1_win = Point(x1, y1)

'''second window'''
#p2_win is the top coord for the second window; generate coordinate from 3/5 the house length and 1/3 the house height
x2, y2 = (1/3)*length + (1/5)*length, (1/2)*length + (1/18)*length
p2_win = Point(x2, y2)
#p3_win is the bottom coord for the second window; generate coordinate from 4/5 the house length and 2/3 the house height
x3, y3 = (1/3)*length + (4/15)*length, (1/2)*length + (1/9)*length
p3_win = Point(x3, y3)

window1 = Rectangle(p0_win, p1_win)
window1.setFill('yellow')
window1.setOutline('yellow')
window1.draw(win)

window2 = Rectangle(p2_win, p3_win)
window2.setFill('yellow')
window2.setOutline('yellow')
window2.draw(win)
# Close after mouse click
try:
    win.getMouse()    
    win.close()
except:
    pass