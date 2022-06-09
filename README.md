# motion_detection_4ephys


<p align ="center">
    <img src = "https://user-images.githubusercontent.com/65451658/172929419-170e68ee-e738-4e90-bdd4-8a8042067ab4.gif">
</p>
<br>

<p align ="center">
    <img src = "https://user-images.githubusercontent.com/65451658/172926414-1a9c5103-29ff-405a-99e0-2b1184ac7db9.gif">
</p>
<br>


- Create movement variable from camera recording 
- Manual selection of frame coordiantes for rats
- Real time plots
- Synchronize with ephys time using .npy output from Basler

Remarks:
- Install opencv with pip: pip install opencv-python (bugs if installing through conda)
- create virtenv (or conda env) with python version < 3.10 (worked with 3.9 on mercury, and 3.7 on Hubel)


To do:
- save processed as .mp4
