#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 16:41:26 2022

@author: domi
"""

from datetime import timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy import stats, signal
import os

def get_prominences(array):
    
    peaks_h = signal.find_peaks(array)[0]
    prominences_h = signal.peak_prominences(array, peaks_h)[0]
    
    return peaks_h, prominences_h

def gamma_fitting(array, CIlim):
    
    """
    TODO: try to fit the distri to all values, not only peaks.
    Fit gamma distribution to data (array) and get CI % set by CIlim).
    Returns: Outliers and CI value.
    """
    
    peaks, prominences = get_prominences(array = array)#,
                                                                                          
    #gammafit
    alpha,loc,beta = stats.gamma.fit(prominences) #beta=scale
    #quantile=np.arange(0,1400,10)
        
    #IC
    CI=stats.gamma.interval(CIlim,a=alpha,loc=loc,scale=beta)
    print(CI[1])
    
    # #plot distri on histogram
    # #PDF gamma
    # xhist=plt.hist(prominences,density=True,
    #                color="violet",alpha=0.5)
    # quantile=np.arange(0,round(max(xhist[1])),10)
    # R=stats.gamma.pdf(quantile,alpha,loc=loc,scale=beta)
    # plt.vlines(CI[1],ymin=min(R),ymax=max(R),color="red")
    # plt.plot(quantile,R,color="darkblue")
    # plt.show()
    
    #plot peaks that are > ICmax
    peaksGamma=peaks[prominences>CI[1]]
    return peaksGamma, CI[1]
    

def plot_mvm_rescaled(path2duration, path2mvm, f=25, plot_all = False,
                     start={"hours": 2, "minutes": 0, "seconds": 0},
                     dt={"hours": 1, "minutes": 0, "seconds": 0},
                     ylim=1.05, CIlim = 0.95):
    '''plot all duration + mvm or only a section'''
    
    #if you want to plot only a part 
    if not plot_all:
        # determine frames per sec number
        #f = 1000 / (float(df["millisec"][1]) - float(df["millisec"][0]))
        f = 25

        # start and end coordinates depending on duration
        # calculate indexes
        h0 = start["hours"]
        m0 = start["minutes"]
        s0 = start["seconds"]
        h1 = start["hours"] + dt["hours"]
        m1 = start["minutes"] + dt["minutes"]
        s1 = start["seconds"] + dt["seconds"]

        start_st = int((f * h0 * 60 * 60) + (f * m0 * 60) + (f * s0))
        end_st = int((f * h1 * 60 * 60) + (f * m1 * 60) + (f * s1))

    #otherwise plot all (from index 0 to index -1)
    else:
        start_st = 0
        end_st = -1
    
    #read & concatenate files
    d = open(path2duration,"r")
    duration_secs_rescaled = [[float(x) for x in line.split()] for line in d]
    d.close()
    duration_secs_rescaled = np.concatenate(duration_secs_rescaled)
    
    m = open(path2mvm,"r")
    mvm_test_copy = [[float(x) for x in line.split()] for line in m]
    m.close()
    mvm_test_copy = np.concatenate(mvm_test_copy)
    
    #convert duration to timedelta
    duration_secs_rescaled = [timedelta(seconds=float(i)) for i in duration_secs_rescaled]

    #change to df
    duration_secs_rescaled = pd.DataFrame(duration_secs_rescaled, columns=['duration'])

    # to keep only the time of the timedelta (otherwise give you estimate with days as well)
    duration_secs_rescaled['duration'] = duration_secs_rescaled['duration'].values.astype('datetime64[ns]')

    duration_secs_rescaled = [i.strftime("%H:%M:%S.%f")[:-3] for i in duration_secs_rescaled['duration']]


    #change to datetime object
    duration_secs_rescaled = pd.to_datetime(duration_secs_rescaled)


    #identify outliers and distribution confidence interval
    peaksGamma, CI_h = gamma_fitting(array=mvm_test_copy,
                                    CIlim=CIlim)
    
    fig, (ax1) = plt.subplots(1,1, figsize=(16, 8))
    
    #plot signal
    ax1.plot(duration_secs_rescaled[start_st:end_st],
             mvm_test_copy[start_st:end_st],
             label="rat_{}".format(
                 os.path.split(path2mvm)[1][3:6]),
             color = "darkturquoise",
             alpha = 0.6,
             #set to background
             zorder = 0)
    
    #scatter ourliers
    ax1.scatter(duration_secs_rescaled[peaksGamma], 
                mvm_test_copy[peaksGamma], 
                edgecolors="darkblue",label='artifacts', 
                #set to foreground
                zorder = 1)
    
    for ax in [ax1]:
        ax.set_ylim((0, ylim))
        ax.set_xlim((duration_secs_rescaled[start_st],duration_secs_rescaled[end_st]))
        ax.set_title("Movement {}".format(
            os.path.split(path2mvm)[1])[:-18],
                     fontsize=20)
        ax.set_xlabel("Duration", fontsize=16)
        ax.set_ylabel("Relative sum of pixel change", fontsize=16)
        ax.tick_params(axis='x', labelrotation=60, labelsize=14)
        #ax.xaxis.set_major_locator(mdates.DateFormatter('%Y-%b-%%H-%M'))
        ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
        #ax.xaxis.set_major_locator(plt.AutoLocator())
        ax.legend()
        
    
    #plot confidence interval 95% of fitted gamma distribution to movement values
    plt.hlines(y = CI_h, 
                xmin = duration_secs_rescaled[start_st], 
                xmax= duration_secs_rescaled[end_st],
                colors =['purple'], label='CI {} gamma'.format(CIlim),
                linestyles="dashed")
    
    plt.legend()
    plt.show()

# path2rat = "/media/data-119/Rat628-20210714/"
# path2mvm = "Rat628-20210714_1mvm_rescaled.txt"
# path2dur = "Rat628-20210714_1duration_rescaled.txt"
# plot_mvm_rescaled(path2duration = os.path.join(path2rat,path2dur), 
#                   path2mvm = os.path.join(path2rat,path2mvm), 
#                   f=25, plot_all = True,
#                   start={"hours": 4, "minutes": 12, "seconds": 0},
#                   dt={"hours": 0, "minutes": 1, "seconds": 0})