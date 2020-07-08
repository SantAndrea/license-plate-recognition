import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

import zipfile
import cv2

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
from utils import label_map_util
from utils import visualization_utils as vis_util


MODEL_NAME = '/content/drive/My Drive/ALPR/tensorflow/models/research/object_detection/targa_graph'

# Path di frozen detection graph del modello attualmente utilizzato
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

# Lista delle stringhe usate per i label
PATH_TO_LABELS = os.path.join('/content/drive/My Drive/ALPR/tensorflow/models/research/object_detection/training', 'object-detection.pbtxt')

# Numero di classi da identificare
NUM_CLASSES = 1
  
sys.path.append("..") 
  

def run(path):
  	
	# Percorso immagini da cui estrarre gli oggetti 
	PATH_TO_IMAGE = os.path.join(path) 
	# Percorso salvataggio oggetti estratti
	SUPERRES_PATH = os.path.join("superres/") 
	# Carico la label map. 
	label_map = label_map_util.load_labelmap(PATH_TO_LABELS) 
	categories = label_map_util.convert_label_map_to_categories( 
		label_map, max_num_classes = NUM_CLASSES, use_display_name = True) 
	category_index = label_map_util.create_category_index(categories) 
	  
	# Caricamento modello di TensorFlow 
	detection_graph = tf.Graph() 
	with detection_graph.as_default(): 
	    od_graph_def = tf.GraphDef() 
	    with tf.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid: 
	        serialized_graph = fid.read() 
	        od_graph_def.ParseFromString(serialized_graph) 
	        tf.import_graph_def(od_graph_def, name ='') 
	  
	    sess = tf.Session(graph = detection_graph) 
	  
	# Considero i tensori di input e di output 
	  
	# Il tensore di input, l'immagine 
	image_tensor = detection_graph.get_tensor_by_name('image_tensor:0') 
	  
	# Tensori di output: box, punteggi di confidenza e classi degli oggetti
	# I box rappresentano l'area dell'immagine in cui si trova un oggetto riconosciuto
	detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0') 
	detection_scores = detection_graph.get_tensor_by_name('detection_scores:0') 
	detection_classes = detection_graph.get_tensor_by_name('detection_classes:0') 
	  
	# Numero degli oggetti riconosciuti
	num_detections = detection_graph.get_tensor_by_name('num_detections:0') 
	  
	# Carica l'immagine con OpenCV ed espande le dimensioni formando un array da una singola colonna in cui ogni elemento contiene i valori RGB dei vari pixel
	image = cv2.imread(PATH_TO_IMAGE) 
	image_expanded = np.expand_dims(image, axis = 0) 
	  
	# Esegui il riconoscimento
	(boxes, scores, classes, num) = sess.run( 
	    [detection_boxes, detection_scores, detection_classes, num_detections], 
	    feed_dict ={image_tensor: image_expanded}) 
	  
	# Visualizza il risultato del riconoscimento 
	  
	vis_util.visualize_boxes_and_labels_on_image_array( 
	    image, 
	    np.squeeze(boxes), 
	    np.squeeze(classes).astype(np.int32), 
	    np.squeeze(scores), 
	    category_index, 
	    use_normalized_coordinates = True, 
	    line_thickness = 1, 
	    min_score_thresh = 0.20) 

	coordinates = vis_util.return_coordinates(
		image,
		np.squeeze(boxes),
		np.squeeze(classes).astype(np.int32),
		np.squeeze(scores),
		category_index,
		use_normalized_coordinates=True,
		line_thickness=8,
		min_score_thresh=0.20)

	if not coordinates:
		raise Exception("Nessuna targa rilevata")

	i = 0
	# Per ogni gruppo di coordinate, salva la porzione di immagine corrispondente
	for coordinate in coordinates:
		crop_img = image[coordinate[0]+1:coordinate[1], coordinate[2]+1:coordinate[3]]
		try:
		  i += 1
		  cv2.imwrite(SUPERRES_PATH + str(i)+'.jpg', crop_img)
		except:
		  continue

	raise Exception("Errore nel salvataggio degli oggetti estratti") if i=0