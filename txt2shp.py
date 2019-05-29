"""This script is a successor to corners.py found here:
G:\Lidar\arcGIS_tools\v10

The issue with corners.py is coordinates are converted to doubles format
when creating polygon objects in arcpy causing imprecision issues.

This script uses the shapely and fiona modules which manipulates vector
data and reads/writes geospatial data. ArcGIS is not required.

Requires Python 3.6
"""


from shapely.geometry import mapping, Polygon
import fiona
import csv
import os
from pathlib import Path


def tile_coordinates(text):
    """ group edge coordinates into tuples, returns polygon as a list """
    UL = (text[1]), (text[2])           # Upper Left
    UR = (text[3]), (text[2])           # Upper Right
    LR = (text[3]), (text[4])           # Lower Right
    LL = (text[1]), (text[4])           # Lower Left
    coordinates = (UL, UR, LR, LL)
    return text[0], [tuple(float(x) for x in xs) for xs in coordinates]


path = input('What is the full path of your text file? \n > ')

# In addition to polygon geometry there is one property: tile name
schema = {
    'geometry': 'Polygon',
    'properties': {'NAME': 'str'},
}

# Input text files are delimited by multiple spaces
csv.register_dialect('dialect',
                     delimiter=' ',
                     skipinitialspace=True)


# Create and write to folder in path directory
dir = Path(path).with_suffix('')
if not Path.exists(dir):
    Path.mkdir(dir)
os.chdir(dir)


with fiona.open('Tile_Scheme.shp', 'w', 'ESRI Shapefile', schema) as fout:
    with open(path, 'r') as fin:
        rdr = csv.reader(fin, dialect='dialect')
        for row in rdr:
            parsed_lines = tile_coordinates(row)
            tile = Polygon(parsed_lines[1])
            name = parsed_lines[0]
            fout.write({
                'geometry': mapping(tile),
                'properties': {'NAME': name},
            })
