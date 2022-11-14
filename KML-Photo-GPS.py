#Import libraries
from pprint import pprint
from PIL import Image
import piexif
import sys
import simplekml
import os

path = sys.argv[1]
kml = simplekml.Kml()

for dirpath, dirs, files in os.walk(path):
    #folder_name=kml.newfolder(name=dirpath)
    for filename in files:
        fname = os.path.join(dirpath, filename)
        with open(fname) as myfile:
            print(fname)
            try:
                im = Image.open(fname)
                exif_dict = piexif.load(im.info.get('exif'))
                latitud = (exif_dict['GPS'][2][0][0] + exif_dict['GPS'][2][1][0] / 60 + (
                            exif_dict['GPS'][2][2][0] / exif_dict['GPS'][2][2][1]) / 3600) * (
                              -1 if exif_dict['GPS'][1] == b'S' else 1)
                longitud = (exif_dict['GPS'][4][0][0] + exif_dict['GPS'][4][1][0] / 60 + (
                            exif_dict['GPS'][4][2][0] / exif_dict['GPS'][4][2][1]) / 3600) * (
                               -1 if exif_dict['GPS'][3] == b'W' else 1)
                kml.newpoint(name=filename, coords=[(longitud, latitud)])
            except:
                pass
kml.save('Output.kml')
