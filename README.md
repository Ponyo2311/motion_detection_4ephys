# motion_detection_4ephys


<p align ="center">
    <img src = "https://user-images.githubusercontent.com/65451658/172926414-1a9c5103-29ff-405a-99e0-2b1184ac7db9.gif">
</p>
<br>


- Create movement variable from camera recording 
- Manual selection of frame coordiantes for rats
- Real time plots
- Synchronize with ephys time using .npy output from Basler

# 1) Setting up environment
conda update conda<br>
conda create --no-default-packages -n vidpenv python=3.7 anaconda<br>
conda activate vidpenv<br>
pip install jupyterlab<br>
pip install ipykernel<br>
python -m ipykernel install --user --name=vidpenv<br>
pip install opencv-python<br>

+ verify list of environements available in Jupyter (vidpenv should appear there)

jupyter kernelspec list<br>

+ instal spyder (if not installed yet)

conda install spyder<br>

# 2) Using Motion Detector
!! The motion detector extracts the date from the name of the video, so don't change that one !!
1) open vpp/video_processing/getting_manual_coordinates_CLASS.py, change the directory to video (path2vid_test). This path contains the name of the file as well (ends with .mp4)
![image](https://user-images.githubusercontent.com/65451658/172963982-5c3b57b2-940b-4d8c-80d6-e58e019f3b0b.png)

3) In vpp/video_processing/motion_detector_MVMwriter.py, change the directories where you'd like to safe the results.
- The outputs are a csv with timestamp, frame number, and movement for rat(s)  
- rat1 is always the rat on the left of the screen and rat 2 on the right.
- json file with coordinates of the frame (see below) you selected for the processing.
4) When the directories are defined, run vpp/video_processing/getting_manual_coordinates_CLASS.py.
5) When you click on RUN, there will be an image - first frame - displayed:
- This is to select manually the frame for processing for each rat (to avoid overlapping in case of bad camera angle)
- the clicks should be in an order - from left to right, such as :
- when you click 4 times, the picture will disappear and the detector is running.

# 3) Synchronizing + generation of .txt files:
+ Pipeline uses modules saved in vpp/utils<br>
+ applied in notebooks named 'Processing_Movement_*'<br>

