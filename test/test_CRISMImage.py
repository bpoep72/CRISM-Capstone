
import unittest
import classifiers
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from classifiers.crismimage import CRISMImage
from classifiers.imagereader import ImageReader

class test_CRISMImage(unittest.TestCase):

    image = "HRL000040FF_07_IF183L_TRR3_BATCH_CAT_corr.img"

    pass