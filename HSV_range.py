#!/usr/bin/env python

import cv, numpy as np, matplotlib.pyplot as ml , sys, os, pickle
from freenect import sync_get_video as get_video

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

def get_channel_palettes(img):
    HSV = cv.CreateImage(cv.GetSize(img), img.depth, img.nChannels)
    cv.CvtColor(img, HSV, cv.CV_RGB2HSV)

    arr = cv2array(HSV)

    chanH = arr[::, ::, 0]
    chanS = arr[::, ::, 1]
    chanV = arr[::, ::, 2]

    countH = np.bincount(chanH.flatten())
    countS = np.bincount(chanS.flatten())
    countV = np.bincount(chanV.flatten())

    countH = np.hstack((countH, [0 for x in xrange(255 - len(countH))]))
    countS = np.hstack((countS, [0 for x in xrange(255 - len(countS))]))
    countV = np.hstack((countV, [0 for x in xrange(255 - len(countV))]))

    return (countH, countS, countV)

def add_diff_shapes(a, b, offset=(0, 0)):

    max_x = min(a.shape[0], b.shape[0])
    max_y = min(a.shape[1], b.shape[1])

    min_x = max(offset[0], 0)
    min_y = max(offset[1], 0)

    a[min_x:max_x:, min_y:max_y:] += b[min_x:max_x:, min_y:max_y:] 
    return a

def get_multi_channel_palettes(imgs):
    countH = countS = countV = 0
    
    for img in imgs:
        HSV = cv.CreateImage(cv.GetSize(img), img.depth, img.nChannels)
        cv.CvtColor(img, HSV, cv.CV_RGB2HSV)

        arr = cv2array(HSV)

        #print chanH.shape, chanS.shape, chanV.shape

        try:
            chanH = np.hstack((chanH, arr[::, ::, 0].flatten()))
            chanS = np.hstack((chanS, arr[::, ::, 1].flatten()))
            chanV = np.hstack((chanV, arr[::, ::, 2].flatten()))
        except UnboundLocalError:
            chanH = arr[::, ::, 0].flatten()
            chanS = arr[::, ::, 1].flatten()
            chanV = arr[::, ::, 2].flatten()

        countH += np.bincount(chanH.flatten())
        countS += np.bincount(chanS.flatten())
        countV += np.bincount(chanV.flatten())

    countH = np.hstack((countH, [0 for x in xrange(255 - len(countH))]))
    countS = np.hstack((countS, [0 for x in xrange(255 - len(countS))]))
    countV = np.hstack((countV, [0 for x in xrange(255 - len(countV))]))

    return (countH, countS, countV)

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "Usage:", sys.argv[0], "<image name>"
        exit(0)

    dir_name = sys.argv[1]

    names = filter(lambda x: x[0] != '.', os.listdir(dir_name))
    names = map(lambda x: dir_name + x, names)

    images = []

    for image in names:
        img = cv.LoadImage(image)
        images.append(img)    
        print "Opening file <", image, "> with size", cv.GetSize(img)
   
    (H, S, V) = get_multi_channel_palettes(images)

    pickle.dump((H, S, V), open("HSV_out.pickle", "w"))

    #[max(np.where(a==0)[0])+1:]

    N = 255

    ml.ylabel('Value')
    #ml.xticks(ind+width/2., ('G1', 'G2', 'G3', 'G4', 'G5') )
    #ml.yticks(np.arange(0,25,10))
    #ml.legend( (p1[0]), ('Men') )

    ind = np.arange(N)    # the x locations for the groups
    ml.title('Hue Channel')
    p1 = ml.bar(ind, H)
    ml.show()

    ind = np.arange(N)    # the x locations for the groups
    ml.title('Saturation Channel')
    p2 = ml.bar(ind, S)
    ml.show()
    
    ind = np.arange(N)    # the x locations for the groups
    ml.title('Value Channel')
    p3 = ml.bar(ind, V)
    ml.show()
    



