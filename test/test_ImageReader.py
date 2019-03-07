
import unittest
import classifiers

from classifiers.CRISMImage import CRISMImage
from classifiers.ImageReader import ImageReader

class test_ImageReader(unittest.TestCase):

    def test_match_bands(self):
        imr = ImageReader("")

        bands = imr.match_bands()
        self.assertEqual(len(bands), len(imr.specific_bands))


if __name__ == '__main__':
    unittest.main()