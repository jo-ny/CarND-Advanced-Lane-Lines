## Writeup

---

**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./camera_cal/calibration1.jpg "calibration1"
[image2]: ./output_images/calibration1-undistorted.jpg "calibration1-undistorted"
[image3]: ./test_images/straight_lines1.jpg "straight_lines1.jpg"
[image4]: ./output_images/undistorted/straight_lines1-undistorted.jpg "straight_lines1-undistorted.jpg"

[image5]: ./output_images/threshold/straight_lines1-threshold.jpg "straight_lines1-threshold.jpg"
[image6]: ./output_images/perspective/straight_lines1-perspective.jpg "straight_lines1-perspective.jpg"
[image7]: ./output_images/polynomial/straight_lines1-polynomial.jpg "straight_lines1-polynomial.jpg"
[image8]: ./output_images/warpedback/straight_lines1-warpedback.jpg "straight_lines1-warpedback.jpg"

[video1]: ./output_video/project_video.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

本次项目共包含以下内容:
- ./lane                             - >  pipeline code 的实现都在该目录中
- output_images                      - >  对test_images的操作的中间步骤的结果都在这个文件夹中
- output_voide/project_video.mp4     - >  对project_video.mp4应用pipeline的输出结果
- wrtieup.md                         - >  本文档



---

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

这部分的代码放在 ./lane/camera.py中。 
objp 对象代表着棋盘中角点的实际坐标；
objpoints中存放着棋盘的实际坐标;
imgpoints中存放着从棋盘图像中检测到的角点坐标;
首先将图片转换为灰度图；
然后使用cv2.findChessboardCorners检测图片中的角点；
将检测到值存入imgpoints中，objpoints也存入一份拷贝；
使用cv2.calibrateCamera函数计算得出mtx, dist两个值。

对图片进行去除畸变的操作在./lane/correction.py中，使用cv2.undistort函数，利用刚才计算得出的mtx, dist，去除图片中的畸变，效果如下：
 
![alt text][image1] 
明显可以看出，第一幅图像中的畸变得到了校正，这说明camera校准的操作是正常的，图像去除畸变的操作也可以正常进行。
![alt text][image2]

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.
进行去除畸变操作之前：  
![alt text][image3]  
去除畸变操作之后：  
![alt text][image4]  
由于原始图片畸变不是很严重，所以看起来效果不是很明显

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

我同时使用色彩空间转换方法，和梯度方法，得到了阈值化的二进制图像；
- 色彩空间转换方法
    - HLS色彩空间中，S分量；这部分实现在./lane/color_threshold.py中
- 梯度方法：这部分实现在./lane/gradient_threshold.py
    - x轴方向，
    - y轴方向，
    - x**2+y**2 
    - 使用arctan方法结合x，y方向的方法

最后使用将这些方法结合起来，这部分的实现在./lane/combined_threshold.py文件中：
```python
combined[((gradx == 1) & (grady == 1)) | ((mag_binary == 1) & (dir_binary == 1)) | (hls_binary == 1)] = 1
```
对上一步去除畸变操作的图片进行阈值化操作：
![alt text][image5]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

这部分的实现在./lane/perspective.py文件中；
主要包含src，dst变量和perspective函数，
```python
src = np.float32([[700, 460],  # 右上
                  [1080, 720],  # 右下
                  [200, 720],  # 左下
                  [580, 460]])  # 左上

dst = np.float32([[980, 0],  # 右上
                  [980, 720],  # 右下
                  [300, 720],  # 左下
                  [300, 0]])  # 左上
```

This resulted in the following source and destination points:

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 700, 460      | 980, 0        | 
| 1080, 720     | 980, 720      |
| 200, 720      | 300, 720      |
| 580, 460      | 300, 0        |

对上一步操作生成的图片进行透视变换,生成的鸟瞰图:

![alt text][image6]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

这里，为了展示处理的过程，专门实现了用于输出中间结果的代码，其实现在./lane/visual.py中；
在pipeline中，为了提高处理速度以及精简代码，将输出中间过程图片的操作删除，仅保留了寻找车道线上x，y坐标点，拟合出fit，计算出fitx的操作，这部分实现在./lane/Lane.py中

这里用到的技术是直方图技术；
- 先从图片底部选取一条形区域，然后按照axis=0方向求和，找到结果中极大值的的坐标，作为这一条带中车道线的坐标
- 由下至上移动条带，在新的区域中也能找到该区域内的车道线的x坐标
- 收集这一过程中找到的车道线中心点坐标，使用np.polyfit进行拟合，得到拟合结果fit，
- 以y为自变量，利用拟合出的fit，计算出拟合出的车道线
- 当下一帧出现时，无需这样操作，只需要在前一张图片的拟合出的车道线周围进行寻找车道线中心坐标

这是对上一步操作的结果图片进行车道线寻找和拟合；  
![alt text][image7]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

这部分操作实现在./lane/Lane.py 文件中的measure_curvature_real函数中。
返回的结果是以米(m)为单位的结果。

对于半径的计算，主要使用一下公式：
```python 
ym_per_pix = 30 / 720  # meters per pixel in y dimension
xm_per_pix = 3.7 / 700  # meters per pixel in x dimension

fit_cr = np.polyfit(y * ym_per_pix, x * xm_per_pix, 2)

y_eval = np.max(ploty)

curverad = ((1 + (2 * fit_cr[0] * y_eval * ym_per_pix + fit_cr[1]) ** 2) ** 1.5) / np.absolute(2 * fit_cr[0])
```

对于车与车道线的位置关系，我的方法是:
- 寻找图片中心点x坐标，视为车辆的位置
- 寻找车道线在图片底部的坐标，并求出车道线中心
- 计算出以上两者之差，并换算成m单位。

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

这部分操作是现在./lane/draw_lane.py  和 ./lane/draw_text.py 中。
其中draw_lane.py文件主要实现的功能是，利用之前生成鸟瞰图时用到的 dst, src 变量，以及拟合得到的车道线x，y坐标，在上一步生成的binary图片中绘制车道线，以及车道线之间的区域，并将绘制结果变化到透视图中；

![alt text][image8]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

这部分的实现在./lane/main.py中。  
Here's a [link to my video result](./project_video.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

我在实现该项目的过程中主要遇到两个主要的问题：
- 阈值化操作时，寻找合适的阈值比较困难；
- 拟合得到的左右两条车道线半径不一致，个别时候存在差异较大的情况；

针对第一个问题，我的做法是，先对一种阈值化操作进行尝试，当尝试结果效果较好的之后，将阈值范围扩大一些，然后再逐步将多个方法组合在一起，先从两个的组合开始，然后到四个，再到五个...。

针对第二个问题，我使用的方法是，将左右两条车道线的半径求取平均结果以抵消一部分的异常；同事，拟合过程中使用n个最近的fit结果的average_fit作为当前计算fited_x的拟合参数，能够将车道线半径的波动降低很多。

未解决的困难：
- 视频中，个别场景下，光线复杂，车道线边缘出现了变形和跳动。

- 针对这一问题的改进措施之一：寻找更加合适的阈值化参数
