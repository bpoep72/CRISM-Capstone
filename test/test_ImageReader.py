
import unittest
import classifiers
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from classifiers.crismimage import CRISMImage
from classifiers.imagereader import ImageReader

class test_ImageReader(unittest.TestCase):

    #the image from which all oracle data was derived for these tests
    image = "HRL000040FF_07_IF183L_TRR3_BATCH_CAT_corr.img"

    '''
        Objective: compare the lengths of the arrays from bands.txt
        and the matched bands these should be the same length
    '''
    def test_match_bands(self):
        
        imr = ImageReader(self.image)

        bands = imr.match_bands()
        self.assertEqual(len(bands), len(imr.specific_bands))

    def test_get_bands_file(self):

        imr = ImageReader(self.image)

        self.assertEqual(len(imr.specific_bands), 350)

    '''
        Objective: check that we successfully got the data ignore value from the file
    '''
    def test_get_data_ignore_value(self):
       
        imr = ImageReader(self.image)

        self.assertEqual(imr.get_header_data_ignore_value(), 65535.0)

    '''
        Objective: check that the image maintained the same features once it was exported
        to the image wrapper to check that get_raw_image worked as expected
    '''
    def test_get_raw_image(self):

        imr = ImageReader(self.image)

        image = imr.get_raw_image()

        self.assertEqual(image.rows, 480)
        self.assertEqual(image.columns, 320)
        self.assertEqual(image.dimensions, 350)

    '''
        Objective: check that the image maintained the same features once it was exported
        to the image wrapper to check that get_raw_image worked as expected
    '''
    def test_get_original_image(self):

        imr = ImageReader(self.image)

        image = imr.get_raw_original_image()

        self.assertEqual(image.dimensions, 438)
        self.assertEqual(image.rows, 480)
        self.assertEqual(image.columns, 320)
        

    
if __name__ == '__main__':
    unittest.main()