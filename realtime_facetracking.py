#!/usr/bin/env python

import numpy, cv, time
from freenect import sync_get_depth as get_depth, sync_get_video as get_video

#ctx = fn.init()
#if fn.num_devices(ctx) > 0:
#    dev = fn.open_device(ctx, 0)
#    
#curr_tilt_state = fn.get_tilt_state(dev)
#curr_tilt_degs = fn.get_tilt_degs(curr_tilt_state)
        
#print "Current Angle:", curr_tilt_degs
        
#fn.set_tilt_degs(dev, 15)
#fn.shutdown(ctx)
last_time = time.time()-10

while True: 
    (depth,_), (rgb,_) = get_depth(), get_video()

    #depth = depth.astype(numpy.uint8)
    
    #depth = numpy.dstack((depth, depth, depth)).astype(numpy.uint8)
    #d = numpy.hstack((depth, rgb)) 
    
    #cv.ShowImage("depth", cv.fromarray(numpy.array(d[::1, ::1, ::-1])))

    img = cv.fromarray(rgb)
    cv.Flip(img, img, 1)
    cv.CvtColor(cv.fromarray(rgb), img, cv.CV_RGB2BGR)

    grey = cv.CreateImage(cv.GetSize(img), 8, 1)
    cv.CvtColor(img, grey, cv.CV_BGR2GRAY)
    eig = cv.CreateImage(cv.GetSize(img), 32, 1)
    temp = cv.CreateImage(cv.GetSize(img), 32, 1)

    quality = 0.01
    min_distance = 10

    #features = cv.GoodFeaturesToTrack(grey, eig, temp, 100, 0.04, 1.0, None, useHarris = True)
    #for (x, y) in features:
    #    print "feature found at", x, y
    #    cv.Circle(img, (int(x), int(y)), 3, (0, 255, 0), -1, 8, 0)

    # Update the template ever 1 seconds
    if (time.time() - last_time) > 1:
    
        hc = cv.Load("face2.xml")
        faces = cv.HaarDetectObjects(grey, hc, cv.CreateMemStorage(), 1.2, flags = cv.CV_HAAR_DO_CANNY_PRUNING, min_size=(20, 20))
   
        for face in faces:
            if len(face[0]) == 4:
                (x, y, w, h) = face[0]
                cv.Rectangle(img, (x-5, y-5), (x+w+5, y+h+5), (0, 255, 0), 1)#, lineType=8, shift=0)
                
                #haar = False

                header = cv.GetImage(img)
                cv.SetImageROI(header, (x, y, w, h))
                template = cv.CloneImage(header)
                cv.ResetImageROI(header)
                W, H = cv.GetSize(img)
                w, h = cv.GetSize(template)
                width = W - w + 1
                height = H - h + 1
                result = cv.CreateImage((width, height), 32, 1)
 
                print (w, h)

                cv.ShowImage("template", template)
                last_time = time.time()
    
    try:
        cv.MatchTemplate(img, template, result, cv.CV_TM_SQDIFF)
        (min_x, max_y, minloc, maxloc) = cv.MinMaxLoc(result)
        (x, y) = minloc
        cv.Rectangle(img, (int(x), int(y)), (int(x) + w, int(y) + h), (255,255,255), 1, 0)
    except NameError:
        print ":O   I haven't found a single face yet!"

    cv.ShowImage("HaarCascade Face Detection", img)
    cv.WaitKey(5)

"""
import cv
img = cv.LoadImageM("building.jpg", cv.CV_LOAD_IMAGE_GRAYSCALE)
eig_image = cv.CreateMat(img.rows, img.cols, cv.CV_32FC1)
temp_image = cv.CreateMat(img.rows, img.cols, cv.CV_32FC1)
for (x,y) in cv.GoodFeaturesToTrack(img, eig_image, temp_image, 10, 0.04, 1.0, useHarris = True)
    print "good feature at", x,y
    cv.Circle (image, (x, y), 3, (0, 255, 0), -1, 8, 0)


# create the wanted images
eig = cv.CreateImage (cv.GetSize (grey), 32, 1)
temp = cv.CreateImage (cv.GetSize (grey), 32, 1)
# the default parameters
quality = 0.01
min_distance = 10
# search the good points
features = cv.GoodFeaturesToTrack(grey, eig, temp, MAX_COUNT, quality, min_distance, None, 3, 0, 0.04)
for (x,y) in features:
    print "Good feature a: "+x+','+y
    cv.Circle (image, (x, y), 3, (0, 255, 0), -1, 8, 0)

"""

"""
cam = Kinect()
size = cam.getDepth().size()
disp = Display((size[0]*2, size[1]))

while not disp.isDone():

    img1 = cam.getImage().flipHorizontal()
    img2 = cam.getDepth().flipHorizontal()

    img2 = img2.stretch(0, 150)
    
    img2 = img2.edges()
    
    #blobs = img2.findBlobs()
    #blobs.draw()
    
    img2 = img2.applyLayers()

    side = img1.sideBySide(img2)
    side.save(disp)
    
    time.sleep(0.05)
"""
"""
def doloop():
    global depth, rgb
    while True:
        # Get a fresh frame
        (depth,_), (rgb,_) = get_depth(), get_video()
        
        # Build a two panel color image
        d3 = np.dstack((depth,depth,depth)).astype(np.uint8)
        da = np.hstack((d3,rgb))
        
        # Simple Downsample
        cv.ShowImage('both',cv.fromarray(np.array(da[::2,::2,::-1])))
        cv.WaitKey(5)
        
doloop()
"""


