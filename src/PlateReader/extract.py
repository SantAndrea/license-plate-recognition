import os
import cv2
from PIL import Image
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument("--i", help="Immagine di input")
args = parser.parse_args()
PATH = args.i

image = Image.open(PATH)
array_img =  cv2.imread(PATH)

xmin = 0
ymin = 0
xmax = 0
ymax = 0
i = 0

f = open(os.path.splitext(os.path.basename(image.filename))[0]+'.txt')
for x in f.readlines():
    i+=1
    split = x.split()
    xmin = int(float(split[3]))
    ymin = int(float(split[4]))
    xmax = int(float(split[5]))
    ymax = int(float(split[6]))
    crop_img = array_img[ymin:ymax, xmin:xmax]
    cv2.imshow('extracted {}'.format(i), crop_img)

cv2.waitKey(0)