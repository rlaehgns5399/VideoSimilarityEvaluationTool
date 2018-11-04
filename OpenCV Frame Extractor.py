#!/usr/bin/env python
# coding: utf-8

# In[11]:


import cv2
import os
 

input_dir = "C:/tensorflow_workspace/OpenCV_Video/"
output_file = "C:/tensorflow_workspace/dataset/"
# 영상의 의미지를 연속적으로 캡쳐할 수 있게 하는 class
directory = os.listdir(input_dir)

for vid in directory:
    if vid == "accident.mp4":
        vidcap = cv2.VideoCapture(input_dir + vid)
        os.makedirs(os.path.join(output_file + vid))
        count = 0
        ratio = 0
        while(vidcap.isOpened()):
            # read()는 grab()와 retrieve() 두 함수를 한 함수로 불러옴
            # 두 함수를 동시에 불러오는 이유는 프레임이 존재하지 않을 때
            # grab() 함수를 이용하여 return false 혹은 NULL 값을 넘겨 주기 때문
            ret, image = vidcap.read()
            if ret == False:
                break
            # 캡쳐된 이미지를 저장하는 함수 
            if ratio % 3 == 0:
                cv2.imwrite(output_file + vid + "/frame%d.jpg" % count, image)
                count += 1
                print('Saved frame%d.jpg' % count)
            ratio += 1
        vidcap.release()
print('done~')


# In[ ]:




