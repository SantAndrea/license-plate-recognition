from PIL import Image
import pandas as pd
import glob
import os

csvlist = []
for file in glob.glob('/content/OIDv4_ToolKit/OID/Dataset/train/Vehicle registration plate/' + 'Label/*.txt'):
    f = open(file, "r")
    for x in f.readlines():
        split = x.split()
        image = Image.open('/content/OIDv4_ToolKit/OID/Dataset/train/Vehicle registration plate/' + os.path.splitext(os.path.basename(f.name))[0]+'.jpg')
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
txt_df.to_csv('/content/OIDv4_ToolKit/OID/Dataset/train/train_labels.csv', index=None)