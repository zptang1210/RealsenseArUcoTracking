# Tracking the 3D position of the ArUco marker via Intel Realsense Camera

This project detects ArUco Marker via OpenCV, extracts the marker's depth informatioin using Intel Realsense Camera, and inferred the 3d coordinate of the marker.

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