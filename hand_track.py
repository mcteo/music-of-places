#!/usr/bin/env python

#from SimpleCV import *
import cv
import time
import numpy as np
from freenect import sync_get_depth as get_depth, sync_get_video as get_video

def cv2array(im):
    depth2dtype = {
        cv.IPL_DEPTH_8U: 'uint8',
        cv.IPL_DEPTH_8S: 'int8',
        cv.IPL_DEPTH_16U: 'uint16',
        cv.IPL_DEPTH_16S: 'int16',
        cv.IPL_DEPTH_32S: 'int32',
        cv.IPL_DEPTH_32F: 'float32',
        cv.IPL_DEPTH_64F: 'float64',
    }

    arrdtype = im.depth
    a = np.fromstring( im.tostring(), dtype = depth2dtype[im.depth], count = im.width * im.height * im.nChannels)
    a.shape = (im.height, im.width, im.nChannels)
    return a

def array2cv(a):
    dtype2depth = {
        'uint8':   cv.IPL_DEPTH_8U,
        'int8':    cv.IPL_DEPTH_8S,
        'uint16':  cv.IPL_DEPTH_16U,
        'int16':   cv.IPL_DEPTH_16S,
        'int32':   cv.IPL_DEPTH_32S,
        'float32': cv.IPL_DEPTH_32F,
        'float64': cv.IPL_DEPTH_64F,
    }
    try:
        nChannels = a.shape[2]
    except:
        nChannels = 1
    cv_im = cv.CreateImageHeader((a.shape[1], a.shape[0]), dtype2depth[str(a.dtype)], nChannels)
    cv.SetData(cv_im, a.tostring(), a.dtype.itemsize * nChannels * a.shape[1])
    return cv_im


while True:

    (raw_depth, _) = get_depth()
    (raw_video, _) = get_video()

    np.clip(raw_depth, 0, (2**10)-1, raw_depth)
    raw_depth = raw_depth >> 2
    raw_depth = raw_depth.astype(np.uint8)#np.dstack((raw_depth, raw_depth, raw_depth))

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
            cv.Circle(video, depthP, 5, (255, 255, 0), 2)


        font = cv.InitFont(cv.CV_FONT_HERSHEY_DUPLEX, 1, 1)
        cv.PutText(video, "Num of Fingers: " + str(fingerNum), (50, 50), font, (255, 255, 255)) 


    depth_arr = cv2array(depth)
    video_arr = cv2array(video)

    d3 = np.dstack((depth_arr, depth_arr, depth_arr))
    both = np.hstack((video_arr, d3))
 
    cv.ShowImage("video - depth", array2cv(both))
    #cv.ShowImage("depth", depth)
    #cv.ShowImage("rgb", video)

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


