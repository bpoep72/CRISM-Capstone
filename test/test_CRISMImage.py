
import unittest
import classifiers
import os.path
import sys
#add the root of the project to the system path 
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from classifiers.crismimage import CRISMImage
from classifiers.imagereader import ImageReader

class test_CRISMImage(unittest.TestCase):

    #the image from which all oracle data was derived for these tests
    image = "HRL000040FF_07_IF183L_TRR3_BATCH_CAT_corr.img"

    '''
        Objective: Ensure that CRISMImage.get_new_ref() can convert an old band reference
        to a new one if it exists and returns -1 otherwise
    '''
    def test_get_new_ref(self):
        
        imr = ImageReader(self.image)

        image = imr.get_raw_image()

        #old ref should be not exist in the new image
        value = image.get_new_ref(1)
        self.assertEqual(value, -1)

        #old ref should exist in the new image
        value = image.get_new_ref(3)
        self.assertEqual(value, 0)

    
