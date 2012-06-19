#!/usr/bin/env python

#from SimpleCV import *
import cv
import time
import numpy
from freenect import sync_get_depth as get_depth, sync_get_video as get_video

while True:

    (raw_depth, _) = get_depth()
    (raw_video, _) = get_video()

    numpy.clip(raw_depth, 0, (2**10)-1, raw_depth)
    raw_depth = raw_depth >> 2
    raw_depth = raw_depth.astype(numpy.uint8)#numpy.dstack((raw_depth, raw_depth, raw_depth))

    video = cv.GetImage(cv.fromarray(raw_video))
    cv.CvtColor(video, video, cv.CV_RGB2BGR) 
    cv.Flip(video, video, 1)

    depth = cv.GetImage(cv.fromarray(raw_depth))
    cv.Flip(depth, depth, 1)

    cv.Threshold(depth, depth, 150, 255, cv.CV_THRESH_BINARY)
   
    temp = cv.CloneImage(depth)

    cv.Not(temp, temp)
    
    storage = cv.CreateMemStorage(0)
    contours = cv.FindContours(temp, storage, cv.CV_RETR_LIST, cv.CV_CHAIN_APPROX_SIMPLE)

    #cv.DrawContours(video, contours, (0, 255, 0), (0, 0, 255), 0)

    biggestContour = None

    area1 = 0
    area2 = 0
    
    while contours:
       
        area1 = cv.ContourArea(contours)
        if area1 > area2:
            area2 = area1
            biggestContour = contours
    
        #print area1, area2
        contours = contours.h_next()

    if biggestContour is not None:

        currentContour = cv.ApproxPoly(biggestContour, storage, cv.CV_POLY_APPROX_DP, cv.ArcLength(biggestContour) * 0.0025)
        cv.PolyLine(video, [currentContour], False, (0, 255, 0))

        biggestContour = currentContour

        hull = cv.ConvexHull2(biggestContour, storage, cv.CV_CLOCKWISE, 1)
        
        box = cv.MinAreaRect2(currentContour, storage)
        print "box:", box

        points = (box[0], box[1])
        print "points:", points
        
        cv.Rectangle(video, (int(box[0][0]), int(box[1][0])), (int(box[0][1]), int(box[1][1])), (255, 0, 0), 2)
        

        cv.PolyLine(video, [hull], True, (200, 125, 75), 2)

        #bb = cv.BoundingRect(points)
        #center = ( (bb[0]+bb[2]) / 2, (bb[1]+bb[3]) / 2)
        center = ( int( (points[0][0] + points[1][0]) / 2), int( (points[0][1] + points[1][1]) / 2) )
        cv.Circle(video, center, 3, (200, 125, 75), 2)
    
        


    # get biggest contour using conours.HNext and contours.Area;

    # biggestContour.ApproxPoly
    # draw

    #biggestContour.GetConvexHull

    #cv.WaitKey(1000)

    cv.ShowImage("rgb", video)
    cv.ShowImage("depth", depth)

    c = cv.WaitKey(10)
    if c != -1:
        if c == 27:
            break
        else:
            print "Button", c, "was pressed"

    """
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

    img2 = img2.stretch(0, 150)
    img2 = img2.edges()
    
    #blobs = img2.findBlobs()
    #blobs.draw()
    
    img2 = img2.applyLayers()

    side = img1.sideBySide(img2)
    side.save(disp)
    
    time.sleep(0.05)
    """


