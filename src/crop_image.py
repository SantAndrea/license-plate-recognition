import numpy as np
from PIL import Image
import cv2
import os
from glob import glob

def run():
	# Persorso delle immagini originali
	ROTATED_PATH = 'ocr/rotated'
	# Percorso immagini ritagliate
	PATH_TO_ROTATED = os.path.join(ROTATED_PATH) 


	imgs_paths = sorted(glob('%s/*.jpg' % PATH_TO_ROTATED))

	if not img_paths:
		raise Exception("Nessuna immagine da controllare per il ritaglio")
	i = 0
	# Itera i file
	for j,img_path in enumerate(imgs_paths):

		img = cv2.imread(img_path)

		height = img.shape[0]
		width = img.shape[1]

		aspect_ratio = width/height

		# Se l'aspect ratio è inferiore a 1.5, ritaglia l'immagine
		if aspect_ratio < 1.5:
		    crop_img1 = img[0:int(height/2), 0:width]
		    crop_img2 = img[int(height/2):height, 0:width]
		    cv2.imwrite(PATH_TO_ROTATED + '/crop1_' + str(i) + '.jpg', crop_img1)
		    cv2.imwrite(PATH_TO_ROTATED + '/crop2_' + str(i) + '.jpg', crop_img2)
		    os.remove(img_path)
		i += 1
