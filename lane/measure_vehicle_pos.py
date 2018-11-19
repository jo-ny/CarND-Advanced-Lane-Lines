# -*- coding: utf-8 -*-

def measure_vehicle_pos(leftx, rightx,shape):
    xm_per_pix = 3.7 / 700  # meters per pixel in x dimension

    middle_line = leftx[-1] + (rightx[-1] - leftx[-1]) / 2
    middel_cat = shape / 2

    vehicle_pos = (middel_cat - middle_line) * xm_per_pix

    return vehicle_pos



