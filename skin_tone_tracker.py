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

Hue1 = cv.CreateImage(frame_size, cv.IPL_DEPTH_8U, 1)
Sat1 = cv.CreateImage(frame_size, cv.IPL_DEPTH_8U, 1)
Val1 = cv.CreateImage(frame_size, cv.IPL_DEPTH_8U, 1)

cv.SetZero(Hue1)
cv.SetZero(Sat1)
cv.SetZero(Val1)

Hue2 = cv.CreateImage(frame_size, cv.IPL_DEPTH_8U, 1)
Sat2 = cv.CreateImage(frame_size, cv.IPL_DEPTH_8U, 1)
Val2 = cv.CreateImage(frame_size, cv.IPL_DEPTH_8U, 1)

cv.SetZero(Hue2)
cv.SetZero(Sat2)
cv.SetZero(Val2)

mask = cv.CreateImage(frame_size, cv.IPL_DEPTH_8U, 1)

HueUp = 173.4
HueLw = 58.65

SatUp = 50.0
SatLw = 0.0

ValUp = 255.0
ValLw = 0.0

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
    cv.Split(img_HSV, Hue1, Sat1, Val1, None)

    cv.ShowImage("Hue1", Hue1)
    cv.ShowImage("Sat1", Sat1)
    cv.ShowImage("Val1", Val1)

    #           (src,  dest,   border, upper limit  type    [CV_THRESH_TOZERO, CV_THRESH_TOZERO_INV]

    #cv.Threshold(Hue1, Hue2, 255, 255, cv.CV_THRESH_TRUNC)
    #print cv2array(Hue1)

    cv.Threshold(Hue1, Hue2, HueLw, 255, cv.CV_THRESH_TOZERO)
    cv.Threshold(Hue2, Hue2, HueUp, 255, cv.CV_THRESH_TOZERO_INV)

    cv.Threshold(Sat1, Sat2, SatLw, 255, cv.CV_THRESH_TOZERO)
    cv.Threshold(Sat2, Sat2, SatUp, 255, cv.CV_THRESH_TOZERO_INV)

    cv.Threshold(Val1, Val2, ValLw, 255, cv.CV_THRESH_TOZERO)
    cv.Threshold(Val2, Val2, ValUp, 255, cv.CV_THRESH_TOZERO_INV)
 
    #cv.Threshold(Val1, Val2, 255, 255, cv.CV_THRESH_TRUNC)
    #cv.CloneImage(Val1, Val2)
    #Val2 = Val1
    

    #cv.Threshold(Sat1, Sat2, 0, 255, cv.CV_THRESH_BINARY)
    #cv.Threshold(Val1, Val2, 0, 255, thresholdType)

    """

    Sat should be in [0, 50]
    Hue should be in [0.23, 0.68] or [58.65, 173.4] 

    """
    """
def func(pixel):
    h, s, v = pixel
    if (h >= 0) and (h <= 50) and (s >= 58.65) and (s <= 173.4):
        return pixel
    else:
        return [0, 255, 0]
    """
    

    cv.ShowImage("Hue2", Hue2)
    cv.ShowImage("Sat2", Sat2)
    cv.ShowImage("Val2", Val2)

    cv.Merge(Hue2, Sat2, Val2, None, img_HSV)
    cv.CvtColor(img_HSV, img_HSV, cv.CV_HSV2BGR)

    cv.ShowImage("HSV2", img_HSV)

    depth_arr = cv2array(mask)
    video_arr = cv2array(video)

    d3 = np.dstack((depth_arr, depth_arr, depth_arr))
    both = np.hstack((video_arr, d3))
 
    cv.ShowImage("skinmask", array2cv(both))

    print "Hue [", HueLw, ",", HueUp, "], Sat [", SatLw, ",", SatUp, "], Val [", ValLw, ",", ValUp, "]"

    c = cv.WaitKey(10)
    if c != -1:
        if c == 27:
            break
        elif c == 63232:
            HueUp += 1
        elif c == 63233:
            HueUp -= 1
        elif c == 63234:
            HueLw += 1
        elif c == 63235: 
            HueLw -= 1
        
        elif c == 119:
            SatUp += 1
        elif c == 115:
            SatUp -= 1
        elif c == 97:
            SatLw += 1
        elif c == 100:    
            SatLw -= 1

        elif c == 105:
            ValUp += 1
        elif c == 107:
            ValUp -= 1
        elif c == 106:
            ValLw += 1
        elif c == 108:    
            ValLw -= 1

        else:
            print "button", c, "pressed"


