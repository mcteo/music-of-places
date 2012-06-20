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

    cv.Threshold(depth, depth, 125, 255, cv.CV_THRESH_BINARY)
   
    temp = cv.CloneImage(depth)

    cv.Not(temp, temp)
    
    storage = cv.CreateMemStorage(0)
    contours = cv.FindContours(temp, storage, cv.CV_RETR_LIST, cv.CV_CHAIN_APPROX_SIMPLE)

    #cv.DrawContours(video, contours, (0, 255, 0), (0, 0, 255), 0)

    biggestContour = None
    defects = None
    fingerNum = 0

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

        raw_hull = cv.ConvexHull2(biggestContour, storage, cv.CV_CLOCKWISE, 0)
        hull = cv.ConvexHull2(biggestContour, storage, cv.CV_CLOCKWISE, 1)
        
        box = cv.MinAreaRect2(biggestContour)

        points = cv.BoxPoints(box)
        points = map(lambda x: (int(x[0]), int(x[1])), points)

        #cv.PolyLine(video, [points], True, (255, 0, 0), 2)
        cv.PolyLine(video, [hull], True, (200, 125, 75), 2)

        center = ( int(box[0][0]), int(box[0][1]) )
        cv.Circle(video, center, 3, (200, 125, 75), 2)

        filteredHull = []
        for i in range(len(hull) - 1):
            if ( ( (hull[i][0] - hull[i + 1][0])**2 + (hull[i][1] - hull[i + 1][1])**2  )**0.5 ) > (box[1][0] / 10):
                filteredHull.append(hull[i])
       
        defects = cv.ConvexityDefects(biggestContour, raw_hull, storage)

        #print defects

    if defects is not None:

        for defect in defects:

            startP = ( int(defect[0][0]), int(defect[0][1]) )
            endP = ( int(defect[1][0]), int(defect[1][1]) )
            depthP = ( int(defect[2][0]), int(defect[2][1]) )
            
            if ( (startP[1] < box[0][1]) or (depthP < box[0][1]) ) and \
                 ( startP[1] < depthP[1] ) and \
                 ( (( (startP[0] - depthP[0])**2 + (startP[1] - depthP[1])**2 )**0.5 ) > (box[1][1] / 6.5) ):
                fingerNum += 1
                cv.Line(video, startP, depthP, (0, 255, 0), 2) 


            cv.Circle(video, startP, 5, (255, 0, 0), 2)
            cv.Circle(video, depthP, 5, (0, 125, 125), 5)


        font = cv.InitFont(cv.CV_FONT_HERSHEY_DUPLEX, 1, 1)
        cv.PutText(video, "Num of Fingers: " + str(fingerNum), (50, 50), font, (255, 255, 255)) 

    # get biggest contour using conours.HNext and contours.Area;

    # biggestContour.ApproxPoly
    # draw

    #biggestContour.GetConvexHull

    #cv.WaitKey(1000)

    cv.ShowImage("depth", depth)
    cv.ShowImage("rgb", video)

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


