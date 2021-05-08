## Generator for ArUco Markers with OpenCV
## Author: zptang (UMass Amherst)
## Reference: https://www.pyimagesearch.com/2020/12/14/generating-aruco-markers-with-opencv-and-python/

import os
import json
import numpy as np
import cv2

# available dictionaries from OpenCV
ARUCO_DICT = {
	"DICT_4X4_50": cv2.aruco.DICT_4X4_50,
	"DICT_4X4_100": cv2.aruco.DICT_4X4_100,
	"DICT_4X4_250": cv2.aruco.DICT_4X4_250,
	"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	"DICT_5X5_50": cv2.aruco.DICT_5X5_50,
	"DICT_5X5_100": cv2.aruco.DICT_5X5_100,
	"DICT_5X5_250": cv2.aruco.DICT_5X5_250,
	"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	"DICT_6X6_50": cv2.aruco.DICT_6X6_50,
	"DICT_6X6_100": cv2.aruco.DICT_6X6_100,
	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
	"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
	"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
	"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
	"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
	"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
	"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
	"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}


def readConfig(path):
    with open(path, 'r') as fin:
        config = json.load(fin)
    return config['dict_to_use'], config['visualize'], config['grey_color'], config['id']


def generateArUcoMarker(dict_to_use, id, visualize=True):
	# generatethe marker
	arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[dict_to_use])
	tag = np.zeros((300, 300, 1), dtype='uint8')
	cv2.aruco.drawMarker(arucoDict, id, 300, tag, 1)

	# save the marker and visualize it
	file_name = dict_to_use + '_' + str(id) + '.png'
	file_path = './tag/tag_' + dict_to_use + '/' 
	if not os.path.exists(file_path):
		os.makedirs(file_path)
	cv2.imwrite(file_path + file_name, tag)
	if visualize:
		cv2.imshow('ArUCO ' + file_name, tag)
		cv2.waitKey(0)


if __name__ == '__main__':
	dict_to_use, visualize, grey_color, id = readConfig('./config.json')
	generateArUcoMarker(dict_to_use, id, visualize)