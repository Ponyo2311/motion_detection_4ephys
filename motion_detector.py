import pandas as pd
import cv2
from datetime import timedelta, datetime
import re
import os
import numpy as np


def csv_name_creator(path, output_folder="/home/domi/Documents/video_processing/CSV_data"):
    """path: folder+ file_name of the video
    output_folder: where all the csv files should be stored
    return:- a string path as input for pandas 'to_csv()' fun
           - timestamp of the exact date&time of the beginning of the recording"""

    # extract name of the video
    try:
        found = re.search('Basler_(.+?).mp4', path).group(1)
    except AttributeError:
        # AAA, ZZZ not found in the original string
        found = ''  # apply your error handling------------------------

    try:
        date = re.search('__[0-9]+__(.+?)[0-9]{3}.mp4', path).group(1)
    except AttributeError:
        # AAA, ZZZ not found in the original string
        date = ''  # apply your error handling------------------------

    millisec = int(re.findall('(\d{3})(?!.*\d)', found)[0])

    # check whether the folder where you want to save it in exist, if not create it
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)

    # new path
    new_path = os.path.join(output_folder, found + ".csv")

    # Date-time beginning of timestamp
    # first_date=pd.to_datetime(''.join(re.findall('[0-9]+', date)))
    first_date = ''.join(re.findall('[0-9]+', date))
    first_stamp = pd.Timestamp(first_date) + timedelta(milliseconds=millisec)

    return new_path, first_stamp


# Frames per second counter
class FPS:
    def __init__(self):
        """store the start time, end time, and total number of frames
        that were examined between the start and end intervals"""

        self._start = None
        self._end = None
        self._numFrames = 0

    def start(self):
        # start the timer
        self._start = datetime.now()
        return self

    def stop(self):
        # stop the timer
        self._end = datetime.now()

    def update(self):
        # increment the total number of frames examined during the
        # start and end intervals
        self._numFrames += 1

    def elapsed(self):
        # return the total number of seconds between the start and
        # end interval
        return (self._end - self._start).total_seconds()

    def fps(self):
        # compute the (approximate) frames per second
        return self._numFrames / self.elapsed()


def resizing(frame, scale_percent=50):
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    return resized


def timestamping(ts_dict, frame_nb, millisec):
    """Change to pandas data frame in the end"""

    ts_dict["frame_nb"].append(int(frame_nb))
    ts_dict["millisec"].append(millisec)
    return ts_dict


def motion_detector(path, scale_percent=40, area=20, delta_thresh=5,
                    output_4csv="/home/domi/Documents/video_processing/CSV_data"):
    """
    path: path to the video
    area: minimum area size.... TO INCLUDE!!!"""

    # read from a video file & initiate FramePerSec (FPS) count
    vs = cv2.VideoCapture(path)
    fps = FPS().start()

    # initialize average frame, frame delta and thresholded frame
    avgframe = [[], []]
    frameDelta = [[], []]
    thresh = [[], []]

    # initiate dictionary
    ts_dict = {"frame_nb": [], "millisec": [], "mvm_rat1": [], "mvm_rat2": []}

    # initiate dimensions for splitting
    # n_rows=1
    n_cols = 2  # 2 rats = 2 parts split with a vertical line
    # division in the middle

    # loop over the frames of the video
    n = 0
    while True:
        ret, frame = vs.read()  # ret says whether the frame exists

        if frame is None:
            break  # end of video if no more frames

        # get timestamp of each frame...
        frame_nb = n
        millisec = str(vs.get(cv2.CAP_PROP_POS_MSEC))  # in millisecond
        ts_dict = timestamping(ts_dict=ts_dict,
                               frame_nb=frame_nb,
                               millisec=millisec)

        n += 1
        # resize the frame, convert it to grayscale, and blur it
        frame = resizing(frame=frame, scale_percent=scale_percent)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # get gray's shape for splitting............................................
        height, width = gray.shape

        # divide the frame and calculate background and change for each part
        for i in range(n_cols):
            tmp_img = gray[0:height, int(i * width / 2): int((i + 1) * width / 2)]  # take all hight and half of width

            # initialize average frame (=background)
            if len(avgframe[i]) == 0:
                avgframe[i] = tmp_img.copy().astype("float")

            # update average & calculate difference between current and running avg
            cv2.accumulateWeighted(tmp_img, avgframe[i], 0.5)
            frameDelta[i] = cv2.absdiff(tmp_img,
                                        cv2.convertScaleAbs(avgframe[i]))

            # threshold the delta image, dilate the thresholded image to fill
            # in holes, then find contours on thresholded image
            thresh[i] = cv2.threshold(frameDelta[i], delta_thresh, 255,
                                      cv2.THRESH_BINARY)[1]
            thresh[i] = cv2.dilate(thresh[i], None, iterations=1)  # spread the white pixels

        # append mvm count for each rat
        for i in range(2):
            ts_dict[f"mvm_rat{i + 1}"].append(np.sum(thresh[i]))

        # update FPS counter
        fps.update()

        # DISPLAY VIDEOS (IT'S 2x LONGER THIS WAY... 92:177 FPS)!!!
        # cv2.imshow("webcam", frame)
        # cv2.imshow("Thresh_rat1", thresh[0])
        # cv2.imshow("Thresh_rat2", thresh[1])
        # cv2.imshow("Frame Delta_rat2", frameDelta[1])

        # cv2.waitKey(1)
        keyboard = cv2.waitKey(1)
        if keyboard == 'q' or keyboard == 27:
            break

        # testing, remove after...................................................................................
        # if n > 25 * 60 * 1:
        #    cv2.destroyAllWindows()
        #    newpath, first_stamp = csv_name_creator(path, output_folder=output_4csv)
        #    ts_df = pd.DataFrame(ts_dict)

        #    ts_df['duration'] = [timedelta(milliseconds=float(i)) for i in ts_df['millisec']]
        #    ts_df['duration'] = ts_df['duration'].values.astype('datetime64[ns]')
        #    ts_df['duration'] = [i.strftime("%H:%M:%S.%f")[:-3] for i in ts_df['duration']]

        #    ts_df['timestamp'] = [pd.to_timedelta(str(i) + 'millisecond') +
        #                          first_stamp for i in ts_df['millisec']]
        #    ts_df.set_index('timestamp', inplace=True)

        #   order = [0, 1, 4, 2, 3]  # setting column's order
        #  ts_df = ts_df[[ts_df.columns[i] for i in order]]

        # ts_df.to_csv(csv_name_creator(path, output_folder=output_4csv)[0], sep='\t')

        # stop the timer and display FPS information
        # fps.stop()
        # print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        # print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

        # return the df with timestamp+mvm count
        # return ts_df..........................................................................................

    # stop the timer and print Frame Per Sec info
    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # CLEAN UP
    cv2.destroyAllWindows()

    # get path for csv output & init of timestamp (extracted from the video filename)
    newpath, first_stamp = csv_name_creator(path, output_folder=output_4csv)

    # convert dict do pandas data frame...
    ts_df = pd.DataFrame(ts_dict)

    # create column 'duration' (millisec converted to time)
    ts_df['duration'] = [timedelta(milliseconds=float(i)) for i in ts_df['millisec']]
    # to keep only the time of the timedelta (otherwise give you estimate with days as well)
    ts_df['duration'] = ts_df['duration'].values.astype('datetime64[ns]')
    ts_df['duration'] = [i.strftime("%H:%M:%S.%f")[:-3] for i in ts_df['duration']]

    # ...set exact datetime timestamp (adding the first stamp to milliseconds)...
    ts_df['timestamp'] = [pd.to_timedelta(str(i) + 'millisecond') +
                          first_stamp for i in ts_df['millisec']]
    ts_df.set_index('timestamp', inplace=True)

    order = [0, 1, 4, 2, 3]  # setting columns' order
    ts_df = ts_df[[ts_df.columns[i] for i in order]]

    # ...and save it to info directory
    ts_df.to_csv(newpath, sep='\t')
    # return ts_df


# executable motion_detector
#TO REPAIR ARGS!!
if __name__ == "__main__":
    import sys

    motion_detector(sys.argv[1], output_4csv=NEWPATH)  # sys.argv[1] is path; sys.argv[0] is the name of the script.

import sys
