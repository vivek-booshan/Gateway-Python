# -*- coding: utf-8 -*-
from graphics import *

# Create graphics window titled 'My Window' of size 300 by 300 pixels
win = GraphWin('My Window', 300, 300)

# Draw Square
x0 = 50
y0 = 100
width = 150

p0 = Point(x0, y0)
p1 = Point(x0 + width, y0 + width) 

square = Rectangle(p0, p1) # Specify upper-left and lower-right points
square.setFill('green')
square.setOutline('green')
square.draw(win)

# Draw Triangle
p2 = Point(x0+width, y0)
p3 = Point(x0+width/2, y0 - width/2)
triangle = Polygon([p0, p2, p3]) # Note the []
triangle.setFill('blue')
triangle.setOutline('blue')
triangle.draw(win)

# Draw Point
p = Point(150, 80)
p.setFill('red')
p.draw(win)

# Close after mouse click
try:
    win.getMouse()    
    win.close()
except:
    pass

print(p0, p2, p3)