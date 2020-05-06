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

WIP...
