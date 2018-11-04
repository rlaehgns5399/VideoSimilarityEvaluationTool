import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--o", help="original video file")
parser.add_argument("--t", help="video file what you want to evaluate")
parser.add_argument("--debug", help="if Y, shows print. otherwise: dont show anything. default: Y", default="Y")
args = parser.parse_args()

