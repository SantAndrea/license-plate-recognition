# License Plate Recognition

Il sistema proposto consiste in due componenti per l'individuazione e la lettura delle targhe.

## Impostare il progetto

Queste istruzioni guidano nell'installazione del progetto su una macchina, a scopo di training e/o testing.

### Prerequisiti

- tensorflow 1.14
- tensorflow-gpu 1.14 (opzionale)
- tensorflow-object_detection_api

Clonare la repository tensorflow/models nella directory del progetto, che chiameremo ```<root>```, e seguire le istruzioni che si trovano alla pagina https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md (saltare il passaggio COCO API installation).

In caso di problemi con le librerie ```slim```, occorre compilarle.
```
Da root/models/research/slim

python setup.py build
python setup.py install
```

### Training

Per il training è stato usato il tool <b>OIDv4 Toolkit</b> per recuperare le immagini da dare in input alla rete durante l'addestramento.

Da <i>root</i> digitare i seguenti comandi:
```
git clone https://github.com/EscVM/OIDv4_ToolKit.git
```
e, successivamente, entrando nella cartella appena creata, digitare
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
Nelle cartelle in train e in test sono presenti le immagini scaricate e una cartella <b>Label</b>, contenente un file <i>.txt</i> per ciacuna immagine. Ogni file indica le coordinate di uno o più <i>bounding box</i> all'interno della foto. Per esempio:
```
Vehicle registration plate 624.0 609.920256 691.84 624.639744
```
Tuttavia, per procedere con l'allenamento con l'API, abbiamo bisogno di ricavarci dei file <i>.record</i> da poter fornire alla funzione di train, uno per il training set e uno per il test set. Prima di convertire i label nel formato record di TF abbiamo bisogno di raggrupparli in un CSV nel formato Pascal VOC. Ne verranno creati due separati tramite lo script <b>OpenImagesTXT_to_TensorFlow_CSV.py</b>
