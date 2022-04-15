#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 20:02:32 2022

@author: domi
"""

import numpy as np
import os

def syncFileCreator(TTL2_folder = "/media/data-102/2021-07-14_21-20-16/Record Node 101/experiment1/recording1/events/Neuropix-PXI-100.1/TTL_2/",
                    lfp_tmp_folder = "/media/data-102/2021-07-14_21-20-16/Record Node 101/experiment1/recording1/continuous/Neuropix-PXI-100.1/",
                    output_sync_txt = "/media/data-119/Rat628-20210714/"):
    ''' 
    Output folder ...
    '''
    #os.chdir("/media/data-116/Dax/1.Data/2021-05-25_12-32-00/Record Node 102/experiment1/recording1/events/Neuropix-PXI-100.1/TTL_2")
    TTL2_folder=TTL2_folder
    
    timestamps_events=np.load(os.path.join(TTL2_folder,"timestamps.npy"))
    #timestamps_diffed=np.diff(timestamps_events)
    #full_words=np.load(os.path.join(TTL2_folder,"full_words.npy"))
    channel_states=np.load(os.path.join(TTL2_folder,"channel_states.npy"))
    
    lfp_tmp_folder=lfp_tmp_folder
    #os.chdir(lfp_tmp_folder)
    timestamps_lfp=np.load(os.path.join(lfp_tmp_folder,"timestamps.npy"))
    
    #calculation of timestamps of video frames...
    timestamps_video_frames = timestamps_events[channel_states == 1] - timestamps_lfp[0] - 1
    #... in seconds (smapling freq is assumed 2500Hz).. can be an arg
    timestamps_video_frames_sec = [i/2500 for i in timestamps_video_frames]
    print("Video was recorded from second {}.".format(timestamps_video_frames[0]/2500))
    
    #output path
    out4txt = os.path.join(output_sync_txt,
                           os.path.split(output_sync_txt[:-1])[1]) #make sure output folder is assigned with "/" in the end of the string
    
    #ephys timestamps for video frames in seconds
    out4txt_secs = out4txt +"tmstp_sec.txt"
    #ephys timestamp for frames in sampling freq (2500Hz)    
    out4txt = out4txt + "tmstp.txt"
    
    
    #TODO: check whether it's better with np.savetxt
    np.savetxt(out4txt, timestamps_video_frames, fmt = "%d") #%d is decimal
    np.savetxt(out4txt_secs, timestamps_video_frames_sec, fmt = "%f")
    # #open writer object
    # file = open(out4txt, "w+")
    # # Saving the array in a text file
    # #content = str(new_array)
    # file.write(str(timestamps_video_frames))
    # #close writer object
    # file.close()
    
    
    samp_freq_lfp=25 ## the sampling freq is 25 (==the fs of video) in TTL_2
    len_of_vid_reco = len(timestamps_events)/(samp_freq_lfp*3600*2)
    print("Length of the video should be: {} hours".format(len_of_vid_reco))

syncFileCreator()