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

    (video, depth) = params

    if event == cv.CV_EVENT_LBUTTONUP:
        if (x < 640) and (y < 479) and (x > 0) and (y > 0):
            pass

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




    depth_arr = cv2array(depth)
    video_arr = cv2array(video)

    d3 = np.dstack((depth_arr, depth_arr, depth_arr))
    both = np.hstack((video_arr, d3))
 
    cv.ShowImage("both", array2cv(both))

    c = cv.WaitKey(10)
    if c != -1:
        if c == 27:
            break
        else:
            print "button", c, "pressed"


