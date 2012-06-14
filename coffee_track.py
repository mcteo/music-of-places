'''
Created on Jun 13, 2012

@author: thomasdunne
'''

from SimpleCV import *
import time

#cam = Kinect()
cam = VirtualCamera("coffee.mov", "video")
disp = Display()
time.sleep(0.05)

_method = "motion"


hc = HaarCascade("profile.xml")

def TPAtoATPA(TPA, dist):
    Result = []
    c = 0
    l = len(TPA)
    for a in range(0, l):
        found = False
        for b in range(0, c-1):
            if round(((TPA[a][0] - Result[b][0][0])**2 + (TPA[a][1] - Result[b][0][1])**2)**0.5) <= dist:
                found = True
                break
        if found:
            Result[b].append(TPA[a])
        else:
            Result.append([TPA[a]])
            c += 1
    return Result

def getTPABounds(TPA):
    L = len(TPA)
    if L < 0:
        return -1

    seed_blob = TPA[0]
    left, right, top, bottom = seed_blob[0], seed_blob[0], seed_blob[1], seed_blob[1]

    for TP in TPA:
        if TP[0] < left:
            left = TP[0]
        elif TP[0] > right:
            right = TP[0]
        if TP[1] < top:
            top = TP[1]
        elif TP[1] > bottom:
            bottom = TP[1]

    return ((left, top), (right, bottom))

def blobsToTPA(bs):
    tpa = []

    for i in bs:
        tpa.append((i.x, i.y))

    return tpa

while not disp.isDone():
    
    if _method == "haar":
        orig_img = cam.getImage().flipHorizontal().scale(320, 240)
        img = orig_img.copy()

        objs = img.findHaarFeatures(hc)

        if objs:
            for obj in objs:
                img.drawRectangle(obj.x, obj.y, obj.width(), obj.height(), (255, 0, 0), 2, -1)

        #orig_img.sideBySide(img).show()#save(disp)
        img.save(disp)

        #['eye.xml', 'face.xml', 'face2.xml', 'face3.xml', 'face4.xml', 'fullbody.xml', 'glasses.xml', 'left_ear.xml', 'left_eye2.xml', 'lefteye.xml', 'lower_body.xml', 'mouth.xml', 'nose.xml', 'profile.xml', 'right_ear.xml', 'right_eye.xml', 'right_eye2.xml', 'two_eyes_big.xml', 'two_eyes_small.xml', 'upper_body.xml', 'upper_body2.xml']

    elif _method == "motion":

        frame1 = cam.getImage().scale(640, 400)#.flipHorizontal()
        #time.sleep(0.2)
        frame2 = cam.getImage().scale(640, 400)#.flipHorizontal()
        #time.sleep(0.2)
        frame3 = cam.getImage().scale(640, 400)#.flipHorizontal()
        #time.sleep(0.2)

        diff = frame1 - frame2
        diff2 = frame2 - frame3

        #diff.sideBySide(diff2).show()

        diff3 = diff.__or__(diff2)
        #diff3 = diff.copy()

        mask = frame1.dilate(10).colorDistance(Color.BLACK).stretch(175)
        img = Image(frame1.size())
        img = img.blit(frame1, alphaMask=mask)

        diff3 = diff3.dilate(5).colorDistance(Color.BLACK).stretch(125)
        #diff3 = diff3.colorDistance(Color.BLACK).threshold(100)#.stretch(100, 255)

        img2 = Image(frame1.size())
        img2 = img2.blit(frame1, alphaMask=diff3)

        blobs = diff3.findBlobs()#rect=(0, 0, diff.width, diff.height))
        if blobs:
            blobs.draw(autocolor=True)
        
            tpa = blobsToTPA(blobs)
            print "tpa:", tpa

            atpa = TPAtoATPA(tpa, 125)
            print "atpa:", atpa

            for box in atpa:
                if len(box) < 2:
                    continue
                bounds = getTPABounds(box)
                print "bounds:", bounds

                bb = disp.pointsToBoundingBox(bounds[0], bounds[1])
                
                diff3.drawRectangle(bb[0], bb[1], bb[2], bb[3], Color.RED, 2, -1)
                img.drawRectangle(bb[0], bb[1], bb[2], bb[3], Color.RED, 2, -1)
                img2.drawRectangle(bb[0], bb[1], bb[2], bb[3], Color.RED, 2, -1)

                img = img.applyLayers()
                img2 = img2.applyLayers()

        diff3 = diff3.applyLayers()

        #img.sideBySide(diff3.invert()).show()
        img.sideBySide(img2).show()

        """
        grays = diff.colorDistance(Color.BLACK).dilate(20)
        blobs = grays.findBlobs()

            #print "1", frame1
            #print "2", frame2
            #print "3", diff
            #print "4", grays
            #print "5", blobs[-1].image, "***"
            #print len(blobs)

            blobs.draw(autocolor=True)
            grays = grays.applyLayers()

            bb = disp.pointsToBoundingBox((top, left), (bottom, right))
            frame2.drawRectangle(bb[0], bb[1], bb[2], bb[3], Color.GREEN, 2, -1)
            frame2 = frame2.applyLayers()

            frame2.sideBySide(grays).show()
        """

        #['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__getstate__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_mHeight', '_mMaxX', '_mMaxY', '_mMinX', '_mMinY', '_mSrcImgH', '_mSrcImgW', '_mWidth', '_pointInsidePolygon', '_updateExtents', 'above', 'angle', 'area', 'aspectRatio', 'below', 'blobImage', 'blobMask', 'bottomLeftCorner', 'bottomRightCorner', 'boundingBox', 'centroid', 'circleDistance', 'colorDistance', 'contains', 'contour', 'coordinates', 'corners', 'crop', 'distanceFrom', 'distanceToNearestEdge', 'doesNotContain', 'doesNotOverlap', 'draw', 'drawHoles', 'drawHull', 'drawMaskToLayer', 'drawMinRect', 'drawOutline', 'drawRect', 'extents', 'height', 'hull', 'hullImage', 'hullMask', 'hullRadius', 'image', 'isCircle', 'isContainedWithin', 'isNotContainedWithin', 'isRectangle', 'isSquare', 'left', 'length', 'm00', 'm01', 'm02', 'm10', 'm11', 'm12', 'm20', 'm21', 'mArea', 'mAspectRatio', 'mAvgColor', 'mBoundingBox', 'mContour', 'mConvexHull', 'mExtents', 'mHoleContour', 'mHortEdgeHist', 'mHu', 'mHullImg', 'mHullMask', 'mImg', 'mLabel', 'mLabelColor', 'mMask', 'mMinRectangle', 'mPerimeter', 'mVertEdgeHist', 'match', 'maxX', 'maxY', 'meanColor', 'minRect', 'minRectHeight', 'minRectWidth', 'minRectX', 'minRectY', 'minX', 'minY', 'notOnImageEdge', 'onImageEdge', 'overlaps', 'perimeter', 'pickle_skip_properties', 'points', 'radius', 'rectangleDistance', 'rectifyMajorAxis', 'right', 'rotate', 'seq', 'show', 'topLeftCorner', 'topRightCorner', 'width', 'x', 'y']


