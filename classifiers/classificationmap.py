
'''
    This will be the format of the output of the mineral classifier so that
    it may be more easily used within the gui.
'''

from layer import Layer
import numpy
import matplotlib

class ClassificationMap:

    def __init__(self, predicted_labels):
        
        #the predictions from the classifier double[][]
        self.predications = predicted_labels

        #the unique predicted labels int[]
        self.labels = numpy.unique(self.predications)

        #the individial layers afer get_map is run, Layer[]
        self.layers = [None]*len(self.labels)

        self.make_map()

    '''
        Overlay the classification map onto the image

        Params: 
            .png image, the Image that is currently being used on the gui for display
    '''
    def overlay(self, image):

        #read in the image we use to display the image in the gui
        img = matplotlib.image.imread(image)

        #Add the displayed image to a plot
        matplotlib.pyplot.imshow(img)

        #for each layer see if it needs to be overlayed
        for i in range(len(layers)):
            
            if(self.layers[i].is_visible):
                

    '''
        Produces the layered classification map

        Params: None
        Return: None
        Side Effect: self.layers is now initialized
    '''
    def make_map(self):

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

        #integer spacing between each color
        spacing = int(max_color_val / len(self.labels))

        #the combined color value of this number
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

    '''
        A method designed just for testing the gui. This will generate dummy data
        formatted as output from the classifier when fed the rows, columns and a number

        Params:
            rows, int, a number of rows to generate random predicitions for
            columns, int, a number of columns to generate random predictions for
            num_labels, int, the number of labels/layers to generate
    '''
    def make_random_map(self, rows, columns, num_labels):

        combined_map = numpy.random.randint(0, num_labels, size=(rows, columns))
        
        self.labels = numpy.arange(0, 25)
        self.layers = [None]*len(self.labels)
        self.predications = combined_map

        self.make_map()
        

if __name__ == "__main__":

    test_mat = numpy.random.rand(15, 15)

    classification_map = ClassificationMap(test_mat)
    classification_map.make_random_map(310, 450, 25)

    print()

    

