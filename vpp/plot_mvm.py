import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_mvm(path,
             resample_freq = '1S', #you can set resampling freq: '1T' for 1 minute
             plot_all =True,
             start={"hours": 2, "minutes": 0, "seconds": 0},
             dt={"hours": 1, "minutes": 0, "seconds": 0},
             ylim=1,
             save=False):
    """read csv file from path and plot mvm """



    # timest_seconds_DAY=[i/(1000*60) for i in df["millisec"]]

    # import csv
    df = pd.read_csv(path,
                            sep=',', index_col="timestamp") #parse_dates=[2])
    #set duration as index
    df.index = pd.to_datetime(df['duration'])
    #drop duration as column
    df = df.drop('duration', axis = 1)
    #df['duration'] = pd.to_datetime(df['duration'])
    if resample_freq:
        df =  df.resample(resample_freq).mean()
    print(df.columns)
    

    #if you want to plot only a part 
    if not plot_all:
        # determine frames per sec number
        f = 1000 / (float(df["millisec"][1]) - float(df["millisec"][0]))
        
        # start and end coordinates depending on duration
        # calculate indexes
        h0 = start["hours"]
        m0 = start["minutes"]
        s0 = start["seconds"]
        h1 = start["hours"] + dt["hours"]
        m1 = start["minutes"] + dt["minutes"]
        s1 = start["seconds"] + dt["seconds"]
    
        start_st = int((f * h0 * 60 * 60) + (f * m0 * 60) + (f * s0))
        end_st = int((f * h1 * 60 * 60) + (f * m1 * 60) + (f * s1))
    
    #otherwise plot all (from index 0 to index -1)
    else:
        start_st = 0
        end_st = -1

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    ax1.plot(df.index[start_st:end_st],
             df["mvmr1_normalized"][start_st:end_st],
             label="rat_1")
    ax2.plot(df.index[start_st:end_st],
             df["mvmr2_normalized"][start_st:end_st],
             label="rat_2")
    for ax in [ax1, ax2]:
        #ax.set_ylim((0, ylim))
        ax.set_title("movement (pixel change)", fontsize=20)
        ax.set_xlabel("time", fontsize=16)
        ax.set_ylabel("sum of pixel change", fontsize=16)
        ax.tick_params(axis='x', labelrotation=60, labelsize=14)
        #ax.xaxis.set_major_locator(mdates.DateFormatter('%Y-%b-%%H-%M'))
        ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
        #ax.xaxis.set_major_locator(plt.AutoLocator())
        ax.legend()

    if save:
        plt.savefig(input("write the name of the plot") + ".png")
        
plot_mvm("/media/data-119/rat596_20210701_184333/acA1300-60gmNIR__21471690__20210701_184333372.csv", plot_all=False)