# Rig Vadar Facial Performance Analysis
This tool is built using [Autodesk FBX Python SDK](https://www.autodesk.com/developer-network/platform-technologies/fbx-sdk-2020-0) 
and provides a GUI to convert Rig Vadar format text files into FBX files. 

## Features
### Filepath specification
The filepath specification define locations on disk, from where to read and write data.
##### Vadar file

The text field, labelled `Vadar file` should be used to specify a path to the 
source file, intended for FBX conversion. The button next to it, labelled `Open`,
can be used to explore directories for the source file. On filling in source file path,
the tool verifies if the file exists and is valid. In case the file exists and is valid,
the `Convert` button gets enabled, otherwise the tool raises a corresponding error message. i.e.
```
Vadar file not found!
```
or 
```
Invalid vadar file!
```
 
##### Audio file
The tool allows `.wav` audio to be embedded in the fbx file,
however, this practice is discouraged. Only 
[Autodesk Maya](https://www.autodesk.com/products/maya) fully supports audio embedded FBX files,
and it will still raise a warning on load. 
[Autodesk FBX Review](https://www.autodesk.com/products/fbx/fbx-review) and 
[Autodesk 3DS Max](https://www.autodesk.com/products/3ds-max) ignore the audio,
and load only animation data.
[Blender3D](https://www.blender.org/) is unable to handle embedded audio, and will not load such files.

The text field, labelled `Audio file` should be used to specify a path to the 
`.wav` file, intended for embedding. The button next to it, labelled `Open`,
can be used to explore directories for the audio file. On filling in the audio file path
the tool will provide the following warning:
```
Audio files are only supported by Autodesk Maya
```
##### Output file
The text field, labelled `Output file` should be used to specify the output file name. 
The button next to it, labelled `Open`, can be used to explore directories and replace an
existing FBX file.

### Mask options
Specifies options for track points.
##### Rotation
Defines the initial rotation of mask (i.e. all track points) in degrees. 
It is useful in aligning a mask to face front of the camera. 
The tool defaults to: `X=0°`, `Y=180°`, `Z=180°`.
##### Apply Position
If checked, applies `Mask Position Data` from the vadar file to root node. 
Defaults to `unchecked`.
##### Marker Scale
Scales the track point markers. Defaults to `1.0`.
##### Root Scale
Scales the root marker (named after the loaded vadar file), and the rotation marker.
Defaults to `3.0`.
##### Marker Prefix
Defines prefix 

### Scene options
Specifies scene options for the export FBX file.
##### Frame Rate
The float field, labelled `Frame Rate` defines the animation fps. Default value is set to
30 fps, and is updated to match value of key `Units Per Second` from a valid vadar
file. This value can be changed manually, if desired.
##### Up Vector
The combo box, labelled `Up Vector` defines the up axis of the generated fbx.
appended to markers in the FBX file. Useful in case FBX files have to 
be merged.

### Conversion
The button, labelled `Convert` is used to initiate conversion process. 
A progress bar shows the conversion progress, and a success message is displayed on completion.

## Project Build
The tool is built using [Autodesk FBX Python SDK](https://www.autodesk.com/developer-network/platform-technologies/fbx-sdk-2020-0) with the python 2.7 build.
[Visual Studio Python IDE](https://visualstudio.microsoft.com/vs/features/python/) can be used to build this project.
### Steps
- Open project directory `fbx_conversion` in visual studio.
- Set the python interpreter to `Python 2.7`. Make sure it is selected as default interpreter.
- Install python libraries from `requirements.txt`. Visual studio should prompt you with a message to install
dependencies from requirements.txt on its own; if not, then follow instructions from 
[here](https://docs.microsoft.com/en-us/visualstudio/python/managing-required-packages-with-requirements-txt?view=vs-2019).
- Run the `main.py` script to verify everything is set up properly, it should launch the app.
- In order to change the valid file identifiers, modify the `VALID_HEADERS` list in 
`./src/text_to_fbx.py`. The default value of list is:
```python
VALID_HEADERS = ["Rig Vadar Facial Performance Analysis",]
```
As an example, we can add another valid file identifier by appending to list:
```python
VALID_HEADERS = ["Rig Vadar Facial Performance Analysis",
                 "Rig Vadar Facial Performance Analysis 2"]
```
It is worth mention here, that spacing between words is removed when validating a
rig vadar file. So the following list will have the same effect as the previous one:
```python
VALID_HEADERS = ["RigVadarFacialPerformanceAnalysis",
                 "RigVadarFacialPerformanceAnalysis2"]
```

##### Windows
The goal in windows build it to create an installer file, for this, we will use [Inno Setup Compiler](https://jrsoftware.org/isdl.php).
- Run the `setup.py` script, in a windows system. It will create the tool directory `./build/dist/TxtToFbx`.
- To package the directory, open and run `./compile_script_windows.iss` with Inno Setup Compiler. 
This should Create the setup file `./build/dist/TBX Setup.exe`.

##### Linux
- Run the `setup.py` script, in a linux system. The script contains code that creates
an AppImage file `./build/dist/TBX-x86_64.AppImage`. This file should be executable on 
any linux system.
     
