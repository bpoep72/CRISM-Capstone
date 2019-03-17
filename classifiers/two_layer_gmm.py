

import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from classifiers.npzFileReader import DataReader
from classifiers.imagereader import ImageReader
import math
import numpy
import scipy.special

class Two_Layer_Gmm:

    #data is a DataReader defined under classifiers/npzFileReader.py
    def __init__(self, image, model):
        self.image = image
        self.data = model

        #outputs
        self.ypred = None
        self.aa = None
        self.loglik = None
    
    def test(self):

        ncl = len(data.mu_s)
        d = len(data.mu_s[0])

        pi_constant = (d / 2) * math.log(math.pi)
        g1_pc = scipy.special.gammaln( numpy.arange(.5, numpy.max(20), .5 ) ) #NOTE This works at execution have no idea why vscode tells me it won't
        n = len(self.image[0])
        loglik = numpy.zeros((n, ncl))
        
        for i in range(ncl):
            v = self.image - self.data.mu_s[i]
            chsig = numpy.linalg.cholesky( data.Sig_s[:, :, i] )
           
            tpar = g1_pc( data.v_s[i] + d ) - ( g1_pc( data.v_s[i] ) + (d/2) * math.log( data.v_s[i] ) + pi_constant ) - numpy.sum( math.log(numpy.diagonal(chsig)))

            temp = mrdivide(v, chsig) #TODO: need to convert this to python still can't find a method that works

            loglik[: i] = tpar - .5 * (data.v_s[i] + d) * math.log(1 + ( 1 / data.v_s[i] )) * numpy.sum( numpy.multiply(temp, temp)[2] )


if __name__ == "__main__":
    
    import npzFileReader
    import os

    parent_directory = os.path.join(os.path.dirname(__file__), '..')

    resource_file = os.path.join(parent_directory, 'Resources', 'neutral_pixel_classifier.npz')

    imr = ImageReader("HRL000040FF_07_IF183L_TRR3_BATCH_CAT_corr.img")

    img = imr.get_raw_image()

    data = npzFileReader.read_file(resource_file)

    #TODO: image is still in the original matrix form need to transform it so each row is a pixel and each column is a dimension
    Two_Layer_Gmm(img.raw_image, data).test()
        