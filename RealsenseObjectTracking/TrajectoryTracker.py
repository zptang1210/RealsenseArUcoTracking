## Detector for ArUco Markers with Intel RealSense Camera
## Author: zptang (UMass Amherst)

import numpy as np
import pyrealsense2 as rs
import matplotlib.pyplot as plt

class TrajectoryTracker:

    def __init__(self):
        self.trajectory = dict()


    def clear(self):
        self.trajectory = dict()


    def updateTrajectory(self, aligned_frame, detectorResult):
        corners, ids, rejected = detectorResult

        timestamp = aligned_frame.get_timestamp()
        depth_frame = aligned_frame.get_depth_frame()
        depth_intrinsics = depth_frame.profile.as_video_stream_profile().intrinsics
        #depth_image = np.asanyarray(depth_frame.get_data())

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

                coord = self._getCoordinate(depth_intrinsics, depth_frame, (topRight, bottomRight, bottomLeft, topLeft))
                if coord is not None:
                    self._add(timestamp, markerID, coord)

    
    def _add(self, timestamp, id, coord):
        if id not in self.trajectory.keys():
            self.trajectory[id] = list()
        x, y, z = coord
        self.trajectory[id].append((timestamp, x, y, z))
        #print(self.trajectory[0][-10:], '\n')


    def _getCoordinate(self, depth_intrinsics, depth_frame, markerPos):
        # for simplicity, just use the center point to extract the 3D coordinate
        # TODO: In future update, we can use fillPoly to mask the marker, and compute the average 3D coordinate
        topRight, bottomRight, bottomLeft, topLeft = markerPos
        cX = int((topLeft[0] + bottomRight[0]) / 2.0)
        cY = int((topLeft[1] + bottomRight[1]) / 2.0)

        depth = depth_frame.get_distance(cX, cY)
        if depth > 0:
            return rs.rs2_deproject_pixel_to_point(depth_intrinsics, [cX, cY], depth)
        else:
            return None


    def plotTrajectory(self):
        fig = plt.figure()
        ax = plt.axes(projection='3d')

        for id in self.trajectory.keys():
            x_line = [x for t, x, y, z in self.trajectory[id]]
            y_line = [y for t, x, y, z in self.trajectory[id]]
            z_line = [z for t, x, y, z in self.trajectory[id]]
            ax.scatter3D(x_line, y_line, z_line)

        plt.show()



if __name__ == '__main__':
    import time
    import cv2
    from ArUcoDetector import ArUcoDetector
    from Camera import Camera

    visualize = True
    dict_to_use = 'DICT_5X5_50'
    arucoDetector = ArUcoDetector(dict_to_use)

    tracker = TrajectoryTracker()

    camera = Camera()
    camera.startStreaming()
    
    start_time = time.time()
    try:
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

            # Update trajectory
            tracker.updateTrajectory(frame, result)

            # Show images
            images = np.hstack((color_image, masked_color_image, depth_colormap))
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', images)
            cv2.waitKey(1)

            current_time = time.time()
            print(current_time-start_time)
            if current_time - start_time >= 20:
                if visualize:
                    tracker.plotTrajectory()
                tracker.clear()
                start_time = current_time
    finally:
        camera.stopStreaming()