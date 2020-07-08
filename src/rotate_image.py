import numpy as np
import cv2
import math
from scipy import ndimage
import os
from glob import glob

def run():

	"""
	Questa funzione calcola il grado di rotazione di un'immagine e la raddrizza
	"""

	# Percorso immagini originali
	CWD_PATH = 'ROI/'
	# Percorso di salvataggio
	ROTATED_PATH = 'ocr/rotated'
	PATH_TO_ROTATED = os.path.join(ROTATED_PATH) 

	imgs_paths = sorted(glob('%s/*.jpg' % CWD_PATH))
	if not img_paths:
		raise Exception("Nessuna immagine da controllare per la rotazione")
	i = 0
	# Itero le immagini
	for j,img_path in enumerate(imgs_paths):

		img_before = cv2.imread(img_path)
		# Calcolo l'aspect ratio
		w = img_before.shape[1]
		h = img_before.shape[0]
		aspect_ratio = w/h
		# Converto in scala di grigi, rilevo i contorni e applica la trasformata di Hough
		img_gray = cv2.cvtColor(img_before, cv2.COLOR_BGR2GRAY)
		img_edges = cv2.Canny(img_gray, 100, 100, apertureSize=3)
		lines = cv2.HoughLinesP(img_edges, 1, np.pi/180, 30, minLineLength = 60, maxLineGap=300)

		#Calcolo l'angolo di rotazione
		angles = []
		if lines is not None:
				for x1, y1, x2, y2 in lines[0]:
						angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
						angles.append(angle)

		median_angle = np.median(angles)
		# Se l'angolo è compreso tra determinati valori, ruoto l'immagine
		rotate = False
		if (median_angle < 40 and median_angle > 5) or (median_angle > -40 and median_angle < -5):
		    img_rotated = ndimage.rotate(img_before, median_angle)
			rotate = True
		else:
		    img_rotated = img_before

		print ("Angle is {}".format(median_angle))

		# Se l'immagine è stata ruotata riducine l'altezza in eccesso
		if rotate:
		    width = img_before.shape[1]
		    height = img_before.shape[0]
		    height_rotated = img_rotated.shape[0]
		    width_rotated = img_rotated.shape[1]
		    height_new = height_rotated - height
		    height_crop = int(height_new/2)
		    aspect_ratio = width/height
		    print(width, height, height_rotated, height_new, height_crop)
		    crop_img1 = img_rotated[int(height_crop):int(height_rotated - (height_crop)), 20:width]
		    cv2.imwrite(PATH_TO_ROTATED + '/rotated' + str(i) + '.jpg', crop_img1)
		else:
		    cv2.imwrite(PATH_TO_ROTATED + '/rotated' + str(i) + '.jpg', img_before)
		i += 1
