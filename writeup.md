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

This project contains the following contents:
- ./lane                             - >  The implementations of the pipeline code are all in that directory.
- output_images                      - >  The results of the intermediate steps of the operation on test_images are in this folder.
- output_voide/project_video.mp4     - >  The output result of applying pipeline to project_video. Mp4.
- wrtieup.md                         - >  This document.



---

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this section is in`./lane/camera. Py`.  
Objp objects represent the actual coordinates of the points on the board;  
The actual coordinates of the checkerboard are stored in objpoints;  
The corner coordinates detected from the checkerboard image are stored in imgpoints;  

First, the image is transformed into a grayscale image;   
Then use the cv2. FindChessboardCorners detection image of angular point;  
Store the detected value in imgpoints and the objpoints in a copy;  
Using cv2 calibrateCamera function calculated MTX, dist two values.  

In`./lane/correction.py`, `cv2.undistort` function is used, and `mtx` and `dist` calculated just now are used to remove the distortion in the picture. The effect is as follows:  
 
![alt text][image1]  
Obviously, the distortion in the first image was corrected, which indicated that the camera calibration was normal and the image distortion removal could be normal.  
![alt text][image2]  

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.
Before removing the distortion,    
![alt text][image3]   
After the distortion removal operation:   
![alt text][image4]   
Since the original image distortion is not very serious, the effect is not obvious.  

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

At the same time, I used the color space transformation method and gradient method to get the threshold binary image.  
- Color space conversion method   
    - In `HLS` color space, `S` component; This part is implemented in`./lane/color_threshold.py`  
- Gradient method: this part of the implementation is at`./lane/gradient_threshold.py`  
    - In the `x` direction,  
    - The `y` direction,  
    - `x**2+y**2`   
    - We use the `arctan` method in combination with the `x` and `y` direction  

Finally, combine these methods, implemented in the`./lane/combined_threshold.py` file:  
```python
combined[((gradx == 1) & (grady == 1)) | ((mag_binary == 1) & (dir_binary == 1)) | (hls_binary == 1)] = 1
```
The image thresholding operation of the last step to remove the distortion is performed:  
![alt text][image5]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The implementation of this part is in`./lane/perspective.py` file;  
Mainly contains `src`, `dst` variables and ` perspective ` function.  
```python
src = np.float32([[700, 460],  # right_top
                  [1080, 720],  # right_bottom
                  [200, 720],  # left_bottom
                  [580, 460]])  # left_top

dst = np.float32([[980, 0],  # right_top
                  [980, 720],  # right_bottom
                  [300, 720],  # left_bottom
                  [300, 0]])  # left_top
```

This resulted in the following source and destination points:  

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 700, 460      | 980, 0        | 
| 1080, 720     | 980, 720      |
| 200, 720      | 300, 720      |
| 580, 460      | 300, 0        |

Perform perspective transformation on the image generated by the previous operation, and generate the  bird's-eye view:  

![alt text][image6]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

Here, in order to show the process, the code for output intermediate results is implemented specifically in `./lane/visual.py`:  
In the `pipeline`, in order to improve the processing speed and simplify the code, the operation of output intermediate process picture was deleted, only the `x` and `y` coordinate points on the lane line were reserved, fit out fit and calculate the operation of fitx, which was realized in`./lane/ lane.py`  

The technique is histogram:  
- First select a bar of area from the bottom of the image, then sum it according to `axis=0`, and find the coordinates of the maximum value in the result, as the coordinates of the lane line in this bar
- Moving the strip from bottom to top, the `x` coordinates of the lane lines within the new area can also be found.  
- Collect the coordinates of the center points of lane lines found in this process, use `np.polyfit` for fitting, and get the fitting result fit.  
- Taking `y` as the independent variable, the lane line is calculated by using fit fit.  
- When the next frame appears, you don't need to do this, you just need to find the center coordinates of the lane lines around the fitting lane lines of the previous picture.  

This is the lane line search and fitting of the result picture of the previous step:  
![alt text][image7]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

This part of the operation is implemented in `measure_curvature_real` function in the `./lane/lane.py` file.  
The returned result is in meters (m).  

For the calculation of radius, the following formula is mainly used:  
```python 
ym_per_pix = 30 / 720  # meters per pixel in y dimension
xm_per_pix = 3.7 / 700  # meters per pixel in x dimension

fit_cr = np.polyfit(y * ym_per_pix, x * xm_per_pix, 2)

y_eval = np.max(ploty)

curverad = ((1 + (2 * fit_cr[0] * y_eval * ym_per_pix + fit_cr[1]) ** 2) ** 1.5) / np.absolute(2 * fit_cr[0])
```

For the position of the car and lane line, my method is:  
- Look for the `x` coordinates of the center point of the picture, which is the position of the vehicle
- Find the coordinates of the lane lines at the bottom of the picture and figure out the center of the lane lines.  
- Calculate the difference between the two and convert it into  meters (m) units.  

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

The main function implemented by the `draw_lane.py` file is to draw the lane line and the area between the lane line in the binary image generated in the previous step by using the `dst`, `src` variables, and the lane line `x` and `y` coordinates obtained from the previous generation of the aerial view, and change the drawing result to the perspective.   
![alt text][image8]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

This part of the implementation is in `. /lane/main.py`.  
Here's a [link to my video result](./project_video.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

In the process of realizing this project, I mainly encountered two major problems:   
- It is difficult to find the appropriate threshold during the threshold operation.  
- The radius of the left and right lane lines obtained by the fitting were inconsistent, and there were big differences in some cases.  

To solve the first problem, I tried a kind of thresholding operation first. When the result was good, I expanded the threshold range a little, and then gradually combined multiple methods, starting from two combinations, then four, then five...  

For the second problem, the method I use is to calculate the average result of the radius of the left and right lane lines to offset part of the anomaly.  
Colleague, average_fit, which USES n recent fit results in the fitting process, as the fitting parameter of current calculation of fited_x, can reduce the fluctuation of lane line radius a lot.  

Unresolved difficulties:  
- In video, in some scenes, the light is complex, and the edge of the lane line is distorted and bouncing.  
- One of the measures to solve this problem is to find a more suitable threshold parameter.  
