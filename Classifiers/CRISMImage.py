# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 16:02:57 2019

This will be the wrapper class for the images. Preprocessing and access to the
data will be achieved through this wrapper.

@author: Bryce
"""

import numpy as np

class CRISMImage:
    
    def __init__(self, raw_image, image_name, bands, ignore_value):
        self.raw_image = raw_image
        self.image_name = image_name
        self.bands = bands
        self.ignore_value = ignore_value
        
        self.rows = len(self.raw_image)
        self.columns = len(self.raw_image[0])
        self.dimensions = len(self.raw_image[0][0])
        
         
    def __del__(self):
        pass
    
    '''
    
    '''
    def get_ignore_matrix(self):
        
        for i in range(self.dimensions):
            pass
        
    def get_band_by_number(self, band_number):
        
        dimensions = [self.rows, self.columns]
        
        band_matrix = np.asarray(dimensions)
        
        for i in range(self.rows):
            for j in range(self.columns):
                band_matrix[i][j] = self.raw_image[i][j][band_number]
    
    def get_band_by_wavelength(self, wave_length):
        
        band = self.bands.find(wave_length)
        
        return self.get_band_by_number(band)