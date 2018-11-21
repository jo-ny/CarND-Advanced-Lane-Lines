# -*- coding: utf-8 -*-
# use pipeline to precess project_video.mp4

from lane.pipeline import pipeline
from moviepy.editor import VideoFileClip

white_output = "../output_images/project_video.mp4"
clip1 = VideoFileClip("../project_video.mp4")
white_clip = clip1.fl_image(pipeline)
white_clip.write_videofile(white_output, audio=False)