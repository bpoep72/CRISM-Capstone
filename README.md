# CRISMCapstonePython

<h2>Dependancies</h2>

<h3>Packaged with Anaconda</h3>
<ul>
  <li>NumPy</li>
  <li>matlibplot</li>
  <li>webbrowser</li>
  <li>Tkinter</li>
  <li>Pillow (PIL)</li>
</ul>
<h3>NOT Packaged with Anaconda</h3>
<ul>
  <li>Spectral python (SPy)</li>
    <ul>
      <li><a>http://www.spectralpython.net/</a></li>
      <li>To install : conda install -c conda-forge spectral </li>
    </ul>
  <li>Scipy 1.2.1 or later</li>
    <ul>
      <li>Anaconda is packaged with Scipy 1.1.0 as of 3/17/2019</li>
      <li>To install : conda install scipy=1.2.1 </li>
      <li>Alternatively just tell Anaconda to look for the most recent version of the package from the gui package manager (anaconda-navigator)</li>
    </ul>
</ul>

<h2>Getting Started</h2>
  <ul><h3>Steps To Install The Application</h3>
    <li>Download and install Anaconda - <a href="https://docs.anaconda.com/anaconda/navigator/">Instructions</a></li>
    <li>Ensure that Your PYTHONPATH now uses anaconda</li>
      <ul>
        <li>Windows type: where python</li>
        <li>Expect: {A windows path}\anaconda3\{location of python executable}</li>
        <br>
        <li>Debian Linux type: which python</li>
        <li>Expect: /home/{username}/anaconda3/python</li>
        <br>
        <li>NOTE: if the execution environment for python is not the anaconda install it is probable to fail</li>
      </ul>
    <li>Look under the Dependancies NOT packaged with anaconda section above</li>
      <ul>
        <li>Anything listed there must be installed for the application to function</li>
      </ul>
    <li>Clone this repository somewhere local</li>
    <li>Locate {ADD MAIN GUI FILE HERE PLEASE} within {PARENT FOLDER}</li>
    <li>Run the above file using CLI or Double Click</li>
  </ul>
  <br>
  <ul><h3>Steps To Run Unit Tests</h3>
    <li>Ensure that Anaconda is installed and PYTHONPATH is correct (see above)</li>
    <li>Locate a copy of the image file HRL000040FF_07_IF183L_TRR3_BATCH_CAT_corr.img and its .hdr file</li>
    <li>Put this image into the Images Directory</li>
    <li>Type 'pytest' into the terminal at the directory level of the project</li>
  </ul>
  <br>
  <ul><h3>Recommended For Development</h3>
    <li>
      <div>
            Anaconda comes with a GUI interface to launch a collection of Development environments. This is known as Anaconda Navigator. We recommend using one of their supplied IDES, i.e. Spyder or Vscode, this will ensure that the execution environment is using Anaconda and not some other install and will match the way the majority of the code base was created up to now. This is not required.
      </div>
    </li>
  </ul>
  
<h2>Possible features for the future</h2>
  <ul>
    <li>progress bar</li>
    <li>per pixel value information as a hover over on the image</li>
    <li>per band information panel</li>
    <li>optimized ratioing</li>
    <li>save and load classification option</li>
    <li>ability to have multiple images open at once</li>
    <li>ability to see the model files in application</li>
  </ul>
<h2>How to Use The Application</h2>
  <ul>
    <li><h3 style="text-decoration:underline">Opening Images</h3></li>
    <ul>
      <h4>Option 1: File Dialog</h4>
      <li>Hover over the File option in the top bound options menubar</li>
      <li>In the drop down select Open Image File</li>
      <li>Select an image that is inside the default image folder Images or anywhere on your machine (To pick an image it must have the
      .img extension and the .hdr file MUST be the same directory)</li>
      <li>Click Open File</li>
      <li>The image should load and should be displayed using its default bands</li>
    </ul>
    <ul>
      <h4>Option 2: File Tree</h4>
      <li>The file tree is set to show all .img files in this project's default Image folder ( ./Images/ )</li>
      <li>To load a file that is inside the default Image folder click the image name</li>
      <li>The image should load and should be displayed using its default bands</li>
    </ul>
    <li><h3 style="text-decoration:underline">Saving Images</h3></li>
    <ul>
      <li>Hover over the File option in the top bound options menubar</li>
      <li>In the drop down select Save Image As</li>
      <li>In the file dialog navigate to where you want to save the image</li>
      <li>Change the name of the image if desired</li>
      <li>Press Save</li>
    </ul>
    <li><h3 style="text-decoration:underline">Changing Bands</h3></li>
    <ul>
      <li>Locate the Channel Display tab on the right of the application</li>
      <li>If it is not open click it</li>
      <li>In the three fields the channel that will represent the red, green and blue channels can be replaced by your desired bands</li>
      <li>Once you are happy with the selected bands click update. There may be a slight pause then the image should be updated to display the updated image using the input bands.</li>
    </ul>
    <li><h3 style="text-decoration:underline">Changing Rationing/Median Filtering Parameters</h3></li>
    <ul>
      <li>Locate the Parameters tab on the right of the application</li>
      <li>If it is not open click it</li>
      <li>In the three fields the median filtering window size, ratioing window size and the number of highest slogs to use can all be changed to the desired values. (NOTE: the window size variables must both be odd number currently this is not checked before processing.)</li>
      <li>Once you are happy with the selection click Update. Then the classifier will work to reclassify all the pertainate data. This can take quite some time as everything is calculated from scratch in this application (makes it taste better. heh. I need sleep).</li>
    </ul>

  </ul>

<h2>Known Issues</h2>


<h2>Program Flow</h2>

<h2>About</h2>
