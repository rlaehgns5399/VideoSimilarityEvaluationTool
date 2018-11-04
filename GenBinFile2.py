#!/usr/bin/env python
# coding: utf-8

# In[11]:


import os
import PIL
from PIL import Image
import numpy as np
import pickle
from random import shuffle
import time


# In[12]:


input_dir = "C:/tensorflow_workspace/dataset/"
output_file = os.getcwd() + "/OpenCV_Video/dataset/data.bin"
directories = os.listdir(input_dir)

print(os.getcwd() + "/OpenCV_Video/dataset/data.bin")
print(directories)


# In[14]:


index = -1
index2 = 0
file_counter = 0
restart = False

combine_list = []
startt = time.time()
for folder in directories:
    
    folder2 = os.listdir(input_dir + folder)
    index += 1
    print(folder, "index:", index)
    for image in folder2:
        index2 += 1
        im = Image.open(input_dir+folder+"/"+image) #Opening image
        # print(folder + "/" + image + " index: [" + str(index) + "]")
        im = im.resize((32, 32), PIL.Image.ANTIALIAS)
        im = (np.array(im)) #Converting to numpy array

        r = im[:,:,0].flatten() #Slicing to get R data
        g = im[:,:,1].flatten() #Slicing to get G data
        b = im[:,:,2].flatten() #Slicing to get B data
        
        out = np.array(list(r) + list(g) + list(b), np.uint8)
        out = out.reshape(1, 3072)
        combine_list.append([[index], out, str(index) + "_" + str(image)])
        if file_counter % 1000 == 0:
            print(file_counter)
            print(time.time() - startt, "sec")
        file_counter += 1

print("*" * 20)
print("added all data: " + str(file_counter))
print("actual length: " + str(len(combine_list)))
print("*" * 20)
shuffle(combine_list)
print("shuffled")

startt = time.time()
data_counter = 0
final_label = []
final_data = None
final_img_name = []
for item in combine_list:
    # 10000개 데이터 축적, 60000번까지 반복
    if data_counter % 10000 != 0 and data_counter % 50000 != 0:
        final_label.append(item[0][0])
        final_img_name.append(item[2])
        if final_data is None:
            final_data = item[1]
        else :
            final_data = np.vstack([final_data, item[1]])
            
    # 10000개 데이터가 축적되었으면 저장
    elif data_counter % 10000 == 0 and data_counter != 0:
        final_data = np.vstack([final_data, item[1]])
        final_label.append(item[0][0])
        final_img_name.append(item[2])
        data = {
            b'data': final_data,
            b'labels': final_label,
            b'names': final_img_name
        }
        with open('v2_data_batch_' + str(data_counter // 10000), 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
            final_data = None
            final_label = []
            final_img_name = []
    # 60000번째 데이터면 종료
    if data_counter % 1000 == 0:
        if final_data is None:
            print("(0, 3092)")
        else: 
            print(final_data.shape)
    if data_counter == 60000:
        break
    data_counter += 1
print(time.time() - startt)
#         print(combine_list)
#         print(len(combine_list))


# In[ ]:




