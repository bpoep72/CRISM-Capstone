
import math
import numpy
import scipy.special
import scipy.linalg
from npzFileReader import read_file

import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class MineralClassfier:

    def __init__(self, image):

        self.image = image
        self.mineral_model = self.get_model("neutral_pixel_classifier.npz")
        self.neutral_pixel_model = self.get_model("mineral_classifier.npz")
        self.normalized_image = self.neutral_pixel_norm()
        self.neutral_image = self.neutral_pixel_classification()

    '''
        Loads a model file set using the npzFileReader. These models are used in
        both classifiers.

        Params: None
        Returns: DataReader, This is the object that the model data is stored within.
    '''
    def get_model(self, model_file_name):

        parent_directory = os.path.join(os.path.dirname(__file__), '..')

        resource_file = os.path.join(parent_directory, 'Resources', model_file_name)

        model = read_file(resource_file)

        return model

    '''
        Perform the neutral pixel classification and prepare the input image for use
        in the mineral classifier.

        Params: None
        Returns: numpy.double[][][], the neutralized image
    '''
    def neutral_pixel_classification(self):

        model = self.neutral_pixel_model

        classifier_ouput = self.two_layer_gmm(self.normalized_image, model.sigma, model.mu, model.v_s, model.class_id)

        #TODO: finish this method
        #NOTE: slogs are in classifier_ouput[2]

        neutral_image = None

        return neutral_image

    '''
        Perform the mineral classification and return the output as the formatted classification map
        so that if can be easily used within the gui.

        Params: None
        Return: ClassificationMap, the output of the classifier
    '''
    def mineral_classification(self):

        model = self.mineral_model

        classifier_ouput = self.two_layer_gmm(self.image.raw_image, model.sigma, model.mu, model.v_s, model.class_id)

        #TODO: finish this method

    '''
        Use a student T distribution to make a prediction about the input image 
        based on the model files data. Will expect that the images have been properly
        normalized.

        Params:
            image, the input image
            simga, the covariance matrix
            mu, the means
            v_s, ?
            class_ids, The class labels assigned to each row of the output
        Output:
            NOTE: give as a 1x3 tuple
            aa, the max across the rows
            bb, the index where the max occurs
            ypred, the label predictions
    '''
    def two_layer_gmm(self, image, sigma, mu, v_s, class_ids):

        ncl = len(mu)
        d = len(mu[0])

        pi_constant = (d / 2) * math.log(math.pi)
        #g1_pc is a range of values on which we evoke the gamma function
        g1_pc = scipy.special.gammaln( numpy.arange(.5, numpy.max(v_s[:]) + d + .5, .5 ) )
        n = len(image)
        loglik = numpy.zeros((n, ncl))
        
        for i in range(ncl):
            v = image - mu[i, :]
            chsig = numpy.linalg.cholesky( sigma[:, :, i] )

            # the -1  is due to 0 vs 1 based indexing (0 based is superior, fight me)
            x = g1_pc[ v_s[i] + d - 1]
            y = g1_pc[ v_s[i] - 1 ] + (d/2) * math.log( v_s[i] ) + pi_constant
            z = numpy.sum( numpy.log(numpy.diagonal(chsig)) )
           
            tpar = x - ( y ) - z

            #solve Ax = B where chsig is A and v is B
            temp = numpy.linalg.lstsq(chsig, v.T, rcond=None)[0].T

            a = (v_s[i] + d)
            b = numpy.sum( numpy.multiply(temp, temp), axis=1)
            c = numpy.log(1 + ( 1 / v_s[i] ) * b)

            loglik[:, i] = tpar - .5 * a * c

        #find the max across the rows
        aa = numpy.amax( loglik, axis=1 )
        #find index where the max occurs
        bb = numpy.argmax( loglik, axis=1 )
        #predict that the index of the max of each row is associated with a class id
        ypred = class_ids[ bb ]

        return aa, bb, ypred

    '''
        To be passed to two layer gmm the image must be normalized 
        such that each pixel has norm == 1. We only use the bands that
        are defined by neutral_pixel_model.fin for the neutral pixel 
        classification, all others are discarded.

        Params: None
        Returns: float[][], the normalized image where each row is a single pixel vector

    '''
    def neutral_pixel_norm(self):

        #init an empty matrix
        normalized_image = numpy.zeros( (self.image.rows * self.image.columns, self.neutral_pixel_model.fin.size) )

        #reshape the image such that each pixel is a row in the image variable
        image = numpy.reshape( self.image.raw_image, (self.image.rows * self.image.columns, self.image.dimensions) )

        #1 based indexing fix
        self.neutral_pixel_model.fin = self.neutral_pixel_model.fin - 1

        #remove the columns that we don't need according to fin
        reduced_image = image[:, self.neutral_pixel_model.fin]

        row_norms = numpy.linalg.norm(reduced_image, axis=2)

        for i in range(len(row_norms)):
            normalized_image[i] = numpy.divide(reduced_image[i, :], row_norms[i])

        return normalized_image