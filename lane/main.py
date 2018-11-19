# -*- coding: utf-8 -*-
from lane.pipeline import pipeline

# import matplotlib.image as mpimg
# import matplotlib.pyplot as plt

# def pipeline(images):

    # return



from moviepy.editor import VideoFileClip

white_output = "../output_images/project_video.mp4"
clip1 = VideoFileClip("../project_video.mp4")
white_clip = clip1.fl_image(pipeline)
white_clip.write_videofile(white_output, audio=False)