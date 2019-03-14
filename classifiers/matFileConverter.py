'''
Converts a .mat file to the format expected by the input file reader function
'''

import numpy
import scipy.io
import os

'''
Reads in a .mat file with the classifier data and converts
it to a .npz file that is easily read by a function in numpy.
Params: str: the path of the file that is being converted
    The expected format of the input file is one that has the data
    saved in the order Sig_s, class_id, fin, mus_s, v_s
Return: none
'''
def convert_mat_file(input_file_name):
    # gets root file name
    base_file = os.path.basename(input_file_name)
    base_name = os.path.splitext(base_file)[0]
    #os.chdir('..')
    output_path = os.path.join("..//Resources", base_name)

    # loads file as dictionary
    mat_data = scipy.io.loadmat(input_file_name)
    temp_array = []

    # move data from dictionary to array
    for x in mat_data:
        temp_array.append(mat_data[x])

    # ignore first three rows (header, version, globals)
    numpy.savez(output_path, temp_array[3], temp_array[4], temp_array[5], temp_array[6], temp_array[7])
