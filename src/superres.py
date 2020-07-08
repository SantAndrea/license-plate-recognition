import os


def run():

	"""
	Funzione per effettuare il super resolution. Prende in input le immagini presenti nella cartella 'superres'
	e salva il risultato nella cartella ROI
	"""

	# Percorso delle immagini originali
	CWD_PATH = 'superres/'
	# Percorso di salvataggio
	ROI_PATH = 'ROI'
	PATH_TO_ROI = os.path.join(ROI_PATH) 

	import numpy as np
	from PIL import Image
	import cv2
	from glob import glob

	# Itero i file nella cartella
	imgs_paths = sorted(glob('%s/*.jpg' % CWD_PATH))
	if not img_paths:
		raise Exception("Nessuna immagine da scalare")
	i = 0
	for j,img_path in enumerate(imgs_paths):

		img = Image.open(img_path)
		lr_img = np.array(img)

		# Carica il modello Residual Dense Network
		from ISR.models import RDN
		rdn = RDN(weights='psnr-large')

		# Applica due volte il super resolution
		sr_img = rdn.predict(lr_img)
		sr_img = rdn.predict(sr_img)

		# Sfocatura superficie e conversione in scala di grigi
		sr_img2 = cv2.bilateralFilter(sr_img, 50, 10, 10)
		sr_img2 = cv2.cvtColor(sr_img2, cv2.COLOR_RGB2GRAY)

		cv2.imwrite(PATH_TO_ROI + '/filtered_' + str(i) + '.jpg', sr_img2)
		i += 1

