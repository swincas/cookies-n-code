from os import walk
from os import listdir, walk
from os.path import isfile, join
from itertools import izip
import fileinput
import csv

from astropy.io import fits
import pyfits
import numpy as np

'''
Simple handy functionalities to manipulate and deal with data
from your python code.

author: Dany Vohl, 2016.
'''

def list_files_with_paths_recursively(my_path):
    """ Recursively list files in my_path and returns the list in the form of ['path/to/file/myfile.extension', '...'] """
    my_files = []
    for (dirpath, dirnames, filenames) in walk(my_path):
        if dirpath[-1] != '/':
            for f in filenames:
                my_files.append(dirpath + '/' + f)
    return my_files

def list_files_in_current_path(path):
    """ Returns files in the current folder only """
    return [ f for f in listdir(path) if isfile(join(path,f)) ]

def find_replace(filename, text_to_search,text_to_replace):
    """ finds text_to_search in filename and replaces it with text_to_replace """
    i = 0
    for line in fileinput.input(filename, inplace=True):
        sys.stdout.write(line.replace(text_to_search, text_to_replace))

def flip_CSV(file):
    """ flips a CSV file within itself (similar to a transpose) """
    a = izip(*csv.reader(open(file, "rb")))
    csv.writer(open(file, "wb")).writerows(a)

def create_cube_from_files_in_current_folder(out_fname):
    """
    Create a cube from fits files in a folder.

    :param out_fname: output filename (should be .fits)
    :return: nothing.
    """

    #TODO: check that all files are in folder are fits; file ordering; image alignment; etc.

    assert ".fits" in out_fname, 'out_fname needs to contain ".fits"\n' \
                                 'Usage example: create_cube_from_files_in_current_folder("filename.fits")'
    files = list_files_in_current_path('.')
    image = fits.open(files[0])
    cube = np.ndarray(shape=(len(files), image[0].data.shape[0], image[0].data.shape[1]), dtype=float)
    i = 0
    for fname in files:
        image = fits.open(fname)
        cube[i] = image[0].data
        i += 1

    header = pyfits.getheader(files[0])
    pyfits.writeto(out_fname, cube, header, clobber=True)