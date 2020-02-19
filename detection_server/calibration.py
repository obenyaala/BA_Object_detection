# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 16:46:42 2020

@author: WN00151959
"""

ROBOT_CORD = [-1031, 36]
CAMERA_CORD = [125,110]

X_CORRECTION = (40/681)*100
Y_CORRECTION = (31/461)*100

DISTANCE_C = 100/40
DISTANCE_R = 40/100

def get_Cordinates(point):
    x_dist = CAMERA_CORD[0] - point[0]
    y_dist = point[1] - CAMERA_CORD[1]
    x_r = x_dist * DISTANCE_C
    y_r = y_dist * DISTANCE_C
    x_r = x_r + ROBOT_CORD[0]
    y_r = y_r + ROBOT_CORD[1]
    r_x_dist = abs(ROBOT_CORD[0] - x_r)
    r_y_dist = abs(ROBOT_CORD[1] - y_r)    
    """ Y Correction after moving X """
    if x_dist > 0:
        y_r = y_r - (r_x_dist*Y_CORRECTION) / 100
    else:
        y_r = y_r + (r_x_dist*Y_CORRECTION) / 100
    
    """ X Correction after moving Y """
    
    if y_dist > 0:
        x_r = x_r + (r_y_dist * X_CORRECTION) / 100
    else:
        x_r = x_r - (r_y_dist * X_CORRECTION) / 100
    return [x_r, y_r]