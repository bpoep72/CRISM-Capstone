# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 11:24:07 2019

TODO:
Include installation instructions

@author: Morcleon
"""

import os
import numpy as numpy
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import spectral.io.envi as envi
from PIL import Image, ImageTk

import webbrowser
import matplotlib

from classifiers.imagereader import ImageReader
from classifiers.classificationmap import ClassificationMap

# default channels for hyperspectral image (usually 233, 78, 13)
RED_BASE = 0
BLUE_BASE = 0
GREEN_BASE = 0

class GUI:
    def __init__(self, root):
        # initialize class variables from constants
        self.red = RED_BASE
        self.blue = BLUE_BASE
        self.green = GREEN_BASE

        #placeholders for the backend variables
        self.image_reader = ImageReader("")
        self.classifier = None
        self.image_name = 'placeholder.gif'
        self.image = None
        self.median_filter_window_size = 17
        self.highest_slogs = 5
        self.ratioing_window_size = 25
        
        # initialize root of GUI
        self.root = root
        root.title("CRISM Hyperspectral Image Display")
        
        # create menubar and menu options
        self.menubar = tk.Menu(root)
        self.fill_menu_bar()
        root.config(menu=self.menubar)
        
        # create pane system
        self.paneSystem = tk.PanedWindow(root, sashrelief=tk.RAISED, sashwidth=10)
        self.paneSystem.pack(fill=tk.BOTH, expand=True)
        
        # create file directory system
        self.treeFrame = tk.Frame(root)
        #self.treeFrame.grid(row=0, column=0, sticky="n,s,e,w")
        
        self.tree = ttk.Treeview(self.treeFrame)
        self.tree.heading('#0', text=os.path.dirname(__file__), anchor='w')
        self.tree.pack(expand=True, fill=tk.BOTH)
        self.tree.bind('<<TreeviewSelect>>', self.tree_on_click)

        #point the parent directory this file was called from
        abspath = os.path.dirname(os.path.realpath(__file__))
        #go down a directory to point at the images directory
        abspath = os.path.join(abspath, 'Images')
        tree_root_name = 'Images'
        root_node = self.tree.insert('', 'end', text=tree_root_name, open=True)
        self.process_directory(root_node, abspath)
        
        self.paneSystem.add(self.treeFrame, sticky="n,s,e,w", stretch="always")
        
        # open default image in image display
        placeholder_image_dir = os.path.join(abspath, 'placeholder.gif')
        self.photo = tk.PhotoImage(file=placeholder_image_dir)
        self.display = tk.Label(root, image=self.photo)
        self.display.image = self.photo
        #self.display.grid(row=0, column=1, sticky="n,s,e,w")
        
        self.paneSystem.add(self.display, sticky="n,s,e,w", stretch="always")
        
        # create tab system for multiple windows
        self.tabs = ttk.Notebook(root)
        #self.tabs.grid(row=0, column=2, rowspan=12, sticky="n,s,e,w")
        
        self.paneSystem.add(self.tabs, sticky="n,s,e,w", stretch="always")
        
        # create frame for channel switching
        self.channelTab = tk.Frame(root)
        self.fill_channel_tab()
        self.tabs.add(self.channelTab, text="Channel Display")
        
        # create frame for parameters
        self.paramTab = tk.Frame(root)
        self.fill_params_tab()
        self.tabs.add(self.paramTab, text="Parameters")

        #classification tab
        self.classifierTab = tk.Frame(root)
        self.fill_classifier_tab()
        self.tabs.add(self.classifierTab, text="Classification")

    # recursively fills in the file directory
    def process_directory(self, parent, path):
        for p in os.listdir(path):
            abspath = os.path.join(path, p)

            #determine if a file is .img
            split_path = abspath.split('.')
            is_img = bool(split_path[-1] == 'img')

            #also leave out directories for now as they are too complicated to add
            if(is_img and not os.path.isdir(abspath)):
                self.tree.insert(parent, 'end', text=p, open=False)

    def fill_classifier_tab(self):
        if(self.image_name != 'placeholder.gif'):
            self.startClassifierButton = tk.Button(self.classifierTab, text="Start Classifier")
            self.startClassifierButton.pack(side="top", fill="x")
            
            self.canvas = tk.Canvas(self.classifierTab, borderwidth=0, background="#F0F0F0")
            self.frame = tk.Frame(self.canvas)
            self.vsb = tk.Scrollbar(self.classifierTab, orient="vertical", command=self.canvas.yview)
            self.canvas.configure(yscrollcommand=self.vsb.set)
            
            self.vsb.pack(side="right", fill="y")
            self.canvas.pack(side="left", fill="both", expand=True)
            self.canvas.create_window((2,12), window=self.frame, anchor="nw", tags="self.frame")
            self.frame.bind("<Configure>", self.on_frame_configure)
            
            test_mat = numpy.random.rand(1)

            path_to_image = os.path.dirname(__file__)
            path_to_image = os.path.join(path_to_image, 'display.png')
            self.cl = ClassificationMap(test_mat, path_to_image)
            
            self.mineralArray = [] #TODO: ?
            self.mineralButtonArray = [] #TODO: ?
            
            for i in range(0, len(self.cl.layers)):
                self.make_mineral(i)

    '''
        For each mineral discovered by the classifier we need a widget to toggle the visibility
        by use a radio button and a label to identify the mineral
    '''
    def make_mineral(self, index):
        # creates the label and radio button
        tempMineral = tk.Label(self.frame, text=self.cl.layers[index].mineral_name)
        tempMineral.grid(row=index*3, column=0, rowspan=2)
        tempMineralButton = tk.IntVar()
        tempYes = tk.Radiobutton(self.frame, text="Yes", variable=tempMineralButton, value=1, command=self.update_classifier)
        tempYes.grid(row=index*3, column=1)
        tempNo = tk.Radiobutton(self.frame, text="No", variable=tempMineralButton, value=0, command=self.update_classifier)
        tempNo.grid(row=index*3+1, column=1)
        
        # blank label for spacing
        tk.Label(self.frame, text="").grid(row=index*3+2, column=0, columnspan=2)
        
        # puts the items within the array
        self.mineralArray.append(tempMineral)
        self.mineralButtonArray.append(tempMineralButton)
    
    # resets scroll region to encompass entire frame
    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def update_classifier(self):
        pass

    def fill_menu_bar(self):

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open Image File", command=self.openFile)
        self.filemenu.add_command(label="Save Image As", command=self.saveFile)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        
        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Documentation", command=self.documentation)
        self.helpmenu.add_command(label="About", command=self.about)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

    def fill_channel_tab(self):

        # create labels, text boxes, and button for channel switching
        redLabel = tk.Label(self.channelTab, text="Red: ")
        redLabel.grid(row=0,column=0)
        
        blueLabel = tk.Label(self.channelTab, text="Blue: ")
        blueLabel.grid(row=1,column=0)
        
        greenLabel = tk.Label(self.channelTab, text="Green: ")
        greenLabel.grid(row=2,column=0)
        
        self.redEntry = tk.Entry(self.channelTab)
        self.redEntry.insert(0, self.red)
        self.redEntry.grid(row=0,column=1)
        
        self.blueEntry = tk.Entry(self.channelTab)
        self.blueEntry.insert(0, self.blue)
        self.blueEntry.grid(row=1,column=1)
        
        self.greenEntry = tk.Entry(self.channelTab)
        self.greenEntry.insert(0, self.green)
        self.greenEntry.grid(row=2,column=1)
        
        self.colorUpdate = tk.Button(self.channelTab, text="Apply Channels", command=self.updateColor)
        self.colorUpdate.grid(row=3,column=1)

    def fill_params_tab(self):
        # create labels, text boxes, and button for parameters
        medianLabel = tk.Label(self.paramTab, text="Median Filtering Window Size")
        medianLabel.grid(row=0, column=0)
        
        ratioLabel = tk.Label(self.paramTab, text="Ratio Window Size")
        ratioLabel.grid(row=1, column=0)
        
        slogsLabel = tk.Label(self.paramTab, text="Number of Highest Slogs")
        slogsLabel.grid(row=2, column=0)
        
        self.medianEntry = tk.Entry(self.paramTab)
        self.medianEntry.insert(0, self.median_filter_window_size)
        self.medianEntry.grid(row=0, column=1)
        
        self.ratioEntry = tk.Entry(self.paramTab)
        self.ratioEntry.insert(0, self.ratioing_window_size)
        self.ratioEntry.grid(row=1, column=1)
        
        self.slogsEntry = tk.Entry(self.paramTab)
        self.slogsEntry.insert(0, self.highest_slogs)
        self.slogsEntry.grid(row=2, column=1)

        label = tk.Label(self.paramTab, text="Median Filtering Mode:")
        label.grid(row=3, column=0)

        modes = [('Mirror', 0),
                 ('Truncate', 1),
                ]

        #populate with radio buttons
        for i in range(len(modes)):
            b = tk.Radiobutton(self.paramTab, text=modes[i][0], value=modes[i][1])
            #the default
            if(i == 0):
                b.select()
            b.grid(columnspan=2, row=(4 + i) )
        
        self.paramUpdate = tk.Button(self.paramTab, text="Update", command=self.updateParam)
        self.paramUpdate.grid(row=(4 + len(modes)) + 2, columnspan=3)


    '''
        Get the Image that was clicked when it is clicked inside the tree and open the image

        This is a prime example of legacy code that you shouldn't touch.
    '''
    def tree_on_click(self, event):
        #the events are weirdly named 'I<some #>' get the number and add 1 to it to get the image that
        #was selected from within the directory
        clicked = self.tree.selection()[0]
        
        #remove the I
        clicked = clicked[1:]
        #cast to int
        clicked = int(clicked)
        clicked -= 2

        #the parent directory of this file
        parent = os.path.dirname(__file__)
        #the parent of the default images directory
        parent = os.path.join(parent, 'Images')

        directory_list = os.listdir(parent)
        image_list = []

        #remove the entries in that are not .img files
        for file_name in directory_list:
            #those conditions return true if the extension is the given string otherwise 0
            split_name = file_name.split('.')
            if(split_name[-1] == 'img'):
                image_list.append(file_name)

        #if clicked is out of the expected bounds do nothing
        if(clicked > len(image_list) - 1 or clicked < 0):
            pass
        #otherwise load the image
        else:
            self.image_name = image_list[clicked]
            self.image_path = os.path.join(parent, image_list[clicked])
            self.updateImage()

    '''
        Get the default bands from the image reader and set the neccasary attributes
        to assign the current state of the GUI to use these bands.
    '''
    def get_default_bands(self):

        #get bands from the image reader
        bands = self.image_reader.default_bands

        #set the class attributes to match the bands from the above method call
        self.red = bands[0]
        self.blue = bands[1]
        self.green = bands[2]

        #update the tk.Entry fields
        self.redEntry.delete(0, tk.END)
        self.redEntry.insert(0, self.red)

        self.blueEntry.delete(0, tk.END)
        self.blueEntry.insert(0, self.blue)

        self.greenEntry.delete(0, tk.END)
        self.greenEntry.insert(0, self.green)
        
    '''
        Update the color attributes based in the input in the fields under the
        Channel Display tab
    '''
    def updateColor(self):

        try:
            r = int(self.redEntry.get())
            g = int(self.greenEntry.get())
            b = int(self.blueEntry.get())

            max_band_number = len(self.image.bands)
            assert r < max_band_number and g < max_band_number and b < max_band_number
            assert r >= 0 and g >= 0 and b >= 0
            self.red = int(self.redEntry.get())
            self.blue = int(self.blueEntry.get())
            self.green = int(self.greenEntry.get())

            #if an image has actually been loaded
            if(self.image_name != 'placeholder.gif'):
                #get the image from the imagereader
                self.image = self.image_reader.get_raw_image()

                #have imagereader update the display.png, returning the path to the image
                path_to_image = self.image.get_three_channel(self.red, self.blue, self.green)
                
                #render the image pointed to the the path_to_image
                self.photo = tk.PhotoImage(file=path_to_image)
                self.display.image = self.photo
                self.display.configure(image=self.display.image)
        #if coercion failed
        except AttributeError:
            messagebox.showerror("Error", "An image has not been loaded")
        except AssertionError:
            messagebox.showerror("Error", "Valid range for color channels is between 0 and 349")

    '''
        Update the display of the image based on the 
    '''
    def updateImage(self):

        #update the path image reader points at
        self.image_reader.update_image(self.image_path)

        #get the default bands
        self.get_default_bands()

        #get the image from the imagereader
        self.image = self.image_reader.get_raw_image()

        #have imagereader update the display.png, returning the path to the image
        path_to_image = self.image.get_three_channel(self.red, self.blue, self.green)
        
        #render the image pointed to the the path_to_image
        self.photo = tk.PhotoImage(file=path_to_image)
        self.display.image = self.photo
        self.display.configure(image=self.display.image)

    '''
        Open a file using a file dialog. Record the results then do 
        what is neccasary to display the image. We need the image to
        have .img extension. AND THE .HDR FILE MUST BE IN THE SAME
        DIRECTORY
    '''
    def openFile(self):
        try:
            parent_path = os.path.dirname(os.path.abspath(__file__))
            
            image_path = tk.filedialog.askopenfilename(
                    initialdir = os.path.join(parent_path, 'Images'),
                    defaultextension = '.img',
                    filetypes = [('Hyperspectral Image Files', '.img')],
                    title = "Open Image File"
                    )

            #the instruction above returns os dependant paths make them independent of os again
            image_path = os.path.abspath(image_path)
            #update the current image name
            self.image_name = os.path.split(image_path)[1]

            #Only update if the an image was selected
            if(len(image_path) != 0):
                self.image_path = image_path
                self.updateImage()
        except:
            messagebox.showerror("Error", "The header file could not be found. Make sure it is in the same directory as the image.")
    
    '''
        Save the current view of the image out to a place specfied by
        a file dialog with the name that is given.
    '''
    def saveFile(self):
        
        fileName = tk.filedialog.asksaveasfilename(
                defaultextension = '.png',
                filetypes = [('PNG file', '.png'),
                             ('JPEG file', '.jpg')],
                title = "Save Image File As",
                initialfile="image"
                )

        #read in the image we use to display the image in the gui
        img = matplotlib.image.imread('display.png')
        #save it out using the name and extension we were given by asksaveasfilename
        matplotlib.image.imsave(fileName, img)

    def updateParam(self):
        #if an image has been loaded already
        if(self.image != 'placeholder.gif'):
            try:
                #we only want to recalculate anything on the backend if anything changes that would impact the output

                #if median filtering changed
                if(self.median_filter_window_size != int(self.medianEntry.get())):
                    #if median filtering and rationg or highest slogs changed
                    if(int(self.ratioEntry.get()) != self.ratioing_window_size or self.highest_slogs != int(self.slogsEntry.get())):
                        print('everything rerun')

                        self.ratioing_window_size = int(self.ratioEntry.get())
                        self.highest_slogs = int(self.slogsEntry.get())
                        self.median_filter_window_size = int(self.medianEntry.get())
                    
                        self.classifier.update_ratioing_parameters(self.highest_slogs, self.ratioing_window_size)
                    #only median filtering changed
                    else:
                        print('only median filtering')
                        self.median_filter_window_size = int(self.medianEntry.get())
                        
                        self.classifier.update_median_filtering_parameters(self.median_filter_window_size)

                #if median filtering did not change
                else:
                    #if ratioing or highest slogs changed
                    if(int(self.ratioEntry.get()) != self.ratioing_window_size or self.highest_slogs != int(self.slogsEntry.get())):
                        print('everything rerun')

                        self.ratioing_window_size = int(self.ratioEntry.get())
                        self.highest_slogs = int(self.slogsEntry.get())
                        self.median_filter_window_size = int(self.medianEntry.get())
                    
                        self.classifier.update_ratioing_parameters(self.highest_slogs, self.ratioing_window_size)
                    #nothing changed
                    else:
                        pass

            # if the input was not a valid int
            except:
                messagebox.showerror("Error", "All values must be positive integers. The window sizes must be odd. The maximum number of slogs must be less than 50.")

        #if an image has not already been loaded
        else:     
            messagebox.showerror("Error", "An image has not been loaded")

    '''
        Method called by reselection of the mode under the parameters tab of the GUI specific
        to the mode radio button.

        Params:
            mode, int the mode that we want to switch to
    '''
    def update_median_filter_mode(self, mode):

        self.classifier.update_median_filtering_mode(mode)
        
    def documentation(self):

        #open the git page in a new browser tab if possible
        webbrowser.open('https://github.iu.edu/bmpoeppe/CRISMCapstonePython/#how-to-use-the-application', new=2)
        
    def about(self):
        
        webbrowser.open('https://github.iu.edu/bmpoeppe/CRISMCapstonePython/blob/master/README.md#about', new=2)
        
if __name__ == "__main__":

    import os
    root = tk.Tk()

    #maximize the window based on the os, 'nt' = windows
    if(os.name == 'nt'):
        root.state('zoomed')
    else:
        root.attributes('-zoomed', True)

    GUI(root)
    root.mainloop()