# -*- coding: utf-8 -*-

'''
Read in the image from the .img file format where there is a seperate .hdr
file that outlines the contents of the .img file. This reader's principle task
is to take these two files and import only the wavelengths that we need, these
are defined in /Resources/bands.txt. Bands and wavelength are interchanged
frequently in this file, sorry.
'''

import os

import spectral.io.envi as envi
import numpy as numpy

if __package__ is '':

    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    
    from crismimage import CRISMImage

else:
    from classifiers.crismimage import CRISMImage

class ImageReader:

    #root folder of the project
    parent_directory = os.path.join(os.path.dirname(__file__), '..')

    #where the specific bands we plan to use is defined
    bands_file_path = os.path.join(parent_directory, 'Resources', 'bands.txt')

    #head to the images directory
    image_dir = os.path.join(parent_directory, 'Images')

    def __init__(self, imageFile):
        self.image_file = imageFile

        if(len(self.image_file) > 0):
            self.header_bands = self.get_header_wavelengths()
            self.specific_bands = self.get_bands_file()
            self.ignore_value = self.get_header_data_ignore_value()
            self.default_bands = self.get_default_bands()
        else:
            self.header_bands = None
            self.specific_bands = None
            self.ignore_value = None
            self.default_bands = None

    '''
        Get the default bands from the header files.
    '''
    def get_default_bands(self):

        #the string path of the image
        full_path = os.path.join(self.image_dir, self.image_file)

        #open the image reading in its header then the .img file
        image_file = envi.open(full_path + ".hdr", full_path)

        default_bands = image_file.metadata['default bands']

        #cast all the bands to ints
        for i in range(len(default_bands)):

            default_bands[i] = int(default_bands[i])

        return default_bands

    '''
        Update the image and recalculate all the required values.

        Params:
            str, new_dir: the full parent path
            str, image_file: the name of the image file
    '''
    def update_image(self, new_dir, image_file):

        self.image_file = image_file
        self.image_dir = new_dir
        self.header_bands = self.get_header_wavelengths()
        self.specific_bands = self.get_bands_file()
        self.ignore_value = self.get_header_data_ignore_value()
        self.default_bands = self.get_default_bands()

    '''
    Match the bands that came from the bands.txt file to the bands from the
    header file. Make an array of the int indices of the bands in header_bands.
    We do this because the read_bands method expects an array of ints that are
    the indices of the bands from the original file

    Params: none
    Return: int[]: the indices in header_bands of the values that matches
               a value from the specific bands
    '''
    def match_bands(self):

        matched_bands = []

        #run over the list of the bands from the header file to find the indices
        #of matches
        for i in range(len(self.specific_bands)):
            #j will never been less than i but it can be equal so save some time
            j = i
            #scroll through the header_bands till a match is found
            while(self.specific_bands[i] != self.header_bands[j]):
                j += 1
            #at this point j should be a match
            matched_bands.append(j)

        return matched_bands

    '''
    Read the wavelengths from the header file for the original image
    Params: none
    Return: float[]: the wavelength that are used in the original image
    Throws: FileNotFoundError if file does not exist
    '''
    def get_header_wavelengths(self):
        header = self.image_file + ".hdr"

        #the string path of the image
        full_path = os.path.join(self.image_dir, self.image_file)

        #open the image reading in its header then the .img file
        image_file = envi.open(full_path + ".hdr", full_path)

        header_bands = image_file.metadata['wavelength']

        for i in range(len(header_bands)):

            header_bands[i] = float(header_bands[i])

        return header_bands

    '''
    The header has a field where it tells of a value the instrument assigns
    to a pixel value whenever the data be ignored. This function finds that
    value.
    Params: none
    Return: float: the ignore value
    Throws: FileNotFoundError if file does not exist
    '''
    def get_header_data_ignore_value(self):
        header = self.image_file + ".hdr"

        #the string path of the image
        full_path = os.path.join(self.image_dir, self.image_file)

        #open the image reading in its header then the .img file
        image_file = envi.open(full_path + ".hdr", full_path)

        ignore_value = float(image_file.metadata['data ignore value'])

        return ignore_value

    '''
    Get the specific bands that we work with for this project so that the
    image can be loaded according to these bands.
    Params: none
    Return: float[]: the bands from bands.txt
    Throws: FileNotFoundError if file does not exist
    '''
    def get_bands_file(self):
        #open the resource file
        bands_file = open(self.bands_file_path, 'r')

        #read the entries in line by line
        bands = bands_file.readlines()

        #remove the trailing new line character
        for i in range(len(bands)):
            bands[i] = float(bands[i].replace("\n", ""))

        #return the bands as floats
        return bands

    '''
    Read in the original image using all the original bands
    Params: none
    Return: CRISMImage: The image with the wrapper class
    '''
    def get_raw_original_image(self):

        #the string path of the image
        full_path = os.path.join(self.image_dir, self.image_file)

        #open the image reading in its header then the .img file
        image_file = envi.open(full_path + ".hdr", full_path)

        #load the image into memory
        original_image = image_file.load()

        bands = []
        for i in range(len(self.header_bands)):
            bands.append(i)

        image = original_image.read_bands(bands)

        #Put all data up to here into the CRISMImage wrapper class
        crism_image = CRISMImage(image, self.image_file, self.specific_bands, self.header_bands, self.ignore_value)

        return crism_image

    '''
    Get the image using the specific bands that are defiend in bands.txt
    this should be the default.
    Params: none
    Return: Return: CRISMImage: The image with the wrapper class
    '''
    def get_raw_image(self):

        #the string path of the image
        full_path = os.path.join(self.image_dir, self.image_file)

        #open the image reading in its header then the .img file
        image_file = envi.open(full_path + ".hdr", full_path)

        #load the image into memory
        original_image = image_file.load()

        bands = self.match_bands()

        #get the image with only the bands we plan to use
        image = original_image.read_bands(bands).astype(numpy.float, casting='safe')

        #Put all data up to here into the CRISMImage wrapper class
        crism_image = CRISMImage(image, self.image_file, self.specific_bands, self.header_bands, self.ignore_value)

        return crism_image

if __name__ == "__main__":

    imr = ImageReader("HRL000040FF_07_IF183L_TRR3_BATCH_CAT_corr.img")

    img = imr.get_raw_image()

    print(len(img.bands))
