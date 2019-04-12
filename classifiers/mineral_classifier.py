
import math
import numpy
import scipy.special
import scipy.linalg
from scipy.signal import medfilt

import time

import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from npzFileReader import read_file
from classificationmap import ClassificationMap

class MineralClassfier:

    def __init__(self, image):

        #image expects a CRISMImage
        self.image = image

        #the predefined model files need to be loaded
        self.mineral_model = self.get_model("mineral_classifier.npz")
        self.neutral_pixel_model = self.get_model("neutral_pixel_classifier.npz")
 
        #the default parameters for the classifications
        self.ratioing_window_size = 25
        self.M_highest_slogs = 5
        self.median_filter_window_size = 17

        #images that are generated by the classifier
        self.normalized_image = self.neutral_pixel_norm()
        self.neutral_image = self.ratioing(self.M_highest_slogs, self.ratioing_window_size)
        self.median_image = self.median_filtering(self.median_filter_window_size)

        #the first one is commented out for now to save execution time
        #self.mineral_classification_map = self.mineral_classification()
        self.mineral_classification_map = None

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

        model.fin = model.fin - 1

        return model

    '''
        Perform the neutral pixel classification and prepare the input image for use
        in the mineral classifier. Then ratio's the pixels based on the output of that
        classification to stabilize the image before median filtering and mineral classification

        Params: 
            highest_slogs, the number of pixels with the highest slog scores to find
            window_size, the window size    
        Returns: 
            numpy.double[][], the neutralized image
    '''
    def ratioing(self, highest_slogs, window_size):

        model = self.neutral_pixel_model

        classifier_ouput = self.two_layer_gmm(self.normalized_image, model.Sig_s, model.mu_s, model.v_s, model.class_id)

        loglik = classifier_ouput[2]

        #we only use the first 4 columns of loglik
        loglik = loglik[:, 0:len(loglik[0]) - 1]

        #slogs are the sums of the columns of loglik
        slogs = numpy.sum(loglik, axis=1)
        neutral_image = numpy.zeros((self.image.columns * self.image.rows, self.image.dimensions))
        
        #we need x_ind and y_ind to distinguish where a pixel was in the original image
        #all that x_ind and y_ind act as a map between the linear image and the original shape of the image
        indices = numpy.arange(0, self.image.columns)
        x_ind = numpy.tile(indices, self.image.rows)

        y_ind = numpy.zeros((self.image.rows * self.image.columns))  
        for i in range(self.image.rows):

            indices = numpy.ones((self.image.columns)) * i
            y_ind[self.image.columns * i:self.image.columns * (i + 1)] = indices

        #cast y_ind to int
        y_ind = y_ind.astype(int)

        #the linearized ignore matrix
        ignore_matrix = numpy.reshape(self.image.ignore_matrix, (self.image.rows * self.image.columns))

        ''' There are a collection of logical clauses for the next section that
            are calculated outside the loop body. This is to save time in execution
            given that otherwise they would need to be recalculated each iteration.
            Each clause independant of i is below.
        '''
        #clause for all the branches
        clause_1 = ignore_matrix != 1 #if pixel is not in the ignore matrix

        #clause for if(y_ind[i] < window_size - 1):
        clause_2 = y_ind < ( 2 * window_size - 1 ) #NOTE in this case window size is an index

        #clauses for elif(y_ind[i] > self.image.rows - window_size - 1):
        clause_3 = y_ind > self.image.rows - 1 - ( 2 * window_size )
        clause_4 = y_ind < self.image.rows - 1

        t = time.time()

        print(t)

        for i in range(self.image.rows * self.image.columns):

            #upper edge of image
            if(y_ind[i] < window_size - 1):
                
                clause_0 = x_ind == x_ind[i]

                #the product of the logical clauses is the input to the next if branch
                indices = numpy.multiply(clause_0, clause_1)
                indices = numpy.multiply(indices, clause_2)

            #lower edge of image
            elif(y_ind[i] > self.image.rows - 1 - window_size):
                
                clause_0 = x_ind == x_ind[i]

                indices = numpy.multiply(clause_0, clause_1)
                indices = numpy.multiply(indices, clause_3)
                indices = numpy.multiply(indices, clause_4)
            
            #middle pixels
            else:

                clause_0 = x_ind == x_ind[i]
                clause_5 = y_ind > y_ind[i] - window_size
                clause_6 = y_ind < y_ind[i] + window_size

                indices = numpy.multiply(clause_0, clause_1)
                indices = numpy.multiply(indices, clause_5)
                indices = numpy.multiply(indices, clause_6)

            image_linearized = numpy.reshape( self.image.raw_image, (self.image.rows * self.image.columns, self.image.dimensions) )

            #get where the pixels need to manipulated
            if(numpy.sum(indices == True) > 0):
                IFi = image_linearized[indices]
                ppi = slogs[indices]
                ppiind = numpy.argpartition(ppi, -highest_slogs, axis=0)[-highest_slogs:]
                neutral_image[i,:] = numpy.divide(self.image.get_pixel_vector(y_ind[i], x_ind[i]), numpy.mean(IFi[ppiind], axis=0) )

        elapsed = time.time() - t
        print(elapsed)
        
        return neutral_image

    '''
        Perform the median and prepare the input image for use
        in the mineral classifier.

        Params: window_size, the size of the window to use
        Returns: numpy.double[][], the filtered
    '''
    def median_filtering(self, window_size):
        #TODO: deal with edge cases that are calculated differently due to MATLAB using a truncate function
        filtered_image = numpy.zeros([self.image.columns * self.image.rows, self.image.dimensions])
        IF1 = medfilt(self.neutral_image, kernel_size=[1, window_size])
        tmp = abs(IF1 - self.neutral_image)
        #MATLAB code used values from 1 to 248 here so I followed suit
        indices = tmp > numpy.mean(numpy.mean(tmp[:,0:247], axis=1)) + 1.5*numpy.mean(numpy.std(tmp[:,0:247], axis=1))
        filtered_image[indices] = IF1[indices]
        
        return filtered_image

    '''
        Perform the mineral classification and return the output as the formatted classification map
        so that if can be easily used within the gui.

        Params: None
        Return: ClassificationMap, the output of the classifier
    '''
    def mineral_classification(self):

        model = self.mineral_model

        image = self.median_image

        #use only the bands specified by self.mineral_model.fin
        reduced_image = image[:, model.fin]

        #normalize the image
        reduced_image = reduced_image - numpy.amin(reduced_image, axis=1) * numpy.ones( (1, len(model.fin)) )
        diff = ( numpy.amax(reduced_image, axis=1) - numpy.amin(reduced_image, axis=1) ) * numpy.ones(1, len(model.fin))
        reduced_image[ numpy.sum(diff, axis=1) != 0, :] = numpy.divide( reduced_image[numpy.sum(diff, axis=1) != 0, : ], diff[sum(diff, 1) != 0, :])
        reduced_image[ numpy.sum(diff, axis=1) == 0, :] = numpy.zeros( numpy.sum(numpy.sum(diff, axis=1) == 0), len(model.fin) )

        #call the classification method
        classifier_ouput = self.two_layer_gmm(reduced_image, model.Sig_s, model.mu_s, model.v_s, model.class_id)

        #format the output
        self.mineral_classification_map = ClassificationMap(classifier_ouput[0])

        return self.mineral_classification_map

    '''
        Use a student T distribution to make a prediction about the input image 
        based on the model files data. Will expect that the images have been properly
        normalized when coming into this function. This differs slightly based on the
        so it is left outside this method.

        Params:
            image, the input image
            simga, the covariance matrix
            mu, the means
            v_s, ?
            class_ids, The class labels assigned to each row of the output
        Output:
            NOTE: return is given as a 3x1 tuple
            ypred, the label predictions
            aa, the max across the rows
            loglik, the 
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

        return ypred, aa, loglik

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

        #remove the columns that we don't need according to fin
        reduced_image = image[:, self.neutral_pixel_model.fin]

        row_norms = numpy.linalg.norm(reduced_image, axis=2)

        for i in range(len(row_norms)):
            normalized_image[i] = numpy.divide(reduced_image[i, :], row_norms[i])

        return normalized_image

    '''
        Do not rerun mineral classification of you don't need to.
        This method is put here to emphasis that.
        Recalculation takes a long time.
    '''
    def get_mineral_classification(self):
        return self.mineral_classification_map

    '''
        This is the method that should trigger the recalculation and update of the classifier
        whenever the highest slogs and window_size parameters are changed. Will automate the
        the recalculation of the classification as well as the median filtering, the ratioing
        and the mineral classification. 
        
        NOTE: the GUI will need to be updated after this is evoked

        Params:
            highest_slogs: int, the number of slogs to use in the ratioing to clean up bad pixels
            window_size: int, how large the window to find the highest slogs is
    '''
    def update_ratioing_parameters(self, highest_slogs, window_size):

        #the values that are updated
        self.M_highest_slogs = highest_slogs
        self.ratioing_window_size = window_size

        #the recalculations
        self.neutral_image = self.ratioing(self.M_highest_slogs, self.ratioing_window_size)
        self.median_image = self.median_filtering(self.median_filter_window_size)
        self.mineral_classification()

    '''
        This method will trigger the required recalculations whenever the median filtering
        parameters is changed.

        Params:
            windows_size, int: the new windows size to be used for median filtering
    '''
    def update_median_filtering_parameters(self, window_size):

        #the value that is updated
        self.median_filter_window_size = window_size

        #the recalculations
        self.median_image = self.median_filtering(self.median_filter_window_size)
        self.mineral_classification()

if __name__ == "__main__":

    from imagereader import ImageReader
    from crismimage import CRISMImage

    imr = ImageReader("HRL000040FF_07_IF183L_TRR3_BATCH_CAT_corr.img")

    img = imr.get_raw_image()

    classifier = MineralClassfier(img)

    classifier.ratioing(5, 25)

    classifier.median_filtering(17)