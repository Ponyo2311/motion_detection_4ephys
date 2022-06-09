# motion_detection_4ephys


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


**synchronizing + generation of .txt files:** 
+ Pipeline uses modules saved in vpp/utils<br>
+ applied in notebook named Processing_movement_*<br>
+ example for one session:
<br>
ASSIGN SESSION FOLDER
w627 = "/media/data-119/Maeva_mvm/Rat627/Rat627-20210715_2/"

1) CREATE SYNC FILE
syncFileCreator(TTL2_folder = "/media/data-102/2021-07-15_18-55-38/RecordNode101/experiment1/recording1/events/Neuropix-PXI-100.3/TTL_4/",
            lfp_tmp_folder = "/media/data-102/2021-07-15_18-55-38/RecordNode101/experiment1/recording1/continuous/Neuropix-PXI-100.3/",
            output_sync_txt = w627)

2) EXPORT MOVEMENT TO TXT
mvm2txt(glob.glob(w627+"*.csv")[0],
        path2vid = glob.glob(w627+"*.mp4")[0],
        path2ephysTime = glob.glob(w627+"*_sec.txt")[0],
        rat=1)

3) RESCALE NUMBER OF FRAMES
rescalingNOF(path2ephysTime = glob.glob(w627+"*_sec.txt")[0],
             path2mvm = glob.glob(w627+"*mvm.txt")[0],
             path2duration = glob.glob(w627+"*duration.txt")[0])
