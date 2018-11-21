# -*- coding: utf-8 -*-
"""
@author: liweiqiang
@license: None
@contact: weiqiang.li@changhong.com
@file: output_images.py
@time: 2018/11/21 0021 14:17
@desc:
"""
import matplotlib.pyplot as plt
from matplotlib.image import imsave
from moviepy.editor import VideoFileClip

count = 0
start = 950
end = 1100
def pipeline(image):
    global count
    count += 1
    if start <= count <= end:
        print(count)
        if count%5 == 0:
            plt.imshow(image)
            plt.show()
        # if count%10 == 0:
            imsave("../error_images/second/error_image_"+str(count)+".jpg",image)
    return image


white_output = "../output_images/project_video.mp4"
clip1 = VideoFileClip("../project_video.mp4")
white_clip = clip1.fl_image(pipeline)
white_clip.write_videofile(white_output, audio=False)