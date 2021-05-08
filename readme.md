# Tracking the 3D position of the ArUco marker via Intel Realsense Depth Camera

This project detects ArUco Marker via OpenCV, extracts the marker's depth informatioin using Intel Realsense Depth Camera, and inferred the 3d coordinate of the marker.

## Files
* ArUcoGenerator.py:  Generate ArUco Marker in ./tag/tag_[ArUcoDictName]/
* RealsenseTracker.py: Tracking the 3D position of the marker
* Camera.py: The class for realsense camera control
* ArUcoDetector.py: The class for detecting ArUco marker
* TrajectoryTracker.py: The class for inferring the 3D position of the marker
* config.json: configuration file

## Installation
* Install Intel Realsense SDK 2.0 and its python wrapper
* Python 3.9 (other version should also be acceptable)
* conda install numpy
* conda install matplotlib
* pip install opencv-contrib-python

## Usage
* ArUco marker generation: set the properties *dict_to_use* and *id* in config.json, and run 'python ArUcoGenerator.py'. The program will generate the marker with corresponding id from the given dictionary, and save it to the tag folder.
* ArUco marker detection:  run 'python ArUcoDetector.py'. The program will show a window of real-time result. If property *visualize* is set true in config.json, the program will collect 3d points detected from every 20s, and plot them out. The 3d points is in the camera's coordinate system, where the origin sits in the center of the camera sensor, the x-axis directs to the right, the y-axis directs downward, and z-axis directs forward (see the SDK document for further details). All detected points are saved in *trajectory* variable of a TrajectoryTracker object. It is a dictionary object of the form like {id1: [(timestamp, x, y, z), ...], id2: ..., ...}

## configuration
You can fiddle with config.json to control the project parameters:
* dict_to_use: The ArUco Dictionary to use. Check ARUCO_DICT in ArUcoGenerator.py
* id: To specify the id of the marker that you want to generate in ArUcoGenerator.py
* visualize: visualize the result
* grey_color: the color for masking the RGB image after aligning with the depth image (no need to change)

## Reference
1. https://www.pyimagesearch.com/2020/12/21/detecting-aruco-markers-with-opencv-and-python/
2. https://github.com/IntelRealSense/librealsense/tree/master/wrappers/python/examples
3. https://github.com/IntelRealSense/librealsense/issues/2458