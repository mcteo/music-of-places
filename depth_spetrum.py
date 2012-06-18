#!/usr/bin/env python

from SimpleCV import *

cam = Kinect()
size = cam.getDepth().size()
size = (size[0] + size[0], size[1])
disp = Display(size)

screen = True

def colourise(pixel):
    [r, g, b] = pixel
    [h, s, v] = colorsys.rgb_to_hsv(r, g, b)

    #we get (0, 0, v) - v between 90 and 255
    #output should be (h, 1, 1) - h being between 0 and 225
    colour = v

    h = ((colour-90) * 0.6470) / 175
    s = 1
    v = 255

    return colorsys.hsv_to_rgb(h, s, v)
    
    #return (int(r), int(b), int(g))


while not disp.isDone():

    orig = cam.getDepth()
    img = orig.copy()

    img = img.stretch(0, 250)

    if disp.mouseLeft:
        screen = not screen
    
    if screen:
        normal = cam.getImage()
        
        shifted = Image(normal.size())
        shifted = normal.crop(24, 62, 570, 460).scale(640, 480)
       
        img = img.applyPixelFunction(colourise)

        side = orig.sideBySide(img).copy()

    else:
        #orig = cam.getImage()
        side = orig.sideBySide(img).copy()
    
    side.save(disp)


