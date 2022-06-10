#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 18:18:30 2022

@author: domi
"""

import cv2

def count_frames(path, override=False):
    """The first method to count video frames 
    in OpenCV with Python is very fast — it simply 
    uses the built-in properties OpenCV provides to 
    access a video file and read the meta information of the video."""
    
	# grab a pointer to the video file and initialize the total
	# number of frames read
    video = cv2.VideoCapture(path)
    total = 0
    
    try:
        total=int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    except:
        print("someting's wrong")
    
    # release the video file pointer
    video.release()
    
    # return the total number of frames in the video
    return total