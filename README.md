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
