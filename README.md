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

+ verify list of environements available in Jupyter (vidpenv should appear there)<br>
jupyter kernelspec list<br>

+ instal spyder (if not installed yet)<br>
conda install spyder<br>

# 2) Using Motion Detector


# 3) Synchronizing + generation of .txt files:
+ Pipeline uses modules saved in vpp/utils<br>
+ applied in notebooks named 'Processing_Movement_*'<br>

