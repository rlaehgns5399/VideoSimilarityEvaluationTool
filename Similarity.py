import argparse
import cv2
import os
import subprocess
parser = argparse.ArgumentParser()
parser.add_argument("-o", type=str, help="video file")
FLAG = parser.parse_args()

threshold = 0.8

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

dic = {}
with open("/home/team4_jjs/DoHun/pretrained/cifarLabel.txt",'r') as f:
    label = f.read().split("\n")
    print(label)
    for line in label:
        dic[line] = 0


data_count = 0
parsing_text = parsing_text[1:]
for a in parsing_text:
    data = a.strip("\n").split("#")
    if float(data[0]) >= threshold:
        dic[data[1]] += 1
    data_count += 1

for list_item in dic:
    print(list_item + ":" + str(dic[list_item]))


value_list = list(dic.values())
value_list.sort(reverse=True)
maxitem = value_list[0]

for list_item in dic:
    if dic[list_item] == maxitem:
        print("this is classified {}, Similarity: {:.04f}".format(list_item, maxitem / data_count))
