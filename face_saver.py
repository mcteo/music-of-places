#!/usr/bin/env python

import numpy, cv, time
from freenect import sync_get_depth as get_depth, sync_get_video as get_video

image_count = 0
last_time = time.time()-10

while True: 
    (depth,_), (rgb,_) = get_depth(), get_video()

    img = cv.fromarray(rgb)
    cv.Flip(img, img, 1)
    cv.CvtColor(cv.fromarray(rgb), img, cv.CV_RGB2BGR)

    grey = cv.CreateImage(cv.GetSize(img), 8, 1)
    cv.CvtColor(img, grey, cv.CV_BGR2GRAY)
    eig = cv.CreateImage(cv.GetSize(img), 32, 1)
    temp = cv.CreateImage(cv.GetSize(img), 32, 1)

    quality = 0.01
    min_distance = 10

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
                
                cv.SaveImage("images/face"+str(image_count)+".bmp", template)
                image_count += 1

                last_time = time.time()
    
    try:
        cv.MatchTemplate(img, template, result, cv.CV_TM_SQDIFF)
        (min_x, max_y, minloc, maxloc) = cv.MinMaxLoc(result)
        (x, y) = minloc
        cv.Rectangle(img, (int(x), int(y)), (int(x) + w, int(y) + h), (255,255,255), 1, 0)
    except NameError:
        print ":O   I haven't found a single face yet!"

    cv.ShowImage("HaarCascade Face Detection", img)
    key = cv.WaitKey(5)
    if key != -1:
        if key == 27:
            exit()


