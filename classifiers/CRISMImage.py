# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 16:02:57 2019

This will be the wrapper class for the images. Preprocessing and access to the
data will be achieved through this wrapper.

@author: Bryce
"""

import numpy as np
import time
import spectral as spectral

import sys

class CRISMImage:
    
    def __init__(self, raw_image, image_name, bands, original_bands, ignore_value):
        
        #data that came from the original file
        self.ignore_value = ignore_value
        self.original_bands = original_bands
        self.raw_image = raw_image
        self.image_name = image_name
        
        #data about the image as we see it now       
        self.bands = bands
        self.rows = len(self.raw_image)
        self.columns = len(self.raw_image[0])
        self.dimensions = len(self.raw_image[0][0])

        #initilized only if preprocessing runs.
        self.ignore_matrix = None

        self.preprocess()
         
    def __del__(self):
        del self.raw_image

    def preprocess(self):

        self.ignore_matrix = self.get_ignore_matrix()
        self.fix_bad_pixels()
    
    '''
        The goal of this method is to get a boolean matrix. The pixel has a 1 of any its
        dimensions contain an instance of the data ignore value. If it does not then
        the pixel recieves a 0.

        NOTE: Runs over the whole matrix, this takes alot of time. (2-3mins).
        
        Params: none
        Return: int[rows][cols]:    0 means pixel does not contain the data ignore value,
                                    1 means pixel does contain the data ignore value
    '''
    def get_ignore_matrix(self):
        
        #either a pixel is to be ignored or not ignored so we only need 2 dimensions
        ignore_matrix = np.zeros((self.rows, self.columns))

        #get each pixel from the matrix
        for i in range(self.rows):
            for j in range(self.columns):

                pixel = self.get_pixel_vector(i, j)
                
                #check to see if the pixel contains the data ignore value if it does add
                #  it to the ignore matrix and break (no need to check the rest)
                for k in range(self.dimensions):
                    if pixel[k] == self.ignore_value:
                        ignore_matrix[i, j] = 1
                        break

        return ignore_matrix

    '''
        The goal is to replace all the bad values with values that make the image
        more easily displayed. The pixels containing massive outliers, namely the
        data ignore value, are updated to use the next highest pixel value from that
        band instead of the data ignore value. This makes displaying the images many times
        easier as all we have to do is normalize the image into rgb and we no longer have
        to consider these giant outliers.

        Params: None
        Returns: None
        NOTE: 
            Side Effect: 
                The image will be altered from here forward to no longer contain the
            data ignore value. If you want the original image back you must get it from an
            ImageReader
    '''
    def fix_bad_pixels(self):

        for i in range(self.dimensions):
            max_value = self.get_band_max(i)

            for j in range(self.rows):
                for k in range(self.columns):
                    if self.ignore_matrix[i, k] == 1 and self.raw_image[j, k, i] == self.ignore_value:
                        self.raw_image[j, k, i] = max_value
        
    '''
        The goal of this method is to get a single band based on its index from
        the bands array
        NOTE: This uses the new array not the old one so an operation like 
        imshow(image, [band, band, band]) from the matlab file will not use 
        the same bands as this. to translate pass each of those bands to self.get_new_ref()
    ''' 
    def get_band_by_number(self, band_number):

        if(band_number < 0) or (band_number > len(self.bands)):
            raise Exception("Invalid band number given to get_band_by_number() of Class CRISMImage")
        
        band_matrix = self.raw_image[:, :, band_number]

        return band_matrix

    '''
        Get the maxuimum value within the band, not including the data ignore value
        
        Params: int, the band number
        Return: float, the maximum value
    '''
    def get_band_max(self, band_number):

        max_value = 0
        band = self.get_band_by_number(band_number)

        for i in range(self.rows):
            for j in range(self.columns):
                if band[i, j] > max_value and band[i, j] != self.ignore_value:
                    max_value = band[i, j]

        return max_value

    '''
        Get the minimum value within the band
        
        Params: int, the band number
        Return: float, the minimum value
    '''
    def get_band_min(self, band_number):

        #set the min to "infinity"
        min_value = sys.float_info.max
        band = self.get_band_by_number(band_number)

        for i in range(self.rows):
            for j in range(self.columns):
                if band[i, j] < min_value and band[i, j] != self.ignore_value:
                    min_value = band[i, j]

        return min_value
        
    '''
        Get the array for a single pixel in the image

        Params:
            row: int, the row within the image the pixel comes from
            column: int, the column within the image the pixel comes from
        Return: 
            float[], the vector for that pixel
    '''
    def get_pixel_vector(self, row, column):

        return self.raw_image[row, column, :]

    '''
        Get the matrix that represents a band of a given wavelength

        Params: float, the wavelength
        Return: float[][], the band matrix
    '''
    def get_band_by_wavelength(self, wave_length):
        
        band = self.get_band_index(wave_length)
        
        return self.get_band_by_number(band)

    '''
        Get the matrix that represents a band of a given index in the self.bands

        Params: int, the index of the band
        Return: float[][], the band matrix
    '''
    def get_band_index(self, wave_length):

        try:
            return self.bands.index(wave_length)
        except ValueError:
            return -1

    '''
        Take the index of a band in the original image and translate it to
        an index in the new self.bands array
        
        Param: int - a band number from the original image
        Return: int - the band number from the new bands array, -1 if that band does
            not exist the in the new image
    '''
    def get_new_ref(self, band):
        
        wave_length = self.original_bands[band]

        try:
            referenced_index = self.bands.index(wave_length)
            return referenced_index
        except ValueError:
            return -1

if __name__ == "__main__":

    import os.path
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from classifiers.imagereader import ImageReader
    
    imr = ImageReader("HRL000040FF_07_IF183L_TRR3_BATCH_CAT_corr.img")
    
    t = time.time()

    img = imr.get_raw_image()

    elapsed = time.time() - t

    print(elapsed)


