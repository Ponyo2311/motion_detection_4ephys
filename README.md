# motion_detection_4ephys


![ratsgif](https://user-images.githubusercontent.com/65451658/172926414-1a9c5103-29ff-405a-99e0-2b1184ac7db9.gif)


- Create movement variable from camera recording 
- Manual selection of frame coordiantes for rats
- Real time plots
- Synchronize with ephys time using .npy output from Basler

Remarks:
- Install opencv with pip: pip install opencv-python (bugs if installing through conda)
- create virtenv (or conda env) with python version < 3.10 (worked with 3.9 on mercury, and 3.7 on Hubel)


To do:
- save processed as .mp4
