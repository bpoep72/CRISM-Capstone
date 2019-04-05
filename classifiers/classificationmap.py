
'''
    This will be the format of the output of the mineral classifier so that
    it may be more easily used within the gui.
'''

from layer import Layer
import numpy

class ClassificationMap:

    def __init__(self, predicted_labels):
        
        self.predications = predicted_labels

        self.labels = numpy.unique(self.predications)

        self.layers = [None]*len(self.labels)

        self.get_map()

    '''
        Produces the layered classification map

        Params: None
        Return: None
        Side Effect: self.layers is now initialized
    '''
    def get_map(self):

        for label in range(len(self.labels)):

            layer = self.predications == self.labels[label]
            label_num = self.labels[label]
            color = self.get_color(label)

            self.layers[label] = Layer(layer, label_num, color)

    '''
        Produces evenly spaced colors for use when displaying the individual layers

        Params: int, the index of the layer
        Return: 
            NOTE: return is a 3x1 tuple
            r, int the red value
            g, int the green value
            b, int the blue value
    '''
    def get_color(self, number):

        rgb_max = 255

        max_color_val = rgb_max * 3

        spacing = int(max_color_val / len(self.labels))

        color_val = number * spacing

        # color picking "ai"

        #for red
        if(color_val > rgb_max * 1):
            r = 255
        else:
            r = color_val
        
        #for green
        if(color_val > rgb_max * 2):
            g = 255
        elif(color_val <= rgb_max * 1):
            g = 0
        else:
            g = color_val - rgb_max

        #for blue
        if(color_val > rgb_max * 3):
            b = 255
        elif(color_val <= rgb_max * 2):
            b = 0
        else:
            b = color_val - (rgb_max * 2)

        return r, g, b
        

if __name__ == "__main__":

    test_mat = numpy.random.rand(15, 15)

    classification_map = ClassificationMap(test_mat)

    print()

    

