from PIL import Image
import pandas as pd
import glob
import os
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--path", help="Percorso di input. Es: 'root/train/'")
args = parser.parse_args()
PATH = args.path

csvlist = []
for file in glob.glob(PATH + 'Label/*.txt'):
    f = open(file, "r")
    for x in f.readlines():
        split = x.split()
        image = Image.open(PATH + os.path.splitext(os.path.basename(f.name))[0]+'.jpg')
        value = (os.path.splitext(os.path.basename(f.name))[0]+'.jpg',
                  int(image.size[0]),
                  int(image.size[1]),
                  "licenseplate",
                  round(float(split[3]),2),
                  round(float(split[4]),2),
                  round(float(split[5]),2),
                  round(float(split[6]),2)
                  )
        csvlist.append(value)
column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
txt_df = pd.DataFrame(csvlist, columns=column_name)
txt_df.to_csv(PATH + 'train_labels.csv', index=None)
