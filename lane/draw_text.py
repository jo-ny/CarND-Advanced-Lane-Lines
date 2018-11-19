# -*- coding: utf-8 -*-
import cv2

def draw_text(image, r, v):
    image = cv2.putText(image, "Radius of Curvature = %d(m)" % int(r), (5, 40), cv2.FONT_HERSHEY_SIMPLEX , 1.2,
                        (255, 255, 255), 2,cv2.LINE_AA)
    image = cv2.putText(image, "Vehicle is %.2f(m) left of center" % v, (5, 80), cv2.FONT_HERSHEY_SIMPLEX , 1.2,
                        (255, 255, 255), 2,cv2.LINE_AA)
    return image
