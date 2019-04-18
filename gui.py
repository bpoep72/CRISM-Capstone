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
from spectral import *
import spectral.io.envi as envi
from PIL import Image, ImageTk

from classifiers.imagereader import ImageReader

# default channels for hyperspectral image (usually 233, 78, 13)
RED_BASE = 233
BLUE_BASE = 78
GREEN_BASE = 13

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
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open Image File", command=self.openFile)
        self.filemenu.add_command(label="Save Image As", command=self.saveFile)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        
        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Documentation", command=self.documentation)
        self.helpmenu.add_command(label="About", command=self.about)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        
        root.config(menu=self.menubar)
        
        # create pane system
        self.paneSystem = tk.PanedWindow(root, sashrelief=tk.RAISED)
        self.paneSystem.pack(fill=tk.BOTH, expand=True)
        
        # create file directory system
        self.treeFrame = tk.Frame(root)
        #self.treeFrame.grid(row=0, column=0, sticky="n,s,e,w")
        
        self.tree = ttk.Treeview(self.treeFrame)
        self.tree.pack(expand=True, fill=tk.BOTH)
        self.tree.bind("<Double-1>", self.onDoubleClick)

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
        self.tabs.add(self.channelTab, text="Channel Display")
        
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
        
        # create frame for parameters
        self.paramTab = tk.Frame(root)
        self.tabs.add(self.paramTab, text="Parameters")
        
        # create labels, text boxes, and button for parameters
        self.medianLabel = tk.Label(self.paramTab, text="Median Filtering Window Size")
        self.medianLabel.grid(row=0, column=0)
        
        self.ratioLabel = tk.Label(self.paramTab, text="Ratio Window Size")
        self.ratioLabel.grid(row=1, column=0)
        
        self.slogsLabel = tk.Label(self.paramTab, text="Number of Highest Slogs")
        self.slogsLabel.grid(row=2, column=0)
        
        self.medianEntry = tk.Entry(self.paramTab)
        self.medianEntry.grid(row=0, column=1)
        
        self.ratioEntry = tk.Entry(self.paramTab)
        self.ratioEntry.grid(row=1, column=1)
        
        self.slogsEntry = tk.Entry(self.paramTab)
        self.slogsEntry.grid(row=2, column=1)
        
        self.paramUpdate = tk.Button(self.paramTab, text="Update", command=self.updateParam)
        self.paramUpdate.grid(row=3, column=1)

    # recursively fills in the file directory
    def process_directory(self, parent, path):
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            isdir = os.path.isdir(abspath)
            oid = self.tree.insert(parent, 'end', text=p, open=False)
            if isdir:
                self.process_directory(oid, abspath)

    def onDoubleClick(self, event):
        self.item = self.tree.selection()[0]

    def updateColor(self):
        print("updateColor")
        try:
            self.red = int(self.redEntry.get())
            self.blue = int(self.blueEntry.get())
            self.green = int(self.greenEntry.get())

            self.updateImage(self.display, self.red, self.blue, self.green)
        except:
            #TODO: Add input error message for user
            print("Input Invalid: update Color")

    def updateImage(self, display, r, g, b):
        print("change color")

        #if an image has been loaded already
        if(self.image_path != None):
        
            self.image_reader.update_image(self.image_path)
            self.image = self.image_reader.get_raw_image()
            path_to_image = self.image.get_three_channel(self.red, self.blue, self.green)
            
            self.photo = tk.PhotoImage(file=path_to_image)
            self.display.image = self.photo

            self.display.configure(image=self.display.image)

        #the only image loaded so far is the place holder image
        #TODO: maybe add a notification to load an image otherwise nothing happens here
        else:
            pass
        
    def openFile(self):
        print("open file")

        parent_path = os.path.dirname(os.path.abspath(__file__))
        
        image_path = tk.filedialog.askopenfilename(
                initialdir = os.path.join(parent_path, 'Images'),
                defaultextension = '.img',
                filetypes = [('Hyperspectral Image Files', '.img'), ('All Files', '.*')],
                title = "Open Image File"
                )

        #the instruction above returns os dependant paths make them independent of os again
        image_path = os.path.abspath(image_path)

        #incase no image is selected
        if(len(image_path) != 0):
            self.image_path = image_path
            self.updateColor()
        else:
            pass
        
    def saveFile(self):
        print("save file")
        
        self.fileName = tk.filedialog.asksaveasfilename(
                defaultextension = '.jpg',
                filetypes = [('JPEG file', '.jpg'),
                             ('GIF file', '.gif'),
                             ('PNG file', '.png'),
                             ('All Files', '.*')],
                title = "Save Image File As"
                )
        
        # obtains the short file name minus the path and the file extension
        indexName = self.fileName.rfind('/')
        self.fileName = self.fileName[indexName+1:]
        indexExt = self.fileName.rfind('.')
        self.fileExtension = self.fileName[indexExt+1:]
        
        # format only accepts "jpeg", not "jpg"
        if(self.fileExtension == "jpg"):
            self.fileExtension = "jpeg"
        
        save_rgb(self.fileName, self.hsi, [self.red, self.blue, self.green], stretch=(0, 0.9), format=self.fileExtension)

    def updateParam(self):
        # TODO: implementation
        print("Parameters Updated")

        #if an image has been loaded already
        if(self.image != None):
            try:
                #we only want to recalculate anything on the backend if anything changes that would impact the output
                if(self.median_filter_window_size != int(self.medianEntry.get())):
                    #if either of these values change we have to recalculate everything
                    if(int(self.ratioEntry.get()) != self.ratioing_window_size or self.highest_slogs != int(self.slogsEntry.get())):  
                        self.ratioing_window_size = int(self.ratioEntry.get())
                        self.highest_slogs = int(self.slogsEntry.get())
                    
                        self.classifier.update_ratioing_parameters(self.highest_slogs, self.ratioing_window_size)
                    else:
                        self.median_filter_window_size = int(self.medianEntry.get())

                        self.classifier.update_median_filtering_parameters(self.median_filter_window_size)
            # if the input was not a valid int
            except:
                #TODO: Add input error message for user
                print("Input Invalid")

        #if an image has not already been loaded
        else:
            pass
        
    def documentation(self):
        # TODO: implementation
        print("Documentation")
        
    def about(self):
        # TODO: implementation
        print("About")

    def get_default_bands(self):
        pass
        

def main():
    root = tk.Tk()
    mainGUI = GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()