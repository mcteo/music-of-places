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

img_YCrCb = cv.CreateImage(frame_size, frame.depth, frame.nChannels)
chan_Y  = cv.CreateImage(frame_size, cv.IPL_DEPTH_8U, 1)
chan_Cr = cv.CreateImage(frame_size, cv.IPL_DEPTH_8U, 1)
chan_Cb = cv.CreateImage(frame_size, cv.IPL_DEPTH_8U, 1)

mask = cv.CreateImage(frame_size, cv.IPL_DEPTH_8U, 1)

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

    cv.CvtColor(video, img_YCrCb, cv.CV_BGR2YCrCb)
    cv.Split(img_YCrCb, chan_Y, chan_Cr, chan_Cb, None)

    """
    cv.ShowImage("chan_Y", chan_Y)
    cv.ShowImage("chan_Cr", chan_Cr)
    cv.ShowImage("chan_Cb", chan_Cb)

    cv.WaitKey(-1)

    ""  
    IplImage *imgYCrCb = cvCreateImage(imageSize, img->depth, img->nChannels);  
    cvCvtColor(img,imgYCrCb,CV_BGR2YCrCb);  
    cvSplit(imgYCrCb, imgY, imgCr, imgCb, 0);  
    int y, cr, cb, l, x1, y1, value;  
    unsigned char *pY, *pCr, *pCb, *pMask;  
    """

    print "hello1"

    pY =  chan_Y#cv2array(chan_Y)  
    pCr = chan_Cr#cv2array(chan_Cr)
    pCb = chan_Cb#cv2array(chan_Cb)
    pMask = mask#cv2array(mask)
    cv.SetZero(mask) 
   
    print "hello2"

    for x in range(mask.height):
        for y in range(mask.width):

            y  = cv.Get2D(pY, x, y)
            cr = cv.Get2D(pCr, x, y)
            cb = cv.Get2D(pCb, x, y)
            cb -= 109 
            cr -= 152
  
            x1 = (819 * cr - 614 * cb) / 32 + 51;  
            y1 = (819 * cr + 614 * cb) / 32 + 77;  
            x1 = x1 * 41 / 1024;  
            y1 = y1 * 73 / 1024;  
            value = x1 * x1 + y1 * y1;  
   
            if ( y < 100):
                if value < 700:
                    cv.Set2D(pMask, x, y, 255)
                else:
                    cv.Set2D(pMask, x, y, 0)
            else:
                if  value < 850:
                    cv.Set2D(pMask, x, y, 255)
                else:
                    cv.Set2D(pMask, x, y, 0)
            

    depth_arr = pMask#cv2array(mask)
    video_arr = cv2array(video)

    d3 = np.dstack((depth_arr, depth_arr, depth_arr))
    
    print len(d3), len(d3[-1]), len(d3[-1][-1])
    
    
    both = np.hstack((video_arr, d3))
 
    cv.ShowImage("both", array2cv(both))

    c = cv.WaitKey(10)
    if c != -1:
        if c == 27:
            break
        else:
            print "button", c, "pressed"


