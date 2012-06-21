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

img_HSV = cv.CreateImage(frame_size, frame.depth, frame.nChannels)

HueUp = 190#173.4
HueLw = 100#58.65

Sat = 70.0


def func(pixel):
    h, s, v = pixel
    if (h >= 0) and (h <= 50) and (s >= 58.65) and (s <= 173.4):
        return pixel
    else:
        return [0, 255, 0]


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

    cv.CvtColor(video, img_HSV, cv.CV_BGR2HSV)

    arr = cv2array(img_HSV)
    
    arr = np.array(map(lambda x: map(func, x), arr)).astype(np.uint8)

    img_HSV = array2cv(arr)

    cv.CvtColor(img_HSV, img_HSV, cv.CV_HSV2BGR)

    cv.ShowImage("HSV2", img_HSV)

    #video_arr = cv2array(video)

    #d3 = np.dstack((depth_arr, depth_arr, depth_arr))
    #both = np.hstack((video_arr, d3))
 
    #cv.ShowImage("skinmask", array2cv(both))

    print "Hue is being kept in the range of [", HueLw, ",", HueUp, "] and Sat is at [", 0, ",", Sat, "]"

    c = cv.WaitKey(10)
    if c != -1:
        if c == 27:
            break
        elif c == 63232:
            print "UP"
            HueUp += 0.25
        elif c == 63233:
            print "DOWN"
            HueUp -= 0.25
        elif c == 63234:
            print "LEFT"
            HueLw += 0.25
        elif c == 63235: 
            print "RIGHT"
            HueLw -= 0.25
        elif c == 119:
            Sat += 1
        elif c == 115:
            Sat -= 1
        else:
            print "button", c, "pressed"


