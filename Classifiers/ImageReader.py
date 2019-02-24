# -*- coding: utf-8 -*-

class ImageReader:
    
    #where the specific bands we plan to use is presently defined
    bands_file_path = "../Resources/bands.txt"
    image_dir = "../Images/"
    
    def __init__(self, imageFile):
        self.image_file = imageFile
        
    def __del__(self):
        pass

    #Get the header file if it exists
    #Params: none
    #Return: the header file
    #Throws: FileNotFoundError if file does not exist
    def get_Header(self):
        header = self.image_file + ".hdr"
       
        try:
            header_file = open(header, 'r')
            header_file.close()
        except FileNotFoundError:
            raise FileNotFoundError("Image File is missing its corresponding header.")

    #Get the specific bands that we work with for this project so that the 
    #can be loaded according to these bands
    #Params: none
    #Return: float[] bands
    def get_bands(self):
        #open the resource file
        bands_file = open(self.bands_file_path, 'r')
        
        #read the entries in line by line
        bands = bands_file.readlines()
        
        #remove the trailing new line character
        for i in range(len(bands)):
            bands[i] = float(bands[i].replace("\n", ""))
            
        #return the bands as floats
        return bands
    
    