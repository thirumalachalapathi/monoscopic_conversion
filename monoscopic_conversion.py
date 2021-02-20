import cv2
import os
import shutil
import glob
from detecto.utils import split_video
import numpy as np


if __name__ == '__main__':

    ## To get FPS(frames per second) of video
    video = cv2.VideoCapture("D:/suction_cannula/resize/6b165766-bd39-4389-b1b0-9eaa0de8954e.mp4")
    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    if int(major_ver) < 3:
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
        print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS):{0}".format(int(fps)))
    else:
        fps = int(video.get(cv2.CAP_PROP_FPS))
        print("Fames per second using video.get(cv2.CAP_PROP_FPS):{0}".format(fps))
    video.release()


    #we will store the frames getting from video inside "images" folder
    os.mkdir('images')
    #After conversion of each frame  from stereoscopic to monoscopic we will store them inside "Resized" folder
    os.mkdir('Resized')
    # split_video('video file path', 'image save path', frame size)
    split_video('D:/suction_cannula/resize/6b165766-bd39-4389-b1b0-9eaa0de8954e.mp4', 'images/', step_size=1)
    inputFolder = 'images'
    i = 0


    ### monoscopic conversion of stereoscopic images
    for count in range(len(os.listdir(inputFolder))):
        image = inputFolder + '/frame' + str(count) + '.jpg'

        img = cv2.imread(image)

        shapeTuple = img.shape
        height = shapeTuple[0]
        width = shapeTuple[1]
        if (height == 0):
            print('WARNING height == 0')
            height = 1  # avoid div by 0

        aspectRatio = width / height;
        # print('aspectratio:',aspectRatio)
        isStereo = True
        if (aspectRatio < 1.77778):
            isStereo = False

        stereoWidth = width
        monoscopicWidth = width
        if (isStereo):
            monoscopicWidth = int(width / 2)


        # ------------------------------------------------------------------------------------------------
        # Make monoscopic if necessary: Crop to LEFT
        # ------------------------------------------------------------------------------------------------
        if (isStereo):
            # crop to LEFT using numpy slicing.  0,0 is upper left. +x goes to the right. +y goes down.
            monoscopicImageLEFT = img[0: height, 0: monoscopicWidth]

            # crop to RIGHT using numpy slicing.  0,0 is upper left. +x goes to the right. +y goes down.
            # monoscopicImageRIGHT = img[0: height, monoscopicWidth: 2*monoscopicWidth]

        else:
            monoscopicImageLEFT = img;
            # monoscopicImageRIGHT = img

        # resize to 416 x 416
        newSize = (1920, 1080)
        imgResizedTo416x416 = cv2.resize(monoscopicImageLEFT, newSize)
        # imgResizedTo416x416 = cv2.resize(monoscopicImageRIGHT, newSize)

        cv2.imwrite("Resized/image%05i.jpg" % i, imgResizedTo416x416)
        i += 1
        cv2.waitKey()

    ## preparing video from monoscopic images
    img_array = []
    for filename in glob.glob('Resized/*.jpg'):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    out = cv2.VideoWriter('monoscopic5.avi', cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

    ### Remove the "images" and "Resized" directories
    dir1 = "images"
    dir2 = "Resized"
    cwd = os.getcwd()
    path1 = os.path.join(cwd, dir1)
    path2 = os.path.join(cwd, dir2)
    shutil.rmtree(path1)
    shutil.rmtree(path2)










