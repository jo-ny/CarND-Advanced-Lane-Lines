# -*- coding: utf-8 -*-

import glob
import numpy as np
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt


def calibrate(calibration_images):
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6 * 9, 3), np.float32)
    objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d points in real world space
    imgpoints = []  # 2d points in image plane.

    # Make a list of calibration images

    # Step through the list and search for chessboard corners
    for filename in calibration_images:
        img = mpimg.imread(filename)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)

        # If found, add object points, image points
        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)

            # # Draw and display the corners
            # img = cv2.drawChessboardCorners(img, (9, 6), corners, ret)
            # plt.imshow(img)
            # plt.show()

    img = mpimg.imread(calibration_images[0])
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    return mtx, dist


if __name__ == "__main__":
    calibration_images = glob.glob('./camera_cal/calibration*.jpg')
    mtx, dist = calibrate(calibration_images)


