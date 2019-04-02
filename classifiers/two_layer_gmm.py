

import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from classifiers.npzFileReader import DataReader
from classifiers.imagereader import ImageReader
import math
import numpy
import scipy.special
import scipy.linalg

'''
    Use a student T distribution to make a prediction about the input image based on the model files
'''

class Two_Layer_Gmm:

    #data is a DataReader defined under classifiers/npzFileReader.py
    def __init__(self, image, model):
        self.image = image
        self.data = model
        self.normalized_image = self.norm_image()

        #outputs
        self.ypred = None
        self.aa = None
        self.bb = None
    
    def test(self):

        ncl = len(data.mu_s)
        d = len(data.mu_s[0])

        pi_constant = (d / 2) * math.log(math.pi)
        #g1_pc is a range of values
        g1_pc = scipy.special.gammaln( numpy.arange(.5, numpy.max(self.data.v_s[:]) + d + .5, .5 ) )
        n = len(self.normalized_image)
        loglik = numpy.zeros((n, ncl))
        
        for i in range(ncl):
            v = self.normalized_image - self.data.mu_s[i, :]
            chsig = numpy.linalg.cholesky( self.data.Sig_s[:, :, i] )

            #-1 due to 0 vs 1 based indexing (0 based is superior, fight me)
            x = g1_pc[ self.data.v_s[i] + d - 1]
            y = g1_pc[ self.data.v_s[i] - 1 ] + (d/2) * math.log( self.data.v_s[i] ) + pi_constant
            z = numpy.sum( numpy.log(numpy.diagonal(chsig)) )
           
            tpar = x - ( y ) - z

            #solve Ax = B where chsig is A and v is B
            temp = numpy.linalg.lstsq(chsig, v.T, rcond=None)[0].T

            a = (self.data.v_s[i] + d)
            b = numpy.sum( numpy.multiply(temp, temp), axis=1)
            c = numpy.log(1 + ( 1 / self.data.v_s[i] ) * b)

            loglik[:, i] = tpar - .5 * a * c

        #find the max across the rows
        self.aa = numpy.amax(loglik, axis=1)
        #find where the max occurs
        self.bb = numpy.argmax(loglik, axis=1)
        #predict that the index of the max of each row is associated with a class id
        self.ypred = self.data.class_id[self.bb]

        '''
        Normalizes each pixel to be length 1. Store the resulting matrix into self.normalized_image.
        We store it there because it messes with the display of the image if we did it anywhere else.
        Also we only need this to run the normalized image through the two layer gmm. We only used 50
        channels for this step. Given that the two layer gmm test expects the image to be in the shape
        where each pixel is a row we do that here.

        Params: None
        Returns: float[][], the normalized image where each row is a single pixel vector

    '''
    def norm_image(self):

        #init an empty matrix
        normalized_image = numpy.zeros( (self.image.rows * self.image.columns, self.data.fin.size) )

        #reshape the image such that each pixel is a row in the image variable
        image = numpy.reshape( self.image.raw_image, (self.image.rows * self.image.columns, self.image.dimensions) )

        #1 based indexing fix
        self.data.fin = self.data.fin - 1

        #remove the columns that we don't need according to fin
        reduced_image = image[:, self.data.fin]

        row_norms = numpy.linalg.norm(reduced_image, axis=2)

        for i in range(len(row_norms)):
            normalized_image[i] = numpy.divide(reduced_image[i, :], row_norms[i])

        return normalized_image

if __name__ == "__main__":
    
    import npzFileReader
    import os

    parent_directory = os.path.join(os.path.dirname(__file__), '..')

    resource_file = os.path.join(parent_directory, 'Resources', 'neutral_pixel_classifier.npz')

    imr = ImageReader("HRL000040FF_07_IF183L_TRR3_BATCH_CAT_corr.img")

    img = imr.get_raw_image()

    image = numpy.reshape( img.raw_image, (img.rows * img.columns, img.dimensions) )

    data = npzFileReader.read_file(resource_file)

    Two_Layer_Gmm(img, data).test()
        