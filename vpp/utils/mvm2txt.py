#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 17:17:56 2022

@author: domi
"""
import pandas as pd 
import os
import numpy as np
import cv2

def chopOffTail(path2vid,
               path2ephysTime):
    
    '''
    ephys syncfile input sould be in seconds
    '''
    
    # 1) VIDEO DURATION
    #init the VideoCapture object
    try:
        vid = cv2.VideoCapture(path2vid)
    except:
        vid = cv2.VideoCapture(input("Enter path to the video"))

    #get duration of video in secs
    vid_sec = vid.get(cv2.CAP_PROP_FRAME_COUNT)/vid.get(cv2.CAP_PROP_FPS)

    print("Video duration: {}".format(vid_sec))

    #release the VideoCapture object
    vid.release()

    # 2) TTL2 DURATION
    #read previously created .txt SYNC_file
    e = open(path2ephysTime,"r")
    ephys_time = [[float(x) for x in line.split()] for line in e]
    e.close()

    #concatenate the list of lists into one list (array)
    ephys_time = np.concatenate(ephys_time)

    # #convert ephys to seconds (divide by sampling freq)
    # ephys_time = [i/2500 for i in ephys_time]

    #get the difference between frame in milliseconds
    ephys_time_diff=np.diff(ephys_time)

    #sum of diffs => should be the same as duration of video !!
    ephys_sec = np.sum(ephys_time_diff)
    print("Sum of diffs: {}.".format(ephys_sec))

    # 3) CALCULATE THE DIFFERENCE
    diff_sec =  vid_sec - ephys_sec
    nb_of_frames_2remove = int(diff_sec/0.04)
    print("Video signal is {} seconds longer than sync_file, which corresponds to {} number of frames".format(diff_sec, nb_of_frames_2remove))

    #remove frames if difference is bigger equal or bigger than 1s
    if diff_sec > 0:
        return nb_of_frames_2remove
    else:
        return False
        

def mvm2txt(path2csv, rat, 
            #chopOffTail = False,
           path2vid = None,
           path2ephysTime = None):
    
    ''' + extracts normalized movement vector for the specified 
    rat and save it as txt in the same folder;
        + save rescaled timestamp as well
        + if the video recording was stopped AFTER ephys, then it will be calculated in seconds how much it is needed to be removed from the tail of the movement signal
        + if chopOfTail is True, the path to the video has to be given'''
        
    #read csv
    df = pd.read_csv(path2csv, index_col="timestamp", sep = ',')
    
    #set duration as index
    df.index = pd.to_datetime(df['duration'])
    #drop duration as column
    df = df.drop('duration', axis = 1)
    
    path2folder = os.path.split(path2csv)[0]
    
    #convert millisecs to secs
    secs = [i/1000 for i in df["millisec"]]
    
    #if the video is longer than TTL signal, then we have to cut it
    nb_of_frames2remove =  chopOffTail(path2vid = path2vid,
               path2ephysTime = path2ephysTime)
    if nb_of_frames2remove:
        secs = secs[:-nb_of_frames2remove]
        
    saveMvm2 = os.path.join(path2folder, os.path.split(path2folder)[1]+"mvm.txt")
    saveDuration2 = os.path.join(path2folder, os.path.split(path2folder)[1]+"duration.txt")
    
    if nb_of_frames2remove:
        np.savetxt(saveMvm2, df[f"mvmr{rat}_normalized"][:-nb_of_frames2remove])
    else:
        np.savetxt(saveMvm2, df[f"mvmr{rat}_normalized"])
    #save duration in seconds
    np.savetxt(saveDuration2, secs)

# if __name__ == '__main__':
#     mvm2txt()    

# csv_01 = "/media/data-119/rat596_20210701_184333/acA1300-60gmNIR__21471690__20210701_184333372.csv"
# mvm2txt(csv_01, rat=1)