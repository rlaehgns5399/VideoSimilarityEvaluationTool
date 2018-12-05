import argparse
import cv2
import os
import subprocess
parser = argparse.ArgumentParser()
parser.add_argument("-o", type=str, help="video file")
FLAG = parser.parse_args()

dir = "./video"
if not os.path.isdir(dir):
    os.mkdir(dir)

vid = cv2.VideoCapture(FLAG.o)
i = 0
while(vid.isOpened()):
    ret, image = vid.read()
    if not ret:
        break
    image = cv2.resize(image, (32, 32))
    cv2.imwrite(dir + "/frame%d.jpg" % i, image)
    i += 1

inception_cifar = "inception_cifar.py"
result = subprocess.check_output("python " + inception_cifar + " --load 99 --predict --im_name .jpg", shell=True)
parsing_text = result.decode('utf8').split("===============================")

for a in parsing_text:
    print(a.strip("\n"))