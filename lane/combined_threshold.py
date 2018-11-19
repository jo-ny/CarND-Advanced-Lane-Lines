# -*- coding: utf-8 -*-


from lane.color_threshold import hls_select_s,adp_thresh_grayscale
from lane.gradient_threshold import abs_sobel_thresh,mag_thresh,dir_threshold
from lane.gaussian_blur import gaussian_blur
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt


def combined_threshold(image, ksize=3,th=None):

    if th is None:
        th = [[20, 100],  # gradx
              [20, 100],  # grady
              [20, 100],  # mag_binary
              [0.7, 1.3],  # dir_binary
              [90, 255],  # hls_binary
              [250, 0]]  # adp_binary

    gradx = abs_sobel_thresh(image, orient='x', sobel_kernel=ksize, thresh=(th[0][0], th[0][1]))
    grady = abs_sobel_thresh(image, orient='y', sobel_kernel=ksize, thresh=(th[1][0], th[1][1]))
    mag_binary = mag_thresh(image, sobel_kernel=ksize, mag_thresh=(th[2][0], th[2][1]))
    dir_binary = dir_threshold(image, sobel_kernel=ksize, thresh=(th[3][0], th[3][1]))
    hls_binary = hls_select_s(image, thresh=(th[4][0], th[4][1]))
    adp_binary = adp_thresh_grayscale(image, thresh=th[5][0])
    combined = np.zeros_like(dir_binary)
    # combined[((gradx == 1) & (grady == 1)) | ((mag_binary == 1) & (dir_binary == 1)) | (hls_binary == 1) | (adp_binary == 1)] = 1
    combined[((gradx == 1) & (grady == 1)) | ((mag_binary == 1) & (dir_binary == 1)) | (hls_binary == 1)] = 1
    #     combined[((gradx == 1) & (grady == 1)) | ((mag_binary == 1) & (dir_binary == 1))] = 1
    #     combined[(gradx == 1) & (grady == 1)] = 1  # x = 5 y = 5
    #     combined[((mag_binary == 1) & (dir_binary == 1))] = 1
    #     combined[(hls_binary == 1 )] = 1
    return combined


if __name__ == "__main__":
    import  glob
    images = glob.glob('../output_images/undistorted/*.jpg')
    for fname in images:
        image = mpimg.imread(fname)
        image = gaussian_blur(image, 3)
        combined = combined_threshold(image, ksize=3,th=[[20, 100], [25, 254], [100, 250], [0.6, 1.2], [180, 254], [250, 0]])
        fig, ax = plt.subplots(figsize=(20, 7))
        ax.imshow(combined, cmap='gray')
        plt.show()
        mpimg.imsave("../output_images/threshold/" + fname.split("\\")[-1].split("-")[0] + "-threshold.jpg", combined,cmap="gray")
