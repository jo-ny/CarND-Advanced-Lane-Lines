# -*- coding: utf-8 -*-
from lane.combined_threshold import combined_threshold
from lane.gaussian_blur import gaussian_blur
import numpy as np
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

src = np.float32([[700, 460],  # 右上
                  [1080, 720],  # 右下
                  [200, 720],  # 左下
                  [580, 460]])  # 左上

dst = np.float32([[980, 0],  # 右上
                  [980, 720],  # 右下
                  [300, 720],  # 左下
                  [300, 0]])  # 左上

def perspective(img,src=src, dst=dst):

    # Compute and apply perpective transform
    img_size = (img.shape[1], img.shape[0])
    M = cv2.getPerspectiveTransform(src, dst)  # 反向透视，对掉参数
    warped = cv2.warpPerspective(img, M, img_size, flags=cv2.INTER_NEAREST)  # keep same size as input image
    return warped


if __name__ == "__main__":
    import glob

    images = glob.glob('../output_images/threshold/*.jpg')
    for fname in images:
        image = mpimg.imread(fname)
        image = perspective(image)
        plt.imshow(image, cmap='gray')
        plt.show()
        mpimg.imsave("../output_images/perspective/" + fname.split("\\")[-1].split("-")[0] + "-perspective.jpg", image,
                     cmap="gray")
