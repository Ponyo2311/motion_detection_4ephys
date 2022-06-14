# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 18:43:31 2022

@author: domi
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
#to save animation as GIF:
#https://towardsdatascience.com/basics-of-gifs-with-pythons-matplotlib-54dd544b6f30
import imageio
import cv2
import json

path2output = "C:/Users/domin/Documents/SCHOOL/STAGE2/motion_detection_4ephys/data/CSV_outputs/"
testing_CSV = os.path.join(path2output,"acA1300-60gmNIR__21471690__20211207_113623925.csv")
path2vid = "C:/Users/domi/.../motion_detection_4ephys/data/rats16s_Basler_acA1300-60gmNIR__21471690__20211207_113623925.mp4"
path2npy = "C:/Users/domi/.../motion_detection_4ephys/data/NPY_outputs/acA1300-60gmNIR__21471690__20211207_113623925_rat1&2.npy"
path2json = "C:/Users/domi/.../motion_detection_4ephys/data/NPY_outputs/acA1300-60gmNIR__21471690__20211207_113623925_rat1&2.json"

ts_dict = pd.read_csv(testing_CSV, sep= ",")
#print(ts_dict.head())

class Rat_mvm:
    '''create object 'rat_movement':
        - will be updated for every frame
        - plot updated plot'''
        
    def __init__(self):
        #init figure
        self.xs = []  #millisecs converted to secs
        self.ys1 = [] #rat 1
        self.ys2 = [] #rat2
        
        self.fig = plt.figure(figsize=(18, 10))
        self.gs = self.fig.add_gridspec(3, 2)
    
        self.ax1 = self.fig.add_subplot(self.gs[0, 0])
        self.ax2 = self.fig.add_subplot(self.gs[0, 1], sharey=self.ax1) #share axis with one of the subplots
        self.ax3 = self.fig.add_subplot(self.gs[1, 0])
        self.ax4 = self.fig.add_subplot(self.gs[1, 1])
        self.ax5 = self.fig.add_subplot(self.gs[2, 0:2])
        #self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3,1, sharey= False)...old
        
        #save figs for GIF
        self.filenames = []
        
        #init video
        self.vs = cv2.VideoCapture(path2vid)
        
        #shape of memmapped object
        with open(path2json,'r') as f:
            self.npyShape = json.load(f)
        f.close()
        
        #processed frames
        self.npyMvm = np.memmap(path2npy, dtype='uint8',mode='r', shape=tuple(self.npyShape['shape']))
        
        #TESTING
        # self.line1, = self.ax1.plot(self.xs, self.ys1, color="darkblue")
        # self.line2, = self.ax2.plot(self.xs, self.ys2, color="deeppink"))
        
        # self.ax1.title.set_text("rat1_left")
        # self.ax2.title.set_text("rat2_right")
        
    # def __init__(self):----------------------------------------------------------------------------------------
    #     #init figure
    #     self.xs = []  #millisecs converted to secs
    #     self.ys1 = [] #rat 1
    #     self.ys2 = [] #rat2
        
    #     self.fig, (self.ax1, self.ax2) = plt.subplots(1,2, sharey= True)
        
    #     # self.fig = plt.figure()
    #     # self.ax = self.fig.add_subplot(111)    # The big subplot
    #     # self.ax1 = self.fig.add_subplot(121)
    #     # self.ax2 = self.fig.add_subplot(122, sharey = self.ax1)
        
    #     self.ax1.title.set_text("rat1_left")
    #     self.ax2.title.set_text("rat2_right")
        
    #     # #remove axis labels
    #     # ax1.get_yaxis().set_visible(False)
    #     # ax2.axes.get_yaxis().set_visible(False)--------------------------------------------------------------
        
    
    def update(self, ts_dict, frame, m_rat1, m_rat2, fps_vs, secs):
        
        #tight layout
        #plt.tight_layout()
        
        #axes off
        for ax in [self.ax3,self.ax4,self.ax5]:
            ax.set_axis_off()
        
        #if there's more values than desired num of sec to plot, shorten it
        if len(ts_dict["millisec"]) >= fps_vs*secs:
            self.xs = ts_dict["millisec"][-int(fps_vs*secs):]
            self.xs = [float(x)/1000 for x in self.xs]
            self.ys1 = ts_dict["mvm_rat1"][-int(fps_vs*secs):]
            self.ys2 = ts_dict["mvm_rat2"][-int(fps_vs*secs):]
        else:
            #assign the whole dict 
            self.xs = ts_dict["millisec"]
            self.xs = [float(x)/1000 for x in self.xs]
            self.ys1 = ts_dict["mvm_rat1"]
            self.ys2 = ts_dict["mvm_rat2"]
        
       
        self.ax1.plot(self.xs, self.ys1, color="darkblue")
        self.ax2.plot(self.xs, self.ys2, color="deeppink")
        self.ax1.set_title("rat1_left")
        self.ax2.set_title("rat2_right")
        
        #moving rats
        #rat1
        self.ax3.imshow(m_rat1)
        #rat2
        self.ax4.imshow(m_rat2)
        
        #vid
        self.ax5.imshow(frame)
        
        
        #SAVE FIGS
        # create file name and append it to a list
        filename = f'{i}.png'
        self.filenames.append(filename)
        
        # save frame
        plt.savefig(os.path.join(path2output,"figs",filename))
        #plt.close()
        
        
        plt.show()
        plt.autoscale()
        plt.pause(0.00000000000001)
        
        #clear axis
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax4.clear()
        self.ax5.clear()
        
    def update_setData(self, ts_dict, fps_vs, secs):
        
        #clear axis
        #plt.cla()
        
        #if there's more values than desired num of sec to plot, shorten it
        if len(ts_dict["millisec"]) >= fps_vs*secs:
            self.xs = ts_dict["millisec"][-int(fps_vs*secs):]
            self.xs = [float(x)/1000 for x in self.xs]
            self.ys1 = ts_dict["mvm_rat1"][-int(fps_vs*secs):]
            self.ys2 = ts_dict["mvm_rat2"][-int(fps_vs*secs):]
        else:
            #assign the whole dict 
            self.xs = ts_dict["millisec"]
            self.xs = [float(x)/1000 for x in self.xs]
            self.ys1 = ts_dict["mvm_rat1"]
            self.ys2 = ts_dict["mvm_rat2"]
        
        # self.line1.set_data(self.xs, self.ys1)
        # self.line2.set_data(self.xs, self.ys2)
        self.line1.set_data(self.xs, self.ys1)
        self.line2.set_data(self.xs, self.ys2)
        self.ax1.set_title("rat1_left")
        self.ax2.set_title("rat2_right")
        
        
        
        plt.show()
        plt.autoscale()
        plt.pause(00000000.1)
        
        # self.ax1.clear()
        # self.ax2.clear()
        
        
    
    def animate(self,i, ts_dict):
        '''updater? 
        or just replot it as it is? 
        don't need i - entire dict is being incremented '''
        
        
        #assign values 
        self.xs = ts_dict["millisec"][:i]
        self.xs = [x/1000 for x in self.xs]
        self.ys1 = ts_dict["mvm_rat1"][:i]
        self.ys2 = ts_dict["mvm_rat2"][:i]
        
              
        #clear the axis (to not to stack plot) #OR WE CAN USE UPDATER
        plt.cla() #clear axis
        
        
        #plot into the figure that was previously intitated
        self.ax1.plot(self.xs, self.ys1, color="darkblue", label = "rat1_left")
        self.ax2.plot(self.xs, self.ys2, color="deeppink", label = "rat2_right")
        #self.ax1[1].plot(self.xs, self.ys2, color="deeppink", label = "rat2_right")
        
        #TRY TO CENTER-------------------------------
        plt.xlabel('seconds')
        plt.ylabel('movement')
        self.ax1.title.set_text("rat1_left")
        self.ax2.title.set_text("rat2_right")
        #plt.show()
        
           



if __name__ == '__main__':
    rm = Rat_mvm()
    ts_dict_i = []
    
    for i in range(200):
        ts_dict_i = ts_dict.iloc[:i,:]
    #     rm.plotting_updated(ts_dict_i)
        
        #vid
        ret, frame = rm.vs.read()
        
        #m_rats
        m_rat1 = rm.npyMvm[0,i]
        m_rat2 = rm.npyMvm[1,i]
        
    #     #FARGS: ts_dict (as tuple)
        rm.update(ts_dict_i, frame, m_rat1, m_rat2, fps_vs= 30, secs =3)
        
    # build gif
    with imageio.get_writer(os.path.join(path2output,"figs",'ratsgif.gif'), mode='I') as writer:
        for filename in rm.filenames[90:190]:
            image = imageio.imread(os.path.join(path2output,"figs",filename))
            writer.append_data(image)
            
    # Remove files
    for filename in set(rm.filenames):
        os.remove(os.path.join(path2output,"figs",filename))
 

