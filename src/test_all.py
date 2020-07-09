import estrazione
import superres
import rotate_image
import crop_image
import argparse
import os
import glob
import time

parser = argparse.ArgumentParser()
parser.add_argument('--images_path', required = True)
args = parser.parse_args()
imgs_paths = sorted(glob.glob('%s/*.*' % args.images_path))

fp1 = open("tempo.txt","a")
flag = False
print("""                                                                                                                                                                             
FFFFFFFFFFFFFFFFFFFFFFVVVVVVVV           VVVVVVVV   AAA               BBBBBBBBBBBBBBBBB         222222222222222         000000000      222222222222222         000000000     
F::::::::::::::::::::FV::::::V           V::::::V  A:::A              B::::::::::::::::B       2:::::::::::::::22     00:::::::::00   2:::::::::::::::22     00:::::::::00   
F::::::::::::::::::::FV::::::V           V::::::V A:::::A             B::::::BBBBBB:::::B      2::::::222222:::::2  00:::::::::::::00 2::::::222222:::::2  00:::::::::::::00 
FF::::::FFFFFFFFF::::FV::::::V           V::::::VA:::::::A            BB:::::B     B:::::B     2222222     2:::::2 0:::::::000:::::::02222222     2:::::2 0:::::::000:::::::0
  F:::::F       FFFFFF V:::::V           V:::::VA:::::::::A             B::::B     B:::::B                 2:::::2 0::::::0   0::::::0            2:::::2 0::::::0   0::::::0
  F:::::F               V:::::V         V:::::VA:::::A:::::A            B::::B     B:::::B                 2:::::2 0:::::0     0:::::0            2:::::2 0:::::0     0:::::0
  F::::::FFFFFFFFFF      V:::::V       V:::::VA:::::A A:::::A           B::::BBBBBB:::::B               2222::::2  0:::::0     0:::::0         2222::::2  0:::::0     0:::::0
  F:::::::::::::::F       V:::::V     V:::::VA:::::A   A:::::A          B:::::::::::::BB           22222::::::22   0:::::0 000 0:::::0    22222::::::22   0:::::0 000 0:::::0
  F:::::::::::::::F        V:::::V   V:::::VA:::::A     A:::::A         B::::BBBBBB:::::B        22::::::::222     0:::::0 000 0:::::0  22::::::::222     0:::::0 000 0:::::0
  F::::::FFFFFFFFFF         V:::::V V:::::VA:::::AAAAAAAAA:::::A        B::::B     B:::::B      2:::::22222        0:::::0     0:::::0 2:::::22222        0:::::0     0:::::0
  F:::::F                    V:::::V:::::VA:::::::::::::::::::::A       B::::B     B:::::B     2:::::2             0:::::0     0:::::02:::::2             0:::::0     0:::::0
  F:::::F                     V:::::::::VA:::::AAAAAAAAAAAAA:::::A      B::::B     B:::::B     2:::::2             0::::::0   0::::::02:::::2             0::::::0   0::::::0
FF:::::::FF                    V:::::::VA:::::A             A:::::A   BB:::::BBBBBB::::::B     2:::::2       2222220:::::::000:::::::02:::::2       2222220:::::::000:::::::0
F::::::::FF                     V:::::VA:::::A               A:::::A  B:::::::::::::::::B      2::::::2222222:::::2 00:::::::::::::00 2::::::2222222:::::2 00:::::::::::::00 
F::::::::FF                      V:::VA:::::A                 A:::::A B::::::::::::::::B       2::::::::::::::::::2   00:::::::::00   2::::::::::::::::::2   00:::::::::00   
FFFFFFFFFFF                       VVVAAAAAAA                   AAAAAAABBBBBBBBBBBBBBBBB        22222222222222222222     000000000     22222222222222222222     000000000     
                                                                                                                                                                             
                                                                                                                                                                             
                                                                                                                                                                             
                                                                                                                                                                             
                                                                                                                                                                             
                                                                                                                                                                             
                                                                                                                                                                            """)
for _,img_path in enumerate(imgs_paths):

  if img_path.endswith(('.jpg','.jpeg','.png')):

    print("Elaborazione di: {}".format(args.image_path))
    start = time.time()

    files = glob.glob('superres/*')
    for f in files:
        os.remove(f)

    files = glob.glob('ROI/*')
    for f in files:
        os.remove(f)

    files = glob.glob('ocr/rotated/*')
    for f in files:
        os.remove(f)

    try:
      estrazione.run(img_path)
      print("Estrazione completata")
      superres.run()
      print("Super-Resolution completato")
      rotate_image.run()
      print("Rotazione immagine completata")
      crop_image.run()
      print("Ritaglio immagine completato")
      os.chdir('ocr')
      os.system('python license-plate-ocr.py')
    except:
      fp2 = open("targhe.txt","a")
      fp2.write("\n")
      fp2.close()
    os.chdir('..')

    end = time.time()
    finalTime = end - start
    fp1.write(str(finalTime) + "\n")

file1.close()
