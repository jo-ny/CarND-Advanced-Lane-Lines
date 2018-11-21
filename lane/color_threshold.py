# -*- coding: utf-8 -*-

import glob
import numpy as np
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

def hls_select_h(img, thresh=(0, 255)):
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    h_channel = hls[:, :, 0]
    binary_output = np.zeros_like(h_channel)
    binary_output[(h_channel > thresh[0]) & (h_channel <= thresh[1])] = 1
    return binary_output

def hls_select_l(img, thresh=(0, 255)):
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    l_channel = hls[:, :, 1]
    binary_output = np.zeros_like(l_channel)
    binary_output[(l_channel > thresh[0]) & (l_channel <= thresh[1])] = 1
    return binary_output

def hls_select_s(img, thresh=(0, 255)):
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    s_channel = hls[:, :, 2]
    binary_output = np.zeros_like(s_channel)
    binary_output[(s_channel > thresh[0]) & (s_channel <= thresh[1])] = 1
    return binary_output

def lab_select_l(img, thresh=(0, 255)):
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2Lab)
    l_channel = lab[:, :, 0]
    binary_output = np.zeros_like(l_channel)
    binary_output[(l_channel > thresh[0]) & (l_channel <= thresh[1])] = 1
    return binary_output

def lab_select_a(img, thresh=(0, 255)):
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2Lab)
    a_channel = lab[:, :, 1]
    binary_output = np.zeros_like(a_channel)
    binary_output[(a_channel > thresh[0]) & (a_channel <= thresh[1])] = 1
    return binary_output

def lab_select_b(img, thresh=(0, 255)):
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2Lab)
    b_channel = lab[:, :, 2]
    binary_output = np.zeros_like(b_channel)
    binary_output[(b_channel > thresh[0]) & (b_channel <= thresh[1])] = 1
    return binary_output


def luv_select_l(img, thresh=(0, 255)):
    luv = cv2.cvtColor(img, cv2.COLOR_RGB2LUV)
    l_channel = luv[:, :, 0]
    binary_output = np.zeros_like(l_channel)
    binary_output[(l_channel > thresh[0]) & (l_channel <= thresh[1])] = 1
    return binary_output


def luv_select_u(img, thresh=(0, 255)):
    luv = cv2.cvtColor(img, cv2.COLOR_RGB2LUV)
    u_channel = luv[:, :, 1]
    binary_output = np.zeros_like(u_channel)
    binary_output[(u_channel > thresh[0]) & (u_channel <= thresh[1])] = 1
    return binary_output

def luv_select_v(img, thresh=(0, 255)):
    luv = cv2.cvtColor(img, cv2.COLOR_RGB2LUV)
    v_channel = luv[:, :, 2]
    binary_output = np.zeros_like(v_channel)
    binary_output[(v_channel > thresh[0]) & (v_channel <= thresh[1])] = 1
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
        hls_binary = adp_thresh_grayscale(image, thresh=250)
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

    # images = glob.glob('../error_images/first/*.jpg')
    # for fname in images:
    #     image = mpimg.imread(fname)
    #     luv_binary = luv_select_l(image, thresh=[225,255])
    #     plt.imshow(luv_binary, cmap='gray')
    #     plt.title("LUV_L")
    #     plt.show()

    # images = glob.glob('../error_images/first/*.jpg')
    # for fname in images:
    #     image = mpimg.imread(fname)
    #     lab_binary = lab_select_b(image, thresh=[155, 200])
    #     plt.imshow(lab_binary, cmap='gray')
    #     plt.title("lab_b")
    #     plt.show()

    # images = glob.glob('../error_images/first/*.jpg')
    # for fname in images:
    #     image = mpimg.imread(fname)
    #     hls_binary = hls_select_s(image, thresh=[240, 255])
    #     plt.imshow(hls_binary, cmap='gray')
    #     plt.title("lab_b")
    #     plt.show()


