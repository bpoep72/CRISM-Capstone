
'''
    This will be the format of the output of the mineral classifier so that
    it may be more easily used within the gui.
'''

import numpy
import matplotlib
import PIL

if __package__ is '':

    #module is at the root of /classifiers/
    import sys
    from os import path
    
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    
    from layer import Layer

else:

    #module is at the root of the project
    from classifiers.layer import Layer

class ClassificationMap:

    def __init__(self, predicted_labels, original_image_path):

        self.distinct_colors = [
        "#FFFF00", "#1CE6FF", "#FF34FF", "#FF4A46", "#008941", "#006FA6", "#A30059", "#7ED379",
        "#FFDBE5", "#7A4900", "#0000A6", "#63FFAC", "#B79762", "#004D43", "#8FB0FF", "#997D87",
        "#5A0007", "#809693", "#FF0000", "#1B4400", "#4FC601", "#3B5DFF", "#4A3B53", "#FF2F80",
        "#61615A", "#BA0900", "#6B7900", "#00C2A0", "#FFAA92", "#FF90C9", "#B903AA", "#D16100",
        "#DDEFFF", "#000035", "#7B4F4B", "#A1C299", "#300018", "#0AA6D8", "#013349", "#00846F",
        "#372101", "#FFB500", "#C2FFED", "#A079BF", "#CC0744", "#C0B9B2", "#C2FF99", "#001E09",
        "#00489C", "#6F0062", "#0CBD66", "#EEC3FF", "#456D75", "#B77B68", "#7A87A1", "#788D66",
        "#885578", "#FAD09F", "#FF8A9A", "#D157A0", "#BEC459", "#456648", "#0086ED", "#886F4C",

        "#34362D", "#B4A8BD", "#00A6AA", "#452C2C", "#636375", "#A3C8C9", "#FF913F", "#938A81",
        "#575329", "#00FECF", "#B05B6F", "#8CD0FF", "#3B9700", "#04F757", "#C8A1A1", "#1E6E00",
        "#7900D7", "#A77500", "#6367A9", "#A05837", "#6B002C", "#772600", "#D790FF", "#9B9700",
        "#549E79", "#201625", "#72418F", "#BC23FF", "#99ADC0", "#3A2465", "#922329", "#012C58"
        "#5B4534", "#FDE8DC", "#404E55", "#0089A3", "#CB7E98", "#A4E804", "#324E72", "#6A3A4C",
        "#83AB58", "#001C1E", "#D1F7CE", "#004B28", "#C8D0F6", "#A3A489", "#806C66", "#222800",
        "#BF5650", "#E83000", "#66796D", "#DA007C", "#FF1A59", "#8ADBB4", "#1E0200", "#5B4E51",
        "#C895C5", "#320033", "#FF6832", "#66E1D3", "#CFCDAC", "#D0AC94", "#00FF00", "#FF0000"
        ]
        
        #the predictions from the classifier double[][]
        self.predictions = predicted_labels

        #the image without any overlay
        self.original_image = None
        self.fetch_image(original_image_path)

        #what we currently believe the display of the 
        self.current_view = self.original_image

        #the unique predicted labels int[]
        self.labels = numpy.unique(self.predictions)

        #the individial layers afer get_map is run, Layer[]
        self.layers = [None]*len(self.labels)

        self.make_map()


    '''
        Fetches the original image so that it is perserved

        Params: str, the path to the original image
        Returns: numpy[][][4] array, the original image as an array
    '''
    def fetch_image(self, path):

        self.original_image = matplotlib.pyplot.imread(path)
        self.current_view = self.original_image

    '''
        Overlay the classification map onto the image

        Params: None
        Returns:
            numpy[][][3], representing the image with the layers overlayed
        
    '''
    def overlay(self):

        self.current_view = self.original_image * 255

        #for each layer generate an image matrix for that layer
        for i in range(len(self.layers)):
            
            #only make the layer if it is currently visible
            if(self.layers[i].is_visible):

                #we need to generate the image we want to blend
                image = numpy.zeros((self.predictions.shape[0], self.predictions.shape[1], 4))

                #get the bool prediction matrix for the layer we are looking at 
                prediction_matrix = self.layers[i].prediction_matrix

                #set the rgb values
                image[:, :, 0] = prediction_matrix * self.layers[i].color[0]
                image[:, :, 1] = prediction_matrix * self.layers[i].color[1]
                image[:, :, 2] = prediction_matrix * self.layers[i].color[2]

                #zero out the places in the image where we are about to add the layer
                self.current_view[:, :, 0] = numpy.multiply(self.current_view[:, :, 0], numpy.invert(prediction_matrix))
                self.current_view[:, :, 1] = numpy.multiply(self.current_view[:, :, 1], numpy.invert(prediction_matrix))
                self.current_view[:, :, 2] = numpy.multiply(self.current_view[:, :, 2], numpy.invert(prediction_matrix))

                #add the layer
                self.current_view = numpy.add(self.current_view, image)
                self.current_view = self.current_view.astype(int)

        return self.current_view

    '''
        Produces the layered classification map

        Params: None
        Return: None
        Side Effect: self.layers is now initialized
    '''
    def make_map(self):

        for label in range(len(self.labels)):

            layer = self.predictions == self.labels[label]
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

        hex_value = self.distinct_colors[number]

        #remove the Ox
        hex_value = hex_value.split('#')[1]

        #pad with 0's if needed
        hex_value = hex_value.ljust(6, '0')

        #convert back to decimal
        r = int(hex_value[0:2], 16)
        g = int(hex_value[2:4], 16)
        b = int(hex_value[4:6], 16)

        return r, g, b

    '''
        A method designed just for testing the gui. This will generate dummy data
        formatted as output from the classifier when fed the rows, columns and a number

        Params:
            rows, int, a number of rows to generate random predictions for
            columns, int, a number of columns to generate random predictions for
            num_labels, int, the number of labels/layers to generate
    '''
    def make_random_map(self, rows, columns, num_labels):

        combined_map = numpy.random.randint(0, num_labels, size=(rows, columns))
        
        self.labels = numpy.arange(0, num_labels)
        self.layers = [None]*len(self.labels)
        self.predictions = combined_map

        self.make_map()
        

if __name__ == "__main__":

    from imagereader import ImageReader
    import os
    import matplotlib

    test_mat = numpy.random.rand(1)

    imr = ImageReader("HRL000040FF_07_IF183L_TRR3_BATCH_CAT_corr.img")

    img = imr.get_raw_image()

    #get the path to the image
    path = os.path.abspath(__file__)
    path = os.path.split(path)[0]
    path = os.path.split(path)[0]
    path = os.path.join(path, 'display.png')

    classification_map = ClassificationMap(test_mat, path)
    classification_map.make_random_map(480, 320, 1)

    classification_map.overlay()

    matplotlib.pyplot.imshow(classification_map.current_view)
    matplotlib.pyplot.show()

    

