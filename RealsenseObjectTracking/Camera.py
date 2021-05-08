## Detector for ArUco Markers with Intel RealSense Camera
## Author: Zhipeng Tang (UMass Amherst)

import pyrealsense2 as rs
import numpy as np
import cv2

class Camera:

    def __init__(self):
        self.isStreaming = False

        # Camera configuration
        # Configure depth and color streams
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = self.config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))

        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

        if device_product_line == 'L500':
            self.config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
        else:
            self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        # Create an align object
        # rs.align allows us to perform alignment of depth frames to others frames
        # The "align_to" is the stream type to which we plan to align depth frames.
        align_to = rs.stream.color
        self.align = rs.align(align_to)
    

    def __del__(self):
        self.stopStreaming()


    def startStreaming(self):
        if not self.isStreaming:
            self.pipeline.start(self.config)
            self.isStreaming = True


    def stopStreaming(self):
        if self.isStreaming:
            self.pipeline.stop()
            self.isStreaming = False

    
    def getNextFrame(self):
        if self.isStreaming == False:
            return None

        frame = self.pipeline.wait_for_frames()
        return self._alignFrame(frame)


    def _alignFrame(self, frame):
        return self.align.process(frame)


    def extractImagesFromFrame(self, frame):
        depth_frame = frame.get_depth_frame()
        color_frame = frame.get_color_frame()
        if not depth_frame or not color_frame:
            return None, None

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        return depth_image, color_image




if __name__ == '__main__':
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

        # Show images
        images = np.hstack((color_image, masked_color_image, depth_colormap))
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        cv2.waitKey(1)

    camera.stopStreaming()