
import unittest
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from classifiers.crismimage import CRISMImage
from classifiers.imagereader import ImageReader

class test_CRISMImage(unittest.TestCase):

    #the image from which all oracle data was derived for these tests
    #this image is expected to be in /Images/<the file>
    imr = ImageReader("HRL000040FF_07_IF183L_TRR3_BATCH_CAT_corr.img")

    image = imr.get_raw_image()

    '''
        Objective: Ensure that CRISMImage.get_new_ref() can convert an old band reference
        to a new one if it exists and returns -1 otherwise
    '''
    def test_get_new_ref(self):
        
        #old ref should be not exist in the new image
        value = self.image.get_new_ref(1)
        self.assertEqual(value, -1)

        #old ref should exist in the new image
        value = self.image.get_new_ref(3)
        self.assertEqual(value, 0)

    def test_get_band_max(self):

        value = self.image.get_band_max(0)

        self.assertAlmostEqual(value, 0.23118185)

    def test_get_band_min(self):

        value = self.image.get_band_min(0)

        self.assertAlmostEqual(value, 0.12474143)
    
if __name__ == '__main__':
    unittest.main()