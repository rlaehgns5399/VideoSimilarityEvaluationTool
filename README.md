# VideoSimilarityEvaluationTool
With OpenCV(Python), let's evaluate video similarity!

# GenBinFile.py
Given folder, it reads all its own folder.
after find images, it starts to convert 32x32 img, RGB Channel.

But this script is unused!

```
just modify PATH in file, and enjoy how to works!
```

you need to install [pickle], [PIL], [numpy]


# GenBinFile2.py
Given folder, it reads all its own folder like [GenBinFile.py].

it makes custom CIFAR-10 data 50000 train data & 10000 valid data.

if you have 60000 data more, don't worry. 

when it makes long LIst, it shuffles List, and cuts exactly at 60000.
```
python GenBinFile2.py
```
modify PATH correctly.

it is made for only 10 classes. but it supports more.
structure is shown below

b'data': R(1,1024), G(1,1024), B(1,1024) with uint 8
b'labels': 0~9 index
b'names': index _ imageName

# LoadBinFile.py
you may have some questions about [GenBinFile2.py] work correctly.

Modify PATH also and enjoy.
```
python LoadBinFile.py
```

it shows " b'labels' b'data' b'names'".


# OpenCV Frame Extractor.py
Modify PATH and file name that you want to extract.

line 30, you should judge frame variable.

# SSIMCalculatorWithOpenCV.py
This is sample OpenCV SSIM caculator.

modify img1,2's path. (you must know that exactly same width, height requires)

and it shows how different they are. (it depends on line 28)

# videoToImage.py

it converts video to image. but it doesnt depend on frame(when you define method SSIM, it will use SSIM with tolerance and extract image).

```
python videoToImage --file aaa.mp4 --method (SSIM, ORB, SIFT, FLANN_SIFT, FLANN_ORB) --debug (Y or N) --tolerance (0.0~1.0) --factor (0.0~1.0)
```

but ORB,SIFT,FLANN_SIFT,FLANN_ORB is implemented. but i didnt make extract code!
