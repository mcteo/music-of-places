#!/usr/bin/env python

import cv, time
from freenect import sync_get_depth as get_depth, sync_get_video as get_video

#ctx = fn.init()
#if fn.num_devices(ctx) > 0:
#    dev = fn.open_device(ctx, 0)
#    
#curr_tilt_state = fn.get_tilt_state(dev)
#curr_tilt_degs = fn.get_tilt_degs(curr_tilt_state)
        
#print "Current Angle:", curr_tilt_degs
        
#fn.set_tilt_degs(dev, 15)
#fn.shutdown(ctx)

raw_sample = None
while raw_sample == None:
    (raw_sample, _) = get_video()

sample_screen = cv.GetImage(cv.fromarray(raw_sample))
cv.Flip(sample_screen, sample_screen, 1)
cv.CvtColor(sample_screen, sample_screen, cv.CV_RGB2BGR)
screen_size = cv.GetSize(sample_screen)

colour_image = cv.CreateImage(screen_size, 8, 3)
grey_image = cv.CreateImage(screen_size, cv.IPL_DEPTH_8U, 1)
moving_average = cv.CreateImage(screen_size, cv.IPL_DEPTH_32F, 3)

cv.Smooth(sample_screen, sample_screen, cv.CV_GAUSSIAN, 3, 0)
difference = cv.CloneImage(sample_screen)
temp = cv.CloneImage(sample_screen)
cv.ConvertScale(sample_screen, moving_average, 1.0, 0.0)

while True: 
    (raw_image, _) = get_video()
    colour_image = cv.GetImage(cv.fromarray(raw_image))
    cv.Flip(colour_image, colour_image, 1)
    cv.CvtColor(colour_image, colour_image, cv.CV_RGB2BGR)

    cv.Smooth(colour_image, colour_image, cv.CV_GAUSSIAN, 3, 0)
    cv.RunningAvg(colour_image, moving_average, 0.020, None)
    
    cv.ConvertScale(moving_average, temp, 1.0, 0.0)
    cv.AbsDiff(colour_image, temp, difference)
    cv.CvtColor(difference, grey_image, cv.CV_RGB2GRAY)
    cv.Threshold(grey_image, grey_image, 70, 255, cv.CV_THRESH_BINARY)

    cv.Dilate(grey_image, grey_image, None, 18)
    cv.Erode(grey_image, grey_image, None, 10)

    storage = cv.CreateMemStorage(0)
    contour = cv.FindContours(grey_image, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
    points = []

    while contour:
        bound_rect = cv.BoundingRect(list(contour))
        contour = contour.h_next()

        pt1 = (bound_rect[0], bound_rect[1])
        pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
        points.append(pt1)
        points.append(pt2)
        cv.Rectangle(colour_image, pt1, pt2, cv.CV_RGB(255, 0, 0), 1)

    cv.ShowImage("Target", colour_image)

    c = cv.WaitKey(7)
    if c == 27:
        break
    elif c != -1:
        print "Button", c, "was pressed"

    #depth = depth.astype(numpy.uint8)
    
    #depth = numpy.dstack((depth, depth, depth)).astype(numpy.uint8)
    #d = numpy.hstack((depth, rgb)) 
    
    #cv.ShowImage("depth", cv.fromarray(numpy.array(d[::1, ::1, ::-1])))

"""
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
"""

