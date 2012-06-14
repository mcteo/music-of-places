'''
Created on Jun 13, 2012

@author: thomasdunne
'''

from SimpleCV import *
import time

cam = Kinect()
disp = Display()
time.sleep(0.05)

_method = "motion"


hc = HaarCascade("profile.xml")

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

        frame1 = cam.getImage().flipHorizontal()
        time.sleep(0.2)
        frame2 = cam.getImage().flipHorizontal()
        time.sleep(0.2)
        frame3 = cam.getImage().flipHorizontal()
        time.sleep(0.2)

        diff = frame1 - frame2
        diff2 = frame2 - frame3

        #diff.sideBySide(diff2).show()

        #diff3 = diff.__and__(diff2)
        diff3 = diff.copy()

        diff3 = diff3.dilate(5)
        diff3 = diff3.colorDistance(Color.BLACK).threshold(100)#.stretch(100, 255)
        blobs = diff3.findBlobs()#rect=(0, 0, diff.width, diff.height))
        if blobs:
            blobs.draw(autocolor=True)
        diff3 = diff3.applyLayers()


        frame3.sideBySide(diff3).show()

        """
        grays = diff.colorDistance(Color.BLACK).dilate(20)
        blobs = grays.findBlobs()

        if blobs:
            seed_blob = blobs[-1]
            left, right, top, bottom = seed_blob.x, seed_blob.x, seed_blob.y, seed_blob.y

            for blob in blobs:
                if blob.minX() < left:
                    left = blob.minX()
                elif blob.maxX() > right:
                    right = blob.maxX()
                if blob.minY() < top:
                    top = blob.minY()
                elif blob.maxY() > bottom:
                    bottom = blob.maxY()

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


