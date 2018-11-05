import cv2
import os
import argparse
import numpy as np
from skimage.measure import compare_ssim

parser = argparse.ArgumentParser()
parser.add_argument("--file", help="Video file i.e) xyz.mp4")
parser.add_argument("--method", help="defines method. SSIM: simple & fast.ORB: SIFT: FLANN_SIFT, FLANN_ORB: experimental. you need to install opencv-python, opencv-contrib-python 3.4.2.16. If you want to show next image, press any in keyboard. not click <close> button. it occurs infinte loop",default="SSIM")
parser.add_argument("--debug", help="if Y, shows print. otherwise: dont show anything. default: Y", default="Y")
parser.add_argument("--tolerance", help="If you use SSIM, defines tolerance. default: 0.4", default=0.4)
parser.add_argument("--factor", help="If you use FLANN, defines factor. default: 0.7", default=0.7)
args = parser.parse_args()

folder_name = "images_" + args.file

# tolerance defines to save or not
tolerance = args.tolerance

# with opencv2, Open video
video = cv2.VideoCapture(args.file)
count = 0

ret = None
image = None
grayOrigin = None
length = None

if video.isOpened():
    length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)

    if args.debug == "Y":
        print("Filename: ", args.file)
        print("Video size: " + str(width) + "x" + str(height))
        print("frame size: ", length)
        print("fps: ", fps)
        print("method: ", args.method)
        print("tolerance: ", tolerance)

    ret, image = video.read()
    grayOrigin = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if not os.path.isdir(os.path.join(folder_name)):
        os.makedirs(os.path.join(folder_name))

def SSIM(img1, img2):
    (ssim, diff) = compare_ssim(img1, img2, full=True)
    if args.debug == "Y":
        print("SSIM: {}".format(ssim))
    return ssim

def ORB(img1, img2):
    res = None
    orb = cv2.ORB_create()

    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)

    matches = sorted(matches, key=lambda x:x.distance)
    res = cv2.drawMatches(img1, kp1, img2, kp2, matches[:30], res, flags=0)

    if args.debug == "Y":
        cv2.imshow('Feature Matching(ORB)', res)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def SIFT(img1, img2):
    res = None
    sift = cv2.xfeatures2d.SIFT_create()

    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    matches = bf.match(des1, des2)

    matches = sorted(matches, key=lambda x:x.distance)
    res = cv2.drawMatches(img1, kp1, img2, kp2, matches[:30], res, flags=0)

    if args.debug == "Y":
        cv2.imshow('Feature Matching(SIFT)', res)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def FLANN_SIFT(img1, img2):
    res = None
    sift = cv2.xfeatures2d.SIFT_create()

    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)


    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    good = []
    for m, n in matches:
        if m.distance < args.factor*n.distance:
            good.append(m)

    res = cv2.drawMatches(img1, kp1, img2, kp2, good, res, flags=0)

    if args.debug == "Y":
        cv2.imshow('Feature Matching(FLANN_SIFT)', res)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def FLANN_ORB(img1, img2):
    res = None
    orb = cv2.ORB_create()

    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    FLANN_INDEX_LSH = 6
    index_params = dict(algorithm=FLANN_INDEX_LSH, table_number=6, key_size=12, multi_prob_level=1)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    good = []
    for m, n in matches:
        if m.distance < args.factor*n.distance:
            good.append(m)

    res = cv2.drawMatches(img1, kp1, img2, kp2, good, res, flags=0)

    if args.debug == "Y":
        cv2.imshow('Feature Matching(FLANN_ORB)', res)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    print(len(good))
    return len(good)

while(video.isOpened()):
    if ret != False:
        count += 1
        aaa = os.path.join("./", "temp", "frame" + str(count) + ".jpg")
        compare_ret, compare_image = video.read()
        grayCompare = cv2.cvtColor(compare_image, cv2.COLOR_BGR2GRAY)

        if args.method == "SSIM":
            score = SSIM(grayOrigin, grayCompare)
            if score <= float(args.tolerance):
                cv2.imwrite(os.path.join(folder_name, "frame" + str(count) + ".jpg"), image)
                if args.debug == "Y":
                    print("The origin is changed to frame " + str(count) + "/" + str(length));
                image = compare_image
                grayOrigin = grayCompare
        elif args.method == "ORB":
            ORB(grayOrigin, grayCompare)
        elif args.method == "SIFT":
            SIFT(grayOrigin, grayCompare)
        elif args.method == "FLANN_SIFT":
            FLANN_SIFT(grayOrigin, grayCompare)
        elif args.method == "FLANN_ORB":
            score = FLANN_ORB(grayOrigin, grayCompare)
            if score <= 10 * args.factor:
                grayOrigin = grayCompare
                if args.debug == "Y":
                    print("The origin is changed to frame " + str(count) + "/" + str(length));
    else:
        break

video.release()

