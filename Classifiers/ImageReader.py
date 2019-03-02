# -*- coding: utf-8 -*-

'''
Read in the image from the .img file format where there is a seperate .hdr
file that outlines the contents of the .img file. This reader's principle task
is to take these two files and import only the wavelengths that we need, these
are defined in /Resources/bands.txt. Bands and wavelength are interchanged
frequently in this file, sorry.
'''

import spectral.io.envi as envi

class ImageReader:
    
    #where the specific bands we plan to use is defined
    bands_file_path = "../Resources/bands.txt"
    #head to the images directory
    image_dir = "../Images/"
    
    def __init__(self, imageFile):
        self.image_file = imageFile
        self.header_bands = self.get_header_wavelengths()
        self.specific_bands = self.get_bands_file()
        self.ignore_value = self.get_header_data_ignore_value()
        
    def __del__(self):
        pass
    
    '''
    Match the bands that came from the bands.txt file to the bands from the
    header file. Make an array of the int indices of the bands in header_bands
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
       
        #get the wavelenghts from the header file
        with open(self.image_dir + header) as header_file:
            file = header_file.read()
            
            #get the index where the waves start at
            word = "wavelength = {"
            start_index = file.find(word) + len(word) + 1
            
            #get the place where the waves end
            word = "}"
            end_index = file.find(word, start_index)
            
            #get the bands from the header file
            header_bands = file[start_index:end_index]
            
            #get rid of end the end line character
            header_bands = header_bands.replace("\n", "")
            #split the csv file
            header_bands = header_bands.split(", ")
            
            #convert to float
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
       
        #get the data ignore value from the header file
        with open(self.image_dir + header) as header_file:
            file = header_file.read()
            
            #get the index where the data ignore value is at
            word = "data ignore value = "
            start_index = file.find(word) + len(word)
            
            #the end of line character
            word = "\n"
            end_index = file.find(word, start_index)
            
            ignore_value = file[start_index:end_index]
            
            return float(ignore_value)

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
    Return: nparray[][][]: a matrix of the image with all of the bands from the
            parent file
    '''
    def get_raw_original_image(self):
        
        #the string path of the image
        full_path = self.image_dir + self.image_file
        
        #open the image reading in its header then the .img file
        image_file = envi.open(full_path + ".hdr", full_path)
        
        #load the image into memory
        image = image_file.load()
        
        return image
        
    '''
    Get the image using the specific bands that are defiend in bands.txt
    this should be the default.
    Params: none
    Return: nparray[][][]: a matrix of the image with only the bands from the
            bands.txt file
    '''
    def get_raw_image(self):
        
        #the string path of the image
        full_path = self.image_dir + self.image_file
        
        #open the image reading in its header then the .img file
        image_file = envi.open(full_path + ".hdr", full_path)
        
        #load the image into memory
        original_image = image_file.load()
        
        bands = self.match_bands()
        
        #get the image with only the bands we plan to use
        image = original_image.read_bands(bands)
        
        return image
        
    