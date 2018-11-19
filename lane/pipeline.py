# -*- coding: utf-8 -*-
from lane.camera import calibrate
from lane.correction import undistort
from lane.gaussian_blur import gaussian_blur
from lane.combined_threshold import combined_threshold
from lane.perspective import perspective, src, dst
from lane.Lane import Lane
from lane.measure_vehicle_pos import measure_vehicle_pos
from lane.draw_lane import draw_lane
from lane.draw_text import draw_text
import glob
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

print("================ camera calibrate ===================")
calibration_images = glob.glob('../camera_cal/calibration*.jpg')
m, d = calibrate(calibration_images)

print("=========== create left and right lanes===============")
l_lane = Lane()
r_lane = Lane()


def pipeline(image, mtx=m, dist=d, left_lane=l_lane, right_lane=r_lane):
    # 去畸变
    img = undistort(image, mtx, dist)

    # 平滑
    img = gaussian_blur(img, 3)

    # 阈值化
    combined = combined_threshold(img, ksize=3,th=[[20, 100], [25, 254], [100, 250], [0.8, 1.3], [180, 254], [250, 0]])
    #
    # plt.imshow(combined, cmap="gray")
    # plt.show()

    # 平滑
    combined = gaussian_blur(combined, 3)

    # plt.imshow(combined, cmap="gray")
    # plt.show()

    # 透视变化
    perspectived_img = perspective(combined, src, dst)
    # plt.imshow(perspectived_img, cmap="gray")
    # plt.show()

    # 检测左侧车道线
    left_lane.fit(perspectived_img, location = "left")

    # 检测右侧车道线
    right_lane.fit(perspectived_img, location = "right")


    # average_fit = left_lane.average_fit + right_lane.average_fit
    plt.imshow(perspectived_img)
    # plt.plot(left_lane.average_fitted_x,left_lane.ploty)
    # plt.plot(right_lane.average_fitted_x, right_lane.ploty)




    # 计算曲率
    left_r = left_lane.measure_curvature_real(left_lane.ploty, left_lane.allx, left_lane.ally)
    right_r = right_lane.measure_curvature_real(right_lane.ploty, right_lane.allx, right_lane.ally)
    r = (left_r + right_r)/2
    # print("left=%d right=%d avg=%d"%(int(left_r),int(right_r),int(r)))
    #
    # plt.text(0, 60, "L_R = %d" % int(left_r), fontdict={'size': 10, 'color': 'w'})
    # plt.text(1050, 60, "R_R = %d" % int(right_r), fontdict={'size': 10, 'color': 'w'})
    # plt.text(600, 60, "diff_R = %d" % int(abs(left_r - right_r)), fontdict={'size': 10, 'color': 'w'})
    # plt.show()

    # 计算偏移值
    v = measure_vehicle_pos(left_lane.average_fitted_x, right_lane.average_fitted_x, left_lane.current_warped_binary_shape[1])

    # 绘制车道线
    lane_img = draw_lane(image, combined, dst, src, left_lane.average_fitted_x, right_lane.average_fitted_x,right_lane.ploty)
    # plt.imshow(lane_img)
    # plt.show()
    # 绘制文字
    lane_img_with_text = draw_text(lane_img, r, v)


    return lane_img_with_text


if __name__ == "__main__":
    images = glob.glob("../output_images/undistorted/*.jpg")
    for filename in images:
        image = mpimg.imread(filename)
        img = pipeline(image)
        plt.imshow(img)
        plt.show()
        mpimg.imsave("../output_images/warpedback/" + filename.split("\\")[-1].split("-")[0] + "-warpedback.jpg", img,
                     cmap="gray")
