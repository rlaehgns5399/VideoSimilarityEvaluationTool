#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import PIL
from PIL import Image
import numpy as np
import pickle


# In[4]:


input_dir = "C:/tensorflow_workspace/dataset/"
output_file = os.getcwd() + "/OpenCV_Video/dataset/data.bin"
directories = os.listdir(input_dir)

print(os.getcwd() + "/OpenCV_Video/dataset/data.bin")
print(directories)


# In[21]:


index = -1
index2 = 0
file_counter = 1
restart = False
#output = open(output_file, "ab")
for folder in directories:
    print(folder)

    folder2 = os.listdir(input_dir + folder)
    index += 1
    total_data
    for image in folder2:
        index2 += 1
        im = Image.open(input_dir+folder+"/"+image) #Opening image
        print(folder + "/" + image + " index: [" + str(index) + "]")
        im = im.resize((32, 32), PIL.Image.ANTIALIAS)
        im = (np.array(im)) #Converting to numpy array

        r = im[:,:,0].flatten() #Slicing to get R data
        g = im[:,:,1].flatten() #Slicing to get G data
        b = im[:,:,2].flatten() #Slicing to get B data
        #label = [index]
        
        if index2 == 1 or restart == True:
            total_data = np.array(list(r) + list(g) + list(b), np.uint8)
            total_data = total_data.reshape(1, 3072)
            label = [index]
            restart = False
        else :
            out = np.array(list(r) + list(g) + list(b), np.uint8)
            out = out.reshape(1, 3072)
            label.append(index)
            total_data = np.vstack([total_data, out])
        
        if index2 % 10000 == 0:
            data = {
                b'data': total_data,
                b'label': label
            }
            with open('data_batch_' + str(file_counter), 'wb') as f:
                pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
                file_counter += 1
                restart = True
        print(total_data.shape)
#        output.write(out.tobytes())

#output.close()


# In[ ]:




