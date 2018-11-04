#!/usr/bin/env python
# coding: utf-8

# In[2]:


from PIL import Image
import numpy as np
import pickle


# In[5]:


with open('v2_data_batch_6', 'rb') as f:
    temp = pickle.load(f)
    for i in range(0, 9999):
        print(temp[b'labels'][i], ": " + temp[b'names'][i])
    print(temp)
    print(temp[b'labels'])
    print("label size: " + str(len(temp[b'labels'])))
    print(temp[b'data'])
    print(temp[b'data'].shape)
    print("data size: " + str(len(temp[b'data'])))


# In[ ]:




