# -*- coding: utf-8 -*-
import glob
import numpy as np
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt


def draw_lane(image, binary_warped, dst, src, left_fitx, right_fitx, ploty):
    # Create an image to draw the lines on
    warp_zero = np.zeros_like(binary_warped).astype(np.uint8)
    # 用于绘制车道线之间的区域
    color_warp = np.dstack((warp_zero, warp_zero, warp_zero))
    # 用于绘制车道线
    lane_wrap = np.zeros_like(color_warp).astype(np.uint8)

    # Recast the x and y points into usable format for cv2.fillPoly()
    pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
    pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
    pts = np.hstack((pts_left, pts_right))

    # Draw the lane onto the warped blank image
    cv2.fillPoly(color_warp, np.int_([pts]), (0, 255, 0))

    lane_left_1 = np.array([np.transpose(np.vstack([left_fitx - 20, ploty]))])
    lane_left_2 = np.array([np.flipud(np.transpose(np.vstack([left_fitx + 20, ploty])))])
    lane_left = np.hstack((lane_left_1, lane_left_2))

    # Draw the lane onto the warped blank image
    cv2.fillPoly(lane_wrap, np.int_([lane_left]), (255, 0, 0))

    # Recast the x and y points into usable format for cv2.fillPoly()
    lane_right_1 = np.array([np.transpose(np.vstack([right_fitx - 20, ploty]))])
    lane_right_2 = np.array([np.flipud(np.transpose(np.vstack([right_fitx + 20, ploty])))])
    lane_right = np.hstack((lane_right_1, lane_right_2))

    # Draw the lane onto the warped blank image
    cv2.fillPoly(lane_wrap, np.int_([lane_right]), (0, 0, 255))

    M = cv2.getPerspectiveTransform(dst, src)  # 反向透视，对掉参数

    # Warp the blank back to original image space using inverse perspective matrix (Minv)
    new_color_warp = cv2.warpPerspective(color_warp, M, (image.shape[1], image.shape[0]))
    # Combine the result with the original image
    result = cv2.addWeighted(image, 1, new_color_warp, 0.3, 0)

    new_line_warp = cv2.warpPerspective(lane_wrap, M, (image.shape[1], image.shape[0]))
    # Combine the result with the original image
    result = cv2.addWeighted(result, 1, new_line_warp, 1.0, 0)

    return result