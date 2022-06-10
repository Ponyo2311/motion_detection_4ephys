#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 17:19:12 2022

@author: domi
"""

# import os
# import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats, signal
import os
from datetime import timedelta
import pandas as pd
import matplotlib.dates as mdates

def get_prominences(array):
    
    peaks_h = signal.find_peaks(array)[0]
    prominences_h = signal.peak_prominences(array, peaks_h)[0]
    
    return peaks_h, prominences_h


def gamma_fitting(path2mvm, path2duration, distance=1, CIlim=0.95):
    
    """
    """
    
    
    d = open(path2duration,"r")
    duration = [[float(x) for x in line.split()] for line in d]
    d.close()
    duration = np.concatenate(duration)
    
    m = open(path2mvm,"r")
    mvm = [[float(x) for x in line.split()] for line in m]
    m.close()
    mvm = np.concatenate(mvm)
    
    #convert duration to timedelta
    duration = [timedelta(seconds=float(i)) for i in duration]

    #change to df
    duration = pd.DataFrame(duration, columns=['duration'])

    # to keep only the time of the timedelta (otherwise give you estimate with days as well)
    duration['duration'] = duration['duration'].values.astype('datetime64[ns]')

    duration = [i.strftime("%H:%M:%S.%f")[:-3] for i in duration['duration']]


    #change to datetime object
    duration = pd.to_datetime(duration)
    

    array = mvm
    peaks, prominences = get_prominences(array = array)#,
                                                                                           
    ####################
    
    #gammafit
    alpha,loc,beta=stats.gamma.fit(prominences) #beta=scale
    #quantile=np.arange(0,1400,10)
    #PDF gamma
    xhist=plt.hist(prominences,density=True,
                   color="violet",alpha=0.5)
    quantile=np.arange(0,round(max(xhist[1])),10)
    R=stats.gamma.pdf(quantile,alpha,loc=loc,scale=beta)
    #IC
    IC=stats.gamma.interval(0.95,a=alpha,loc=loc,scale=beta)
    plt.vlines(IC[1],ymin=min(R),ymax=max(R),color="red")
    plt.plot(quantile,R,color="darkblue")
    plt.show()
    
    
    #plot peaks that are > ICmax
    peaksGamma=peaks[prominences>IC[1]]
    plt.figure(figsize=(16,5))
    plt.plot(duration, mvm, 'lightblue', label='data',alpha=0.5)
    plt.scatter(duration[peaksGamma],mvm[peaksGamma], edgecolors="darkblue",label='artifacts', alpha = 0.9)
    plt.legend()
    plt.show()
    ########################################
    
path2rat = "/media/data-119/Rat628-20210714/"
path2mvm = "Rat628-20210714_1mvm_rescaled.txt"
path2dur = "Rat628-20210714_1duration_rescaled.txt"
gamma_fitting(path2mvm = os.path.join(path2rat, path2mvm),
              path2duration = os.path.join(path2rat, path2dur))

    # # fitting gamma to prominences
    # m, sd = stats.norm.fit(prominences)  # beta=scale
    # xhist = plt.hist(prominences, density=True,
    #                  color="grey", alpha=0.5)
    # quantile = np.linspace(stats.norm.ppf(0.001, loc=m, scale=sd),
    #                        stats.norm.ppf(0.999, loc=m, scale=sd), 1000)
    # CI = stats.norm.interval(CIlim, loc=m, scale=sd)
    # print(CI)
    # R = stats.norm.pdf(quantile, loc=m, scale=sd)
    # plt.vlines(x=[CI[1], CI[0]], ymin=min(R), ymax=max(R), color=["red", "green"], linestyle="dashed")
    # plt.plot(quantile, R, color="darkblue")
    # plt.show()

    # plt.figure(figsize=(16, 5))
    # plt.plot(oriDF.index, oriDF.iloc[:, col_index], 'pink', label='data', alpha=0.3)
    # # plt.plot(testSlice1.index, testSlice1.iloc[:,1], 'violet', label='data',alpha=0.7)
    # # plt.plot(testSlice2.index, testSlice2.iloc[:,1], 'violet', label='data',alpha=0.7)
    # for i in range(len(peaks)):
    #     peaksGammaHigh = peaks[i][prominences_high[i] > CI[1]]
    #     peaksGammaLow = peaks_low[i][prominences_low[i] < CI[0]]
    #     plt.scatter(df[i].index[peaksGammaHigh], df[i].iloc[:, col_index][peaksGammaHigh], color="red")
    #     plt.scatter(df[i].index[peaksGammaLow], df[i].iloc[:, col_index][peaksGammaLow], color="green")
    #     # plt.plot(col2analyse.index, col2analyse, 'pink', label='data',alpha=0.5)
    #     plt.plot(df[i].index, df[i].iloc[:, col_index], 'violet', label='data', alpha=0.5)
    #     # plt.plot(df.index, inversed_col, 'darkblue', label='data',alpha=0.5)
    # plt.show()
