import argparse
import cv2
import time
from skimage.measure import compare_ssim

parser = argparse.ArgumentParser()
parser.add_argument("--o", help="original video file")
parser.add_argument("--t", help="video file what you want to evaluate")
parser.add_argument("--method", help="how to compare? SSIM, ORB, SIFT, FLANN_SIFT, FLANN_ORB, default=SSIM", default="SSIM")
parser.add_argument("--debug", help="if Y, shows print. otherwise: dont show anything. default: Y", default="Y")
parser.add_argument("--resize", help="each image is converted to 32x32", default="N")
FLAG = parser.parse_args()

origin_video = cv2.VideoCapture(FLAG.o)
eval_video = cv2.VideoCapture(FLAG.t)

frame = 0
max_ssim = 0
saved_frame = 0
origin_length = 0

start_time = time.time()
if origin_video.isOpened():
    if FLAG.debug == "Y":
        origin_length = int(origin_video.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(origin_video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(origin_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = origin_video.get(cv2.CAP_PROP_FPS)
        print("="*30);
        print("Filename: ", FLAG.o)
        print("Video size: " + str(width) + "x" + str(height))
        print("frame size: ", origin_length)
        print("fps: ", fps)
        print("method: ", FLAG.method)
        print("resize: ", FLAG.resize)

# 첫번째 이미지만 가지고 시작점 찾음
if eval_video.isOpened():
    _, eval_video_image = eval_video.read()
    eval_video_image = cv2.cvtColor(eval_video_image, cv2.COLOR_BGR2GRAY)
    if FLAG.resize == "Y":
        eval_video_image = cv2.resize(eval_video_image, (32, 32))

    if FLAG.debug == "Y":
        print("="*30);
        length = int(eval_video.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(eval_video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(eval_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = eval_video.get(cv2.CAP_PROP_FPS)
        print("Filename: ", FLAG.t)
        print("Video size: " + str(width) + "x" + str(height))
        print("frame size: ", length)
        print("fps: ", fps)
        print("method: ", FLAG.method)
        print("resize: ", FLAG.resize)

while origin_video.isOpened():
    # 비교 이미지 읽고 흑백으로 바꿈

    origin_status, origin_video_image = origin_video.read()
    # 동영상 다읽었으면, 종료
    if origin_status == False:
        break

    origin_video_image = cv2.cvtColor(origin_video_image, cv2.COLOR_BGR2GRAY)
    if FLAG.resize == "Y":
        origin_video_image = cv2.resize(origin_video_image, (32, 32))
    # SSIM 계산
    if FLAG.method == "SSIM":
        (ssim, diff) = compare_ssim(origin_video_image, eval_video_image, full=True)

        # SSIM 최대값을 갖는 frame index를 저장
        if ssim > max_ssim:
            max_ssim = ssim
            saved_frame = frame

    frame += 1
    if frame % 1000 == 0:
        print(str(frame) + "/" + str(origin_length), time.time() - start_time, "secs")
if FLAG.debug == "Y":
    print("MAX_SSIM:", max_ssim, "at frame:", saved_frame)
    print("Elapsed Time:", time.time() - start_time)
origin_video.release()
eval_video.release()