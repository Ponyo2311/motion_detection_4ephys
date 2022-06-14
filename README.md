# motion_detection_4ephys
- Create movement variable from camera recording 
- Manual selection of frame coordiantes for rats
- Real time plots
- Synchronize with ephys time using .npy output from Basler
<br>

<p align ="center">
    <img src = "https://user-images.githubusercontent.com/65451658/173108006-a974da64-965c-475d-93df-bd676d6a9d86.gif">
</p>
<br>

## 1) Setting up environment
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

## 2) Using Motion Detector
- clone this repo<br>

git clone https://github.com/Ponyo2311/motion_detection_4ephys.git<br>
<br>

- open spyder (with vidpenv activated)<br>

spyder<br>
<br>
!! The motion detector extracts the date from the name of the video, so don't change that one !!
1) open vpp/video_processing/getting_manual_coordinates_CLASS.py, change the directory to video (path2vid_test). This path contains the name of the file as well (ends with .mp4)<br>
<p align ="left">
    <img src = "https://user-images.githubusercontent.com/65451658/173512817-f8f72846-db3c-49ce-aa4f-fdcfc48b38be.png" width="800" height="150">
</p>
<br>
2) In vpp/video_processing/motion_detector_MVMwriter.py, change the directories where you'd like to safe the results.<br>
<p align ="left">
    <img src = "https://user-images.githubusercontent.com/65451658/172964457-05318e0b-9e4b-424f-9d85-d0b3cef93477.png"
         width="600" height="100">
</p>
<br>
- The outputs are a csv with timestamp, frame number, and movement for rat(s)  
- rat1 is always the rat on the left of the screen and rat 2 on the right.
- json file with coordinates of the frame (see below) you selected for the processing.<br>
3) When the directories are defined, run vpp/video_processing/getting_manual_coordinates_CLASS.py.<br>
4) When you click on RUN, there will be an image - first frame - displayed:<br>
<p align ="left">
    <img src = "https://user-images.githubusercontent.com/65451658/172965394-254f81a5-a4d8-4b45-8e5f-6cc7edac0ddd.png" width="600" height="400"><br>
- This is to select manually the frame for processing for each rat (to avoid overlapping in case of bad camera angle)
- the clicks should be in an order - from left to right, such as :<br>
<p align ="left">
    <img src = "https://user-images.githubusercontent.com/65451658/172965444-540613d7-ec12-4981-ae4e-f7c9c80ae584.png" width="600" height="400"><br>
- when you click 4 times, the picture will disappear and the detector is running.

## 3) Synchronizing + generation of .txt files:
+ Pipeline uses modules saved in vpp/utils<br>
+ applied in notebooks named 'Processing_Movement_*'<br>
+ in the example below, w627 is a path to folder where the (symlink) video and csv of the session are stored. 
+ TTL_2 folder is path to events folder, lfp_tmp_folder is path to lfp folder. 
+ This step would be possible to automatize, but the rat folders should be named by the full date of the session. 
+ !! it is made for file-tree, such that every session has it's own folder. !!<br>
![image](https://user-images.githubusercontent.com/65451658/172966213-b19340b7-abee-4ad3-9f3d-afb1004aedb5.png)

 ## 4) Plot code to finish 
 - removing too high values (produced by the light switch or the experimenter)
