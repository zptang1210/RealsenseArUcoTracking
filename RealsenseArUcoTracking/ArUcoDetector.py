## Detector for ArUco Markers with Intel RealSense Camera
## Author: zptang (UMass Amherst)

import cv2

class ArUcoDetector:

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

    def __init__(self, dict_to_use):
        self.dict_to_use = dict_to_use
        self.arucoDict = cv2.aruco.Dictionary_get(ArUcoDetector.ARUCO_DICT[dict_to_use])
        self.arucoParams = cv2.aruco.DetectorParameters_create()


    def detect(self, image):
        result = cv2.aruco.detectMarkers(image, self.arucoDict, parameters=self.arucoParams)
        return result


    @staticmethod
    def getImageWithMarkers(input_image, detect_res):
        image = input_image.copy()
        corners, ids, rejected = detect_res

        # verify *at least* one ArUco marker was detected
        if len(corners) > 0:
	        # flatten the ArUco IDs list
            ids = ids.flatten()
	        # loop over the detected ArUCo corners
            for (markerCorner, markerID) in zip(corners, ids):
		        # extract the marker corners (which are always returned in
		        # top-left, top-right, bottom-right, and bottom-left order)
                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
		        # convert each of the (x, y)-coordinate pairs to integers
                topRight = (int(topRight[0]), int(topRight[1]))
                bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                topLeft = (int(topLeft[0]), int(topLeft[1]))

                # draw the bounding box of the ArUCo detection
                cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
                cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
                cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
                cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
                # compute and draw the center (x, y)-coordinates of the ArUco marker
                cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
                # draw the ArUco marker ID on the image
                cv2.putText(image, str(markerID),
                (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                #print("[INFO] ArUco marker ID: {}".format(markerID))
        
        return image


if __name__ == '__main__':
    from Camera import Camera
    import numpy as np

    dict_to_use = 'DICT_5X5_50'
    arucoDetector = ArUcoDetector(dict_to_use)

    camera = Camera()
    camera.startStreaming()
    while True:
        frame = camera.getNextFrame()
        depth_image, color_image = camera.extractImagesFromFrame(frame)

        # Remove unaligned part of the color_image to grey
        grey_color = 153
        depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #depth image is 1 channel, color is 3 channels
        masked_color_image = np.where(depth_image_3d <= 0, grey_color, color_image)

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        # Detect markers and draw them on the images
        result = arucoDetector.detect(color_image)
        color_image = ArUcoDetector.getImageWithMarkers(color_image, result)
        masked_color_image = ArUcoDetector.getImageWithMarkers(masked_color_image, result)
        depth_colormap = ArUcoDetector.getImageWithMarkers(depth_colormap, result)

        # Show images
        images = np.hstack((color_image, masked_color_image, depth_colormap))
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        cv2.waitKey(1)

    camera.stopStreaming()
