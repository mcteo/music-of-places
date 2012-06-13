#!/usr/bin/env python

from SimpleCV import *
import time

cam = Kinect()

while True:
    img1 = cam.getImage().flipHorizontal()
    img2 = cam.getDepth().flipHorizontal()
    img2 = img2.stretch(0, 150).edges().findBlobs().draw()
    img3 = img1.sideBySide(img2)
    img3.show()
    time.sleep(0.05)

