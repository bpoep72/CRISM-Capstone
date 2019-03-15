

import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from classifiers.npzFileReader import DataReader
import math
import scipy.special.gammaln
import numpy as np

class Two_Layer_Gmm:

    def __init__(self, data):
        #inputs
        self.data = data

        #outputs
        self.ypred = None
        self.aa = None
        self.loglik = None

    def test(self):

        #[ncl d] = size(mu_s)

        pi_constant = (d / 2) * math.log(math.pi)
        g1_pc = scipy.special.gammaln((.5: .5: max(self.data.v_s) + d) #not sure this will work
        n = len(self.data.X[0])
        loglik = np.zeros((n, ncl))
        
        #do the thing
        for i in range(ncl):
            v = X - self.data.mu_s[i] #check this
            chsig = np.linalg.cholesky( Sig_s(:, :, i) ) #need to use python matrix access
            


if __name__ == "__main__":
    
    import npzFileReader
    import os

    parent_directory = os.path.join(os.path.dirname(__file__), '..')

    resource_file = os.path.join(parent_directory, 'Resources', 'neutral_pixel_classifier.npz')

    data = npzFileReader.read_file(resource_file)

    print(data.mu_s)
        