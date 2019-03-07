
import unittest

import classifiers

help(classifiers)

class test_ImageReader(unittest.TestCase):

    def test_match_bands(self):
        imr = classifiers.Image_Reader.ImageReader("")

        bands = imr.match_bands()
        self.assertEqual(len(bands), len(imr.specific_bands))

        pass


if __name__ == '__main__':
    unittest.main()