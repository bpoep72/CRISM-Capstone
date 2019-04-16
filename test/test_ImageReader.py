
import unittest
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from classifiers.crismimage import CRISMImage
from classifiers.imagereader import ImageReader

class test_ImageReader(unittest.TestCase):

    #the image from which all oracle data was derived for these tests
    #this image is expected to be in /Images/<the file>
    imr = ImageReader("HRL000040FF_07_IF183L_TRR3_BATCH_CAT_corr.img")

    image = imr.get_raw_image()
    image2 = imr.get_raw_original_image()

    '''
        Objective: compare the lengths of the arrays from bands.txt
        and the matched bands these should be the same length
    '''
    def test_match_bands(self):

        bands = self.imr.match_bands()
        
        self.assertEqual(len(bands), len(self.imr.specific_bands))

    def test_get_bands_file(self):

        self.assertEqual(len(self.imr.specific_bands), 350)

    '''
        Objective: check that we successfully got the data ignore value from the file
    '''
    def test_get_data_ignore_value(self):

        self.assertEqual(self.imr.get_header_data_ignore_value(), 65535.0)

    '''
        Objective: check that the image maintained the same features once it was exported
        to the image wrapper to check that get_raw_image worked as expected
    '''
    def test_get_raw_image(self):

        self.assertEqual(self.image.rows, 480)
        self.assertEqual(self.image.columns, 320)
        self.assertEqual(self.image.dimensions, 350)

    '''
        Objective: check that the image maintained the same features once it was exported
        to the image wrapper to check that get_raw_image worked as expected
    '''
    def test_get_original_image(self):

        self.assertEqual(self.image2.rows, 480)
        self.assertEqual(self.image2.columns, 320)
        self.assertEqual(self.image2.dimensions, 438)  

    
if __name__ == '__main__':
    unittest.main()