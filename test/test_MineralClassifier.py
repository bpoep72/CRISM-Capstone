
import unittest
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from classifiers.crismimage import CRISMImage
from classifiers.imagereader import ImageReader
from classifiers.mineral_classifier import MineralClassfier

class test_MineralClassifier(unittest.TestCase):

    #the image from which all oracle data was derived for these tests
    #this image is expected to be in /Images/<the file>
    imr = ImageReader("HRL000040FF_07_IF183L_TRR3_BATCH_CAT_corr.img")

    img = imr.get_raw_image()

    '''
        Objective: Test that the normalized image from neutral_pixel_norm() is exactly as expected
    '''
    def test_neutral_pixel_norm(self):

        pass

if __name__ == '__main__':
    unittest.main()