# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import copy
import os


def rescalingNOF(path2ephysTime, path2mvm, path2duration):
    """
    
    Parameters
    ----------
    path2ephysTime : path to txt ephys frame timestamps file
    path2mvm : path to txt movement file
    path2duration : path to txt video duration file 

    Output
    -------
    Txt movement file with number of entries equal to number of timestamps in ephys sync file.
    File will be saved in the same folder as input files.

    """
    
    #path to SYNC_file & mvm file
    ephys_time_path = path2ephysTime
    mvm_path = path2mvm
    duration_path = path2duration
    
    #read SYNC_file
    e_test = open(ephys_time_path,"r")
    ephys_time_test = [[float(x) for x in line.split()] for line in e_test]
    e_test.close()
    
    #read mvm_file
    m_test = open(mvm_path,"r")
    mvm_test = [[float(x) for x in line.split()] for line in m_test]
    m_test.close()
    
    #read duration file (it's in secs)
    d_test = open(duration_path,"r")
    duration_test = [[float(x) for x in line.split()] for line in d_test]
    d_test.close()
    
    #concatenate the list of lists into one list (array)
    ephys_time_test = np.concatenate(ephys_time_test)
    mvm_test = np.concatenate(mvm_test)
    duration_test = np.concatenate(duration_test)
    
    #determine which file has more entries (if fs = 25, than mvm should have more)
    if len(mvm_test)/len(ephys_time_test) > 1:
        file2rescale = "mvm_test"
    else: 
        file2rescale = "ephys_time_test"
        
    if file2rescale == "mvm_test":
        #number of frames in mvm divided by the difference
        skip_rate = int(len(mvm_test)/(len(mvm_test)-len(ephys_time_test)))
        
        #create copy from which we delete items
        mvm_test_copy=copy.deepcopy(mvm_test)
        duration_test_copy = copy.deepcopy(duration_test)
        
        #delete evenly spaced entries
        mvm_test_copy=[mvm_test[i] for i in range(len(mvm_test)) if (i==0) | (i%skip_rate != 0)]
        duration_test_copy=[duration_test[i] for i in range(len(duration_test)) if (i==0) | (i%skip_rate != 0)]
        
        #verify it's close to the sum of diff (...TO_IMPLEMENT HERE IF YOU WANT...)
        print("{} frames were deleted.".format(len(mvm_test) - len(mvm_test_copy)))
        
        #extract name of the folder to create path to save the rescaled files
        folder = os.path.split(path2mvm)[0]
        rat = os.path.split(folder)[1]
        
        #save rescaled mvm and duration into the same folder
        np.savetxt(os.path.join(folder, rat+"_mvm_rescaled.txt"), 
                   mvm_test_copy)
        np.savetxt(os.path.join(folder, rat+"_duration_rescaled.txt"), 
                   duration_test_copy)
    
    #when the rescaled files are created, delete non-rescaled
    os.remove(path2mvm)
    os.remove(path2duration)