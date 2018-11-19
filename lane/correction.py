# -*- coding: utf-8 -*-


from lane.camera import calibrate
import glob
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt


def undistort(image, mtx, dist):
    undis_img = cv2.undistort(image, mtx, dist, None, mtx)

    return undis_img


if __name__ == "__main__":

    calibration_images = glob.glob('../camera_cal/calibration*.jpg')
    mtx, dist = calibrate(calibration_images)

    images = glob.glob('../test_images/*.jpg')
    for fname in images:
        image = mpimg.imread(fname)
        undis_img = undistort(image, mtx, dist)
        mpimg.imsave("../output_images/undistorted/" + fname.split("\\")[-1][:-4] + "-undistorted.jpg", undis_img)
        plt.imshow(undis_img)
        plt.show()

    # images = glob.glob('../camera_cal/calibration*.jpg')[0:1]
    # for fname in images:
    #     image = mpimg.imread(fname)
    #     undis_img = undistort(image, mtx, dist)
    #     mpimg.imsave("../output_images/undistorted/" + fname.split("\\")[-1][:-4] + "-undistorted.jpg", undis_img)
    #     plt.imshow(undis_img)
    #     plt.show()
