#!/usr/bin/env python

from SimpleCV import *

cam = Kinect()
size = cam.getDepth().size()
size = (size[0] + size[0], size[1])
disp = Display(size)

screen = True

UP = 273
DOWN = 274
RIGHT = 275
LEFT = 276

W = 119
A = 97
S = 115
D = 100

x, y, w, h = 24, 62, 570, 460

while not disp.isDone():

    orig = cam.getDepth()
    img = orig.copy()

    img = img.stretch(0, 250)

    if disp.mouseLeft:
        screen = not screen
    
    if screen:
        normal = cam.getImage()
        
        shifted = Image(normal.size())

        #pos = (0, -20)
        #shifted = shifted.blit(normal, pos)

        for index in range(len(disp.pressed)):
            if disp.pressed[index] == 1:
                print index, "was pressed"

        if disp.pressed[UP]:
            y -= 1
        if disp.pressed[DOWN]:
            y += 1
        if disp.pressed[RIGHT]:
            x += 1
        if disp.pressed[LEFT]:
            x -= 1
        
        if disp.pressed[W]:
            h += 1
        if disp.pressed[S]:
            h -= 1
        if disp.pressed[A]:
            w -= 1
        if disp.pressed[D]:
            w += 1

        shifted = normal.crop(x, y, w, h).scale(640, 480)
       
        blank = Image((640, 480)).blit(shifted, alphaMask=orig.stretch(200))

        side = blank.sideBySide(img).copy()

        print (x, y, w, h)

    else:
        #orig = cam.getImage()
        side = orig.sideBySide(img).copy()
    
    side.save(disp)


