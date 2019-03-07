# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 16:02:57 2019

This will be the wrapper class for the images. Preprocessing and access to the
data will be achieved through this wrapper.

@author: Bryce
"""

import numpy as np

import sys
import ImageReader

class CRISMImage:
    
    def __init__(self, raw_image, image_name, bands, original_bands, ignore_value):
        
        self.raw_image = raw_image
        self.image_name = image_name
        self.bands = bands
        self.ignore_value = ignore_value
        self.original_bands = original_bands
        
        self.rows = len(self.raw_image)
        self.columns = len(self.raw_image[0])
        self.dimensions = len(self.raw_image[0][0])
         
    def __del__(self):
        del self.raw_image
    
    '''
        The goal of this method is to get a boolean matrix. The pixel has a 1 of any its
        dimensions contain an instance of the data ignore value. If it does not then
        the pixel recieves a 0
        Params: none
        Return: boolean[rows][cols]
    '''
    def get_ignore_matrix(self):
        
        for i in range(self.dimensions):
            pass
        
    '''
        The goal of this method is to get a single band based on its index from
        the bands array
        NOTE: This uses the new array not the old one so an operation like 
        imshow(image, [band, band, band]) will not use the same bands as this
    ''' 
    def get_band_by_number(self, band_number):

        if(band_number == -1) or (band_number > len(self.bands)):
            raise Exception("Invalid band number given to get_band_by_number() of Class CRISMImage")
        
        band_matrix = self.raw_image[:, :, band_number]

        return band_matrix
    
    def get_band_by_wavelength(self, wave_length):
        
        band = self.get_band_index(wave_length)
        
        return self.get_band_by_number(band)

    '''
        Get the index of the band based on its wavelength
        Param: int - the wave length to find
        Return: int - the index of the band in self.bands, -1 if not found
    '''
    def get_band_index(self, wave_length):
        
        return self.bands.index(wave_length)

    '''
        Take the index of a band in the original image and translate it to
        an index in the new self.bands array
        Param: int - a band number from the original image
        Return: int - the band number from the new bands array, -1 if that band does
            not exist the in the new image
    '''
    def get_new_ref(self, band):
        
        wave_length = self.original_bands[band]
        
        return self.bands.index(wave_length)


if __name__ == "__main__":
    
    imr = image_reader.ImageReader("HRL000040FF_07_IF183L_TRR3_BATCH_CAT_corr.img")

    img = imr.get_raw_image()
    print(len(img.original_bands))
    print(len(img.bands))

    print(img.get_band_by_number(2))

    print(img.get_new_ref(54))

    print('rows', img.rows)
    print('cols', img.columns)
    print('dims', img.dimensions)

    