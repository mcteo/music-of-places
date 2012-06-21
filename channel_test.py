#!/usr/bin/env python

import numpy as np, cv, cv2
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
cv.CvtColor(frame, frame, cv.CV_BGR2RGB)
cv.Flip(frame, frame, 1)

frame_size = cv.GetSize(frame)

r1 = np.zeros(frame_size)
g1 = np.zeros(frame_size)
b1 = np.array([[255 for x in range(frame_size[0])] for y in range(frame_size[1])])

blank = np.zeros((480, 640))

while True:
    (raw_depth, _) = get_depth()
    (raw_video, _) = get_video()

    #np.clip(raw_depth, 0, (2**10)-1, raw_depth)
    #raw_depth = raw_depth >> 2
    #raw_depth = raw_depth.astype(np.uint8)#numpy.dstack((raw_depth, raw_depth, raw_depth))

    r1 = raw_video[::, ::, 0]
    g1 = raw_video[::, ::, 1]
    b1 = raw_video[::, ::, 2]

    r3 = np.dstack((r1, blank, blank)).astype(np.uint8)
    g3 = np.dstack((blank, g1, blank)).astype(np.uint8)
    b3 = np.dstack((blank, blank, b1)).astype(np.uint8)

    cv.ShowImage("Red1", array2cv(r3))
    cv.ShowImage("Green1", array2cv(g3))
    cv.ShowImage("Blue1", array2cv(b3))

    c = cv.WaitKey(10)
    if c != -1:
        if c == 27:
            break
        else:
            print "button", c, "pressed"


