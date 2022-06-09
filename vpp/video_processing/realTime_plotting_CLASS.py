# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 18:43:31 2022

@author: domin
"""


from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt


# path2output = "C:/Users/domin/Documents/SCHOOL/STAGE2/motion_detection_4ephys/data/CSV_outputs/"
# testing_CSV = os.path.join(path2output,"acA1300-60gmNIR__21471690__20211207_113623925_SHORT.csv")

# ts_dict = pd.read_csv(testing_CSV, sep= ",")
# #print(ts_dict.head())

class Rat_mvm:
    '''create object 'rat_movement':
        - will be updated for every frame
        - plot updated plot'''
        
    def __init__(self):
        #init figure
        self.xs = []  #millisecs converted to secs
        self.ys1 = [] #rat 1
        self.ys2 = [] #rat2
        
        self.fig, (self.ax1, self.ax2) = plt.subplots(1,2, sharey= True)
        
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
        
    
    def update(self, ts_dict, fps_vs, secs):
        
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
        
       
        self.ax1.plot(self.xs, self.ys1, color="darkblue")
        self.ax2.plot(self.xs, self.ys2, color="deeppink")
        self.ax1.set_title("rat1_left")
        self.ax2.set_title("rat2_right")
        
        plt.show()
        plt.autoscale()
        plt.pause(0000.1)
        
        #clear axis
        self.ax1.clear()
        self.ax2.clear()
        
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
        plt.pause(0000.1)
        
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
    
           



# #comment below if NOT testing 

# rm = Rat_mvm()
# ts_dict_i = []

# for i in range(500):
#     ts_dict_i = ts_dict.iloc[:i,:]
# #     rm.plotting_updated(ts_dict_i)
    
# #     #FARGS: ts_dict (as tuple)
#     rm.update(ts_dict_i, fps_vs= 10, secs =3)
 
   