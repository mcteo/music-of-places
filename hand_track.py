#!/usr/bin/env python

from SimpleCV import *
import time

cam = Kinect()
size = cam.getDepth().size()
disp = Display((size[0]*2, size[1]))

while not disp.isDone():

    img1 = cam.getImage().flipHorizontal()
    img2 = cam.getDepth().flipHorizontal()

    img2 = img2.stretch(0, 150)
    
    img2 = img2.edges()
    
    #blobs = img2.findBlobs()
    #blobs.draw()
    
    img2 = img2.applyLayers()

    side = img1.sideBySide(img2)
    side.save(disp)
    
    time.sleep(0.05)

