# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 11:24:07 2019

TODO:
Include installation instructions

@author: Morcleon
"""

import os
import tkinter as tk
from tkinter import filedialog, ttk
import spectral.io.envi as envi
from PIL import Image, ImageTk

import webbrowser
import matplotlib

from classifiers.imagereader import ImageReader

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
        self.paneSystem = tk.PanedWindow(root, sashrelief=tk.RAISED)
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

            #leave out file headers to eliminate redundancy
            is_header = bool(len(abspath.split('.hdr')) - 1)

            #also leave out directories for now as they are too complicated to add
            if(not is_header and not os.path.isdir(abspath)):
                self.tree.insert(parent, 'end', text=p, open=False)

    def fill_classifier_tab(self):
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
        self.redLabel = tk.Label(self.channelTab, text="Red: ")
        self.redLabel.grid(row=0,column=0)
        
        self.blueLabel = tk.Label(self.channelTab, text="Blue: ")
        self.blueLabel.grid(row=1,column=0)
        
        self.greenLabel = tk.Label(self.channelTab, text="Green: ")
        self.greenLabel.grid(row=2,column=0)
        
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
        self.medianLabel = tk.Label(self.paramTab, text="Median Filtering Window Size")
        self.medianLabel.grid(row=0, column=0)
        
        self.ratioLabel = tk.Label(self.paramTab, text="Ratio Window Size")
        self.ratioLabel.grid(row=1, column=0)
        
        self.slogsLabel = tk.Label(self.paramTab, text="Number of Highest Slogs")
        self.slogsLabel.grid(row=2, column=0)
        
        self.medianEntry = tk.Entry(self.paramTab)
        self.medianEntry.insert(0, self.median_filter_window_size)
        self.medianEntry.grid(row=0, column=1)
        
        self.ratioEntry = tk.Entry(self.paramTab)
        self.ratioEntry.insert(0, self.ratioing_window_size)
        self.ratioEntry.grid(row=1, column=1)
        
        self.slogsEntry = tk.Entry(self.paramTab)
        self.slogsEntry.insert(0, self.highest_slogs)
        self.slogsEntry.grid(row=2, column=1)
        
        self.paramUpdate = tk.Button(self.paramTab, text="Update", command=self.updateParam)
        self.paramUpdate.grid(row=3, column=1)

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
            #those conditions return true if the extension is the given string otherwise 0 #TODO: remove non img files
            if(bool( len(file_name.split('.img'))-1 ) and len(file_name.split('.img')[1]) ):
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

            if( r > max_band_number or g > max_band_number or b > max_band_number): #TODO: bound check
                if( r > 0 or g > 0 or b > 0):
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
        except:
            #TODO: Add input error message for user
            print("Input Invalid: update Color")

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

        parent_path = os.path.dirname(os.path.abspath(__file__))
        
        image_path = tk.filedialog.askopenfilename(
                initialdir = os.path.join(parent_path, 'Images'),
                defaultextension = '.img',
                filetypes = [('Hyperspectral Image Files', '.img'), ('All Files', '.*')],
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
    
    '''
        Save the current view of the image out to a place specfied by
        a file dialog with the name that is given.
    '''
    def saveFile(self):
        
        fileName = tk.filedialog.asksaveasfilename(
                defaultextension = '.png',
                filetypes = [('PNG file', '.png'),
                             ('JPEG file', '.jpg'),
                             ('GIF file', '.gif'),
                             ('All Files', '.*')],
                title = "Save Image File As",
                initialfile="image"
                )

        #read in the image we use to display the image in the gui
        img = matplotlib.image.imread('display.png')
        #save it out using the name and extension we were given by asksaveasfilename
        matplotlib.image.imsave(fileName, img)

    def updateParam(self):
        # TODO: implementation
        print("Parameters Updated")

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
                #TODO: Add input error message for user
                print("Input Invalid")

        #if an image has not already been loaded
        else:
            #TODO: Error message about needing to load an image
            pass
        
    def documentation(self):

        #open the git page in a new browser tab if possible
        webbrowser.open('https://github.iu.edu/bmpoeppe/CRISMCapstonePython/#how-to-use-the-application', new=2)
        
    def about(self):
        # TODO: implementation
        print("About")

        

def main():
    root = tk.Tk()
    GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()