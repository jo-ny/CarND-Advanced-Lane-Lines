# -*- coding: utf-8 -*-

import glob
import numpy as np
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt


def hls_select_s(img, thresh=(0, 255)):
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    s_channel = hls[:, :, 2]
    binary_output = np.zeros_like(s_channel)
    binary_output[(s_channel > thresh[0]) & (s_channel <= thresh[1])] = 1
    return binary_output


def hls_select_l(img, thresh=(0, 255)):
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    s_channel = hls[:, :, 1]
    binary_output = np.zeros_like(s_channel)
    binary_output[(s_channel > thresh[0]) & (s_channel <= thresh[1])] = 1
    return binary_output

def adp_thresh_grayscale(image, thresh=250):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY).astype(np.uint8)
    img = cv2.equalizeHist(gray)
    ret, thrs = cv2.threshold(img, thresh=thresh, maxval=255, type=cv2.THRESH_BINARY)
    return thrs


if __name__ == "__main__":
    images = glob.glob('./output_images/undistorted/*.jpg')
    for fname in images:
        image = mpimg.imread(fname)
        hls_binary = adp_thresh_grayscale(image, thr=250)
        plt.imshow(hls_binary, cmap='gray')
        plt.title("S")
        plt.show()

    images = glob.glob('./output_images/undistorted/*.jpg')
    for fname in images:
        image = mpimg.imread(fname)
        hls_binary = hls_select_s(image, thresh=(140, 254))
        plt.imshow(hls_binary, cmap='gray')
        plt.title("S")
        plt.show()
