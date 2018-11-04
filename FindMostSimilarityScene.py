import argparse
import cv2
from skimage.measure import compare_ssim

parser = argparse.ArgumentParser()
parser.add_argument("--o", help="original video file")
parser.add_argument("--t", help="video file what you want to evaluate")
parser.add_argument("--debug", help="if Y, shows print. otherwise: dont show anything. default: Y", default="Y")
FLAG = parser.parse_args()

origin_video = cv2.VideoCapture(FLAG.o)
eval_video = cv2.VideoCapture(FLAG.t)

frame = 0
max_ssim = 0
saved_frame = 0

# 첫번째 이미지만 가지고 시작점 찾음
if eval_video.isOpened():
    _, eval_video_image = eval_video.read()
    eval_video_image = cv2.cvtColor(eval_video_image, cv2.COLOR_BGR2GRAY)

while origin_video.isOpened():
    # 비교 이미지 읽고 흑백으로 바꿈
    origin_status, origin_video_image = origin_video.read()
    origin_video_image = cv2.cvtColor(origin_video_image, cv2.COLOR_BGR2GRAY)

    # 동영상 다읽었으면, 종료
    if not origin_status:
        break

    # SSIM 계산
    (ssim, diff) = compare_ssim(origin_video_image, eval_video_image, full=True)

    # SSIM 최대값을 갖는 frame index를 저장
    if ssim > max_ssim:
        max_ssim = ssim
        saved_frame = frame

    frame += 1

if FLAG.debug == "Y":
    print("MAX_SSIM:", max_ssim, "at frame:", saved_frame)

origin_video.release()
eval_video.release()