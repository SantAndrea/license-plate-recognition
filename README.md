# License Plate Recognition

Il sistema proposto consiste in due componenti per l'individuazione e la lettura delle targhe.

## Impostare il progetto

Queste istruzioni guidano nell'installazione del progetto su una macchina, a scopo di training e/o testing.

### Prerequisiti

- tensorflow 1.14
- tensorflow-gpu 1.14 (opzionale)
- tensorflow-object_detection_api
- ISR

Da ora in avanti chiameremo <i>root</i> la directory principale del progetto.

Clonare la repository tensorflow/models e seguire le istruzioni che si trovano alla pagina https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md (saltare il passaggio COCO API installation).

In caso di problemi con le librerie ```slim```, occorre compilarle.
```
Da root/models/research/slim

python setup.py build
python setup.py install
```

Clonare queste repository nella directory ```models/research/object_detection```.
```
git clone https://github.com/SantAndrea/license-plate-recognition.git
git clone https://github.com/idealo/image-super-resolution.git
git clone https://github.com/pjreddie/darknet.git
```

Spostare il contenuto della cartella ```src``` e i file situati a URL di questa repository in ```models/research/object_detection```.

È possibile anche eliminare la cartella model e tutto il suo contenuto, ad eccezione di ```models/research/object_detection``` e di ```models/research/slim```.

Spostare la cartella ```darknet``` in ```object_detection/ocr```. Dopodiché, aprirla e digitare il comando ```make``` per compilare Darknet.

In ```object_detection``` creare due cartelle, necessarie al funzionamento del programma: ```superres``` e ```ROI```

## Training

Per il training è stato usato il tool <b>OIDv4 Toolkit</b> per recuperare le immagini da dare in input alla rete durante l'addestramento.

Da <i>root</i> digitare i seguenti comandi:
```
git clone https://github.com/EscVM/OIDv4_ToolKit.git
```
e, successivamente, entrando nella cartella appena creata, digitare il comando:
```
pip install -r requirements.txt
```

Per scaricare le immagini digitare il seguente comando:
```
python main.py downloader --classes 'Vehicle Registration Plate' --type_csv train --limit 2000
```
Il programma chiederà anche di scaricare dei file aggiuntivi. Ripetere la stessa operazione per i file di test:
```
python main.py downloader --classes 'Vehicle Registration Plate' --type_csv test --limit 400
```
La struttura finale delle cartelle dopo il download dovrebbe somigliare a questa:
```
OIDv4_ToolKit
│    main.py
│    ...
└─── OID
    │
    └─── csv_folder
    │   │
    │   └─── class-descriptions-boxable.csv
    │   │
    │   └─── test-annotations-bbox.csv
    │   │
    │   └─── train-annotations-bbox.csv
    └─── OID
        │
        └─── Dataset
            │
            └─── train
            |   │
            |   └─── Vehicle Registration Plate
            └─── test
                |
                └─── Vehicle Registration Plate
```
Nelle cartelle presenti in train e in test sono presenti le immagini scaricate e una cartella <b>Label</b>, contenente un file <i>.txt</i> per ciacuna immagine. Ogni file indica le coordinate di uno o più <i>bounding box</i> all'interno della foto. Per esempio:
```
Vehicle registration plate 624.0 609.920256 691.84 624.639744
```
Tuttavia, per procedere con l'allenamento con l'API, abbiamo bisogno di ricavarci dei file <i>.record</i> da poter fornire alla funzione di train, uno per il training set e uno per il test set. Prima di convertire i label nel formato record di TF abbiamo bisogno di raggrupparli in un CSV nel formato Pascal VOC. Ne verranno creati due separati tramite lo script <b>OpenImagesTXT_to_TensorFlow_CSV.py</b>.
```
Da root

python license-plate-recognition/src/OpenImagesTXT_to_TensorFlow_CSV.py --path='OIDv4_ToolKit/OID/OID/Dataset/train/Vehicle Registration Plate/'
python license-plate-recognition/src/OpenImagesTXT_to_TensorFlow_CSV.py --path='OIDv4_ToolKit/OID/OID/Dataset/test/Vehicle Registration Plate/'
```
Eseguiti i due comandi ci saranno due file CSV nelle cartelle Label in train e in test.
```
OIDv4_ToolKit
│    main.py
│    ...
└─── OID
    │
    └─── csv_folder
    │   │
    │   └─── class-descriptions-boxable.csv
    │   │
    │   └─── test-annotations-bbox.csv
    │   │
    │   └─── train-annotations-bbox.csv
    └─── OID
        │
        └─── Dataset
            │
            └─── train
            |   │
            |   └─── Vehicle Registration Plate
            |       └─── Label
            |           └─── train_labels.csv
            └─── test
                |
                └─── Vehicle Registration Plate
                    └─── Label
                        └─── test_labels.csv
```

I file .csv appena creati saranno necessari al generatore di TFrecord. È necessario quindi lanciare lo script <i>object_detection/generate_tfrecord.py</i> per ognuno dei file.
Esempio:
```
python3 generate_tfrecord.py --csv_input=data/train_labels.csv  --output_path=data/train.record
```

Una volta creati i file si può iniziare ad addestrare un modello. Il modello originariamente scelto è stato <b>ssd_mobilenet_v1_coco_2018_01_28</b>, incluso in questa repository.
Esempio:
```
python3 object_detection/legacy/train.py --logtostderr --train_dir=../targa_graph --pipeline_config_path=object_detection/training/ssd_mobilenet_v1_pets.config
```
Il modello addestrato verrà salvato in ```train_dir```

Come ultima cosa, è necessario esportare un grafo inferito dal modello addestrato tramite il seguente comando (di esempio):
```
python3 object_detection/export_inference_graph.py --input_type=image_tensor --pipeline_config_path=object_detection/training/ssd_mobilenet_v1_pets.config --trained_checkpoint_prefix=object_detection/targa_graph/model.ckpt --output_directory=path/to/exported_model_directory
```

## Testing
