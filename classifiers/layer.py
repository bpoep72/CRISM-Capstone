
'''
    Used within the ClassificationMap class to organizes each label
    and to assign any other helpful attributes to make display of
    classification output easier.
'''

import numpy

class Layer:

    def __init__(self, prediction_matrix, label):

        #the boolean matrix that represents the layer
        self.prediction_matrix = prediction_matrix
        
        #the label assigned by the classiifer
        self.mineral_label = label

        #the actual mineral name
        self.mineral_name = self.get_mineral_name()
        
        #the number of occurences of the label within the matrix
        self.occurences = numpy.sum(self.prediction_matrix == 1)
        
        #the color assigned to is layer
        self.color = None

        #whether the layer is currerently expected to be visible or not
        self.is_visible = False

    def get_mineral_name(self):

        name = "Mineral " + str(self.mineral_label) 

        #TODO: Ask for name list for each label

        return name