# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 19:01:31 2022

@author: domi
"""
#NOTES ABOUT RAT SLEEP
#The study looked at 20 albino rats and recorded their sleeping 
#and waking times between 8 a.m. and 8 p.m. Of those 12 hours, 
#rats snoozed more than nine hours. The rest of the time they 
#were awake and active, awake and resting, or half-awake.

from motion_detector import resizing
#from getting_coordinates_manual_CLASS import Rat_coords
from matplotlib.animation import FuncAnimation #to use for afterplot
import matplotlib.pyplot as plt
import cv2
from motion_detector_MVMwriter import motion_detector_MVMwriter


#path to test video
path2vid_test="/media/data-116/Neuropixels Info/Videos/W627-W628/"


class Rat_coords:
    
    def __init__(self):
        #init canvas object
        self.cid_rats = None
        
        #init coords_rat
        self.coords_rat = []
        
        #init path to vid string (empty)
        self.path2vid = ''
    
    def shape_extractor(self, path2vid = path2vid_test, scale_percent = 50):
        '''STEP 1: GET SHAPE OF FRAMES'''
        
        self.scale_percent = scale_percent
        #create videocapture object to extract a frame
        vs_test = cv2.VideoCapture(path2vid)
        
        #print(vs_test.get(cv2.CAP_PROP_FRAME_COUNT))
        
        #get estimation of frame rate (n per second)
        fps_vs_test = vs_test.get(cv2.CAP_PROP_FPS)
        print("Estimated frame rate of the file: {}".format(fps_vs_test))
        ret_test, frame_test = vs_test.read()
        
        #downsize the image 
        frame_test_dw = resizing(frame=frame_test, scale_percent=scale_percent)
        
        #release the VideoCapture object 
        vs_test.release()
        
        # convert to B&W image (get rid of th 3rd dimension)
        self.frame_test_gray = cv2.cvtColor(frame_test_dw, cv2.COLOR_BGR2GRAY)
        
        #frame.shape[0] gives y axis and [1] x axis!
        self.x = self.frame_test_gray.shape[1]
        self.y = self.frame_test_gray.shape[0]
        #print([self.x, self.y, self.frame_test_gray.shape])
        
        #STEP2: GET COORDS OF RAT1 & RAT2 cages
        self.fig = plt.figure()
        ax = self.fig.add_subplot(111)
        
        #change from ax.plot(x,y)
        ax.imshow(self.frame_test_gray)
        
        
        self.text=ax.text(0,0, "", va="bottom", ha="center")
        
    
    def onclick_rats(self, event):
        '''rat1 is on the left'''
            
        tx = 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f' % (
            event.button, event.x, event.y, event.xdata, event.ydata)
        
        self.text.set_text(tx)
                
        self.ix_rat, self.iy_rat = event.xdata, event.ydata
        
    
        #append coordinates of each rat to the list
        self.coords_rat.append((int(self.ix_rat), int(self.iy_rat)))
        
        #disconect it
        if len(self.coords_rat) == 4:
            self.fig.canvas.mpl_disconnect(self.cid_rats)
            
            #close when selected rectangles for both rats
            plt.close()
            
            #path2vid_test="C:/Users/domin/Documents/SCHOOL/STAGE2/motion_detection_4ephys/data/Basler_acA1300-60gmNIR__21471690__20211207_113623925_SHORT.mp4"
            motion_detector_MVMwriter(co = self.coords_rat, 
                                      scale_percent = self.scale_percent,
                                      fw = self.x, fh = self.y, #need for Writer object (not working)
                                      path = path2vid_test)
    
    def coord_extractor(self):
        self.cid_rats = self.fig.canvas.mpl_connect('button_press_event', self.onclick_rats)
        #plt.close()
        
        #plt.close()
        #print(self.coords_rat)
        #return self.coords_rat
        
rc = Rat_coords()
rc.shape_extractor(path2vid=path2vid_test)
rc.coord_extractor()



