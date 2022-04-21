#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 17:17:56 2022

@author: domi
"""
import pandas as pd 
import os
import numpy as np


def mvm2txt(path2csv, rat):
    ''' + extracts normalized movement vector for the specified 
    rat and save it as txt in the same folder;
        + save rescaled timestamp as well'''
        
    #read csv
    df = pd.read_csv(path2csv, index_col="timestamp", sep = ',')
    
    #set duration as index
    df.index = pd.to_datetime(df['duration'])
    #drop duration as column
    df = df.drop('duration', axis = 1)
    
    path2folder = os.path.split(path2csv)[0]
    print(path2folder)
    
    #print(os.path.split(path2folder)[1]+"mvm.txt")
    
    #convert millisecs to secs
    secs = [i/1000 for i in df["millisec"]]
    
    saveMvm2 = os.path.join(path2folder, os.path.split(path2folder)[1]+"mvm.txt")
    saveDuration2 = os.path.join(path2folder, os.path.split(path2folder)[1]+"duration.txt")
    print(saveMvm2)
    
    np.savetxt(saveMvm2, df[f"mvmr{rat}_normalized"])
    #save duration in seconds
    np.savetxt(saveDuration2, secs)
    
csv_01 = "/media/data-119/rat596_20210701_184333/acA1300-60gmNIR__21471690__20210701_184333372.csv"
mvm2txt(csv_01, rat=1)