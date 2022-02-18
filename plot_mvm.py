import pandas as pd
import matplotlib.pyplot as plt

def plot_mvm(path,
             start={"hours": 0, "minutes": 1, "seconds": 0},
             dt={"hours": 0, "minutes": 1, "seconds": 0},
             ylim=3 * 1e6,
             save=False):
    """read csv file from path and plot mvm """



    # timest_seconds_DAY=[i/(1000*60) for i in first_vid["millisec"]]

    # import csv
    first_vid = pd.read_csv(path,
                            sep='\t', index_col="timestamp", parse_dates=[2])

    # determine frames per sec number
    f = 1000 / (float(first_vid["millisec"][1]) - float(first_vid["millisec"][0]))

    # start and end coordinates depending on duration
    # (0 for start, 1 for end)
    h0 = start["hours"]
    m0 = start["minutes"]
    s0 = start["seconds"]
    h1 = start["hours"] + dt["hours"]
    m1 = start["minutes"] + dt["minutes"]
    s1 = start["seconds"] + dt["seconds"]

    start_st = int((f * h0 * 60 * 60) + (f * m0 * 60) + (f * s0))
    end_st = int((f * h1 * 60 * 60) + (f * m1 * 60) + (f * s1))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    ax1.plot(first_vid['duration'][start_st:end_st],
             first_vid["mvm_rat1"][start_st:end_st],
             label="rat_1")
    ax2.plot(first_vid['duration'][start_st:end_st],
             first_vid["mvm_rat2"][start_st:end_st],
             label="rat_2")
    for ax in [ax1, ax2]:
        ax.set_ylim((0, ylim))
        ax.set_title("movement (pixel change)", fontsize=20)
        ax.set_xlabel("time", fontsize=16)
        ax.set_ylabel("sum of pixel change", fontsize=16)
        ax.tick_params(axis='x', labelrotation=60, labelsize=14)
        ax.xaxis.set_major_locator(plt.AutoLocator())
        ax.legend()

    if save:
        plt.savefig(input("write the name of the plot") + ".png")