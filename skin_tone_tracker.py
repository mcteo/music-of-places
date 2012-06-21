#!/usr/bin/env python

import numpy as np, cv
from freenect import sync_get_video as get_video, sync_get_depth as get_depth

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

def cv21darray(im):
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
    #a.shape = (1, 1, im.nChannels)
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

(raw_video, _) = get_video()
cv.WaitKey(10)
frame = cv.GetImage(cv.fromarray(raw_video))
cv.CvtColor(frame, frame, cv.CV_RGB2BGR)
cv.Flip(frame, frame, 1)

frame_size = cv.GetSize(frame)
"""
img_YCrCb = cv.CreateImage(frame_size, frame.depth, frame.nChannels)
chan_Y  = cv.CreateImage(frame_size, cv.IPL_DEPTH_8U, 1)
chan_Cr = cv.CreateImage(frame_size, cv.IPL_DEPTH_8U, 1)
chan_Cb = cv.CreateImage(frame_size, cv.IPL_DEPTH_8U, 1)
"""
mask = cv.CreateImage(frame_size, cv.IPL_DEPTH_8U, 1)

skin_colours = []
depth_arr = cv2array(mask)

def onMouse(event, x, y, flags, params):

    event2str = {
        cv.CV_EVENT_MOUSEMOVE : "Mouse movement",
        cv.CV_EVENT_LBUTTONDOWN : "Left button down",
        cv.CV_EVENT_RBUTTONDOWN : "Right button down",
        cv.CV_EVENT_MBUTTONDOWN : "Middle button down",
        cv.CV_EVENT_LBUTTONUP : "Left button up",
        cv.CV_EVENT_RBUTTONUP : "Right button up",
        cv.CV_EVENT_MBUTTONUP : "Middle button up",
        cv.CV_EVENT_LBUTTONDBLCLK : "Left button double click",
        cv.CV_EVENT_RBUTTONDBLCLK : "Right button double click",
        cv.CV_EVENT_MBUTTONDBLCLK : "Middle button double click",
    }

    flag2str = {
        cv.CV_EVENT_FLAG_LBUTTON : "Left button pressed",
        cv.CV_EVENT_FLAG_RBUTTON : "Right button pressed",
        cv.CV_EVENT_FLAG_MBUTTON : "Middle button pressed",
        cv.CV_EVENT_FLAG_CTRLKEY : "Control key pressed",
        cv.CV_EVENT_FLAG_SHIFTKEY : "Shift key pressed",
        cv.CV_EVENT_FLAG_ALTKEY : "Alt key pressed",
    }

    fflags = []
    while (flags > 0):
        bigger = filter(lambda x: x <= flags, [1, 2, 4, 8, 16, 32])
        fflags.append(bigger[-1])
        flags -= bigger[-1]

    #print "got a", event2str[event], "event @ (", x, ",", y, ") with[", "|".join(map(lambda x: flag2str[x], fflags)), "] flags"

    (video, depth) = params

    if event == cv.CV_EVENT_LBUTTONUP:
        if (x < 640) and (y < 479) and (x > 0) and (y > 0):
            skin_colours.append( ",".join(map(lambda x: str(x), video[x][y])))

cv.NamedWindow("skinmask")

while True:
    (raw_depth, _) = get_depth()
    (raw_video, _) = get_video()

    np.clip(raw_depth, 0, (2**10)-1, raw_depth)
    raw_depth = raw_depth >> 2
    raw_depth = raw_depth.astype(np.uint8)#numpy.dstack((raw_depth, raw_depth, raw_depth))

    video = cv.GetImage(cv.fromarray(raw_video))
    cv.CvtColor(video, video, cv.CV_RGB2BGR) 
    cv.Flip(video, video, 1)

    depth = cv.GetImage(cv.fromarray(raw_depth))
    cv.Flip(depth, depth, 1)










    # Just too slow to even think about implementing in pure python
    # Literally 1 frame every 14 seconds

    """

    cv.CvtColor(video, img_YCrCb, cv.CV_RGB2YCrCb)
    cv.Split(img_YCrCb, chan_Y, chan_Cr, chan_Cb, None)

    #pY =  chan_Y#cv2array(chan_Y)
    #pCr = chan_Cr#cv2array(chan_Cr)
    #pCb = chan_Cb#cv2array(chan_Cb)
    #pMask = mask#cv2array(mask)

    pY =  np.array(cv.GetMat(chan_Y))#.astype(np.uint8)
    pCr = np.array(cv.GetMat(chan_Cr))#.astype(np.uint8)
    pCb = np.array(cv.GetMat(chan_Cb))#.astype(np.uint8)
    pMask = np.array(cv.GetMat(mask))#.astype(np.uint8)

    cv.SetZero(mask) 
   
    print "hello2"

    for x in range(mask.height-1):
        for y in range(mask.width-1):

            yz  = pY[x][y]
            cr = pCr[x][y]
            cb = pCb[x][y]
            cb -= 109 
            cr -= 152
  
            x1 = (819 * cr - 614 * cb) / 32 + 51;  
            y1 = (819 * cr + 614 * cb) / 32 + 77;  
            x1 = x1 * 41 / 1024;  
            y1 = y1 * 73 / 1024;  
            value = x1 * x1 + y1 * y1;  
   
            if ( yz < 100):
                if value < 700:
                    pMask[x][y] = 255
                else:
                    pMask[x][y] = 0
            else:
                if  value < 850:
                    pMask[x][y] = 255
                else:
                    pMask[x][y] = 0
    """

    
    depth_arr = cv2array(mask)
    video_arr = cv2array(video)

    # Even slower method!
    # literally about 1 frame every 25 seconds!!!

    """
    for x in range(mask.height-1):
        for y in range(mask.width-1):
            if ",".join(map(lambda x: str(x), video_arr[x][y])) in skin_colours:
                depth_arr[x][y] = 255
            else:
                depth_arr[x][y] = 0

    cv.SetMouseCallback("skinmask", onMouse, (video_arr, depth_arr))
    
    print skin_colours
    """

    d3 = np.dstack((depth_arr, depth_arr, depth_arr))
    both = np.hstack((video_arr, d3))
 
    cv.ShowImage("skinmask", array2cv(both))

    c = cv.WaitKey(10)
    if c != -1:
        if c == 27:
            break
        else:
            print "button", c, "pressed"


