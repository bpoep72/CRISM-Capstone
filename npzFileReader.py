'''
Reads in the classifier file
'''

import numpy

class DataReader:
    def __init__(self, Sig_s, class_id, fin, mu_s, v_s):
        self.Sig_s = Sig_s
        self.class_id = class_id
        self.fin = fin
        self.mu_s = mu_s
        self.v_s = v_s

'''
Loads in the classifier data from a .npz file
Params: str: the path of the file that is being read
    The expected format of the input file is one that has the data 
    saved in the order Sig_s, class_id, fin, mu_s, v_s
Return: The classifier object
'''
def read_file(input_file_name):
    file_object = numpy.load(input_file_name)
    Sig_s = file_object['arr_0']
    class_id = file_object['arr_1']
    fin = file_object['arr_2']
    mu_s = file_object['arr_3']
    v_s = file_object['arr_4']
    classifier = DataReader(Sig_s, class_id, fin, mu_s, v_s)
    return classifier