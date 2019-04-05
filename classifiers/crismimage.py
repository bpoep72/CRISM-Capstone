# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 16:02:57 2019

This will be the wrapper class for the images. Preprocessing and access to the
data will be achieved through this wrapper.

@author: Bryce
"""

import numpy as numpy
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
        self.normalized_image = None
        self.preprocess()
         
    def __del__(self):
        del self.raw_image

    '''
        These are the preprocessing tasks, some of these can take a large amount of time
        and thus they were added to this method so that toggling it could be made easier
        should such a need arise later on.

        Params: None
        Returns: None
    '''
    def preprocess(self):

        self.ignore_matrix = self.get_ignore_matrix()
        self.fix_bad_pixels()
    
    '''
        The goal of this method is to get a boolean matrix representing instances of the
        data ignore value. The pixel has a 1 of any its dimensions contain an instance 
        of the data ignore value. If it does not then the pixel recieves a 0.
        
        Params: none
        Return: int[rows][cols]:    0 means pixel does not contain the data ignore value,
                                    1 means pixel does contain the data ignore value
    '''
    def get_ignore_matrix(self):
        
        #find all occurences of the data ignore value
        bad_data = self.raw_image > 1000

        #sum up the number of occurences to get the (x, y) view
        bad_data = numpy.sum(bad_data, axis=2)

        #get the logical view in (x, y), if the ignored values occured 1 or more times along z then (x, y) = true else false
        ignore_matrix = bad_data > 0

        return ignore_matrix

    '''
        The goal is to replace all the bad values with values that make the image
        more easily displayed. The pixels containing massive outliers, namely the
        data ignore value, are updated to use the mean of the whole data excluding 
        the data ignore value, though there are a few other outliers.This makes 
        displaying the images many times easier as all we have to do is normalize 
        the image into rgb and we no longer have to consider these giant outliers.

        NOTE: 1000 is a magic number that we were given to use for this

        Params: None
        Returns: None  
    '''
    def fix_bad_pixels(self):

        #get the logical view of the data for whether or not the data ignore value is present
        good_data = self.raw_image < 1000

        #to get the mean we need the number of good data points and their sum
        num_good_data_pts = numpy.sum(good_data)

        #multiply the logical view with the original data to get only the good data 
        good_data = numpy.multiply(self.raw_image, good_data)

        #sum up all good data
        sum_of_data = numpy.sum(good_data)

        #find the mean
        mean_of_data = sum_of_data / num_good_data_pts

        #replace all occurences of the data ignore value with the mean of the data
        self.raw_image[self.raw_image > 1000] = mean_of_data
        
    '''
        The goal of this method is to get a single band based on its index from
        the bands array. 

        NOTE: This uses the new array not the old one so an operation like 
        imshow(image, [band, band, band]) from the matlab file will not use 
        the same bands as this. to translate pass each of those bands to self.get_new_ref()
    ''' 
    def get_band_by_number(self, band_number):

        if(band_number < 0) or (band_number > len(self.bands) - 1):
            raise Exception("Invalid band number", band_number, " given to get_band_by_number() of Class CRISMImage")
        
        band_matrix = self.raw_image[:, :, band_number]

        return band_matrix

    '''
        Get the maxuimum value within the band, not including the data ignore value
        
        Params: int, the band number
        Return: float, the maximum value
    '''
    def get_band_max(self, band_number):

        #isolate the band
        band = self.raw_image[:, :, band_number]
        
        #remove the data ignore value if it exists
        band = band[band != self.ignore_value]

        #return the maximum
        return numpy.max(band)

    '''
        Get the minimum value within the band
        
        Params: int, the band number
        Return: float, the minimum value
    '''
    def get_band_min(self, band_number):

        #isolate the band
        band = self.raw_image[:, :, band_number]
        
        #remove the data ignore value if it exists
        band = band[band != self.ignore_value]

        #return the minumum
        return numpy.min(band)
        
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

    '''
        Normalize a band to be between 0-1 for use when displaying the image

        Params: int, the band to be normalized
        Returns: float (0-1), the normalized band
    '''
    def normalize_band(self, band_number):

        min_value = self.get_band_min(band_number)
        max_value = self.get_band_max(band_number)

        norm_band = numpy.zeros((self.rows, self.columns))

        #if normalization was already done
        if min_value == 0 and max_value == 1:
            pass
        else:
            for i in range(self.rows):
                for j in range(self.columns):
                    old_value = self.raw_image[i, j, band_number]
                    norm_band[i, j] = (old_value - min_value) / (max_value - min_value)

        return norm_band

    '''
        Get just the 3 bands that we need. Channels 1-3 will be RGB values that can be displayed using
        matlibplot's imshow function

        Params: int, the channel numbers that you want to display
        Returns: int[][][3], the 3 channel image as a matrix
    '''
    def get_three_channel(self, channel_1, channel_2, channel_3):

        image = numpy.zeros((self.rows, self.columns, 3))

        norm_channel_1 = self.normalize_band(channel_1)
        norm_channel_2 = self.normalize_band(channel_2)
        norm_channel_3 = self.normalize_band(channel_3)

        image[:, :, 0] = norm_channel_1
        image[:, :, 1] = norm_channel_2
        image[:, :, 2] = norm_channel_3

        return image

if __name__ == "__main__":
    
    from imagereader import ImageReader
    from matplotlib import pyplot
    
    imr = ImageReader("HRL000040FF_07_IF183L_TRR3_BATCH_CAT_corr.img")

    img = imr.get_raw_image()

    pyplot.imshow(img.get_three_channel(233, 78, 13))
    pyplot.show()
