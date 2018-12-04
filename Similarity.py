import argparse
import cv2
import os

parser = argparse.ArgumentParser()
parser.add_argument("--o", type=str, help="original video file")
parser.add_argument("--t", type=str, help="video file what you want to evaluate")
FLAG = parser.parse_args()

