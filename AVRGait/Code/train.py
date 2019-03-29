import pandas as pd
import os
import os.path
import math
import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
from scipy.signal import argrelmax,find_peaks_cwt

from step_detector import *


#Global variables
dir = '../TrainingFiles'

summarySession = pd.read_csv(os.path.join(dir,"SessionsSummary.csv"))
true_steps_count= summarySession["StepsCounts"]
duplicateTrainFiles = range(14,27)

NUM_OF_FILES = 1
NUM_OF_SEC_BEFORE = 11.2
NUM_OF_SEC_AFTER = 0.2

displayGraph = True

##### Detect Step Count ######

total_errors = []
step_counts = []
for i in range(1,NUM_OF_FILES+1):

    # Read the file
    df = pd.read_csv(os.path.join(dir,'Train_' + str(i) + '.csv'))

    # Change column names, parse dates and create magnitude column
    df['x']=df["load.txt.data.x"]
    df['y']=df["load.txt.data.y"]
    df['z']=df["load.txt.data.z"]

    df['magnitude'] = df.apply(lambda row: math.sqrt((row.x)**2 + (row.y)**2 + (row.z)**2),axis=1)
    df['time']= pd.to_datetime(df['epoch'], format='%Y-%m-%d %H:%M:%S.%f')

    # Drop duplicates
    if i in duplicateTrainFiles:
        df = df.drop_duplicates(subset=['x','y','z']).reset_index(drop=True)

    # Get the number of steps
    # Calculate the samples per second in the dataframe
    samples_per_sec = calculate_num_of_sampling_per_sec(df)

    # Get only the relevant data points out of the data frame
    filtered_df = filter_noise(df,samples_per_sec)

    # Butterworth filter
    cutoff = 1.33
    b, a = butter_lowpass(cutoff, samples_per_sec)

    # Low filter
    magnitude_smoothed = lfilter(b, a, filtered_df.magnitude)

    # Get peaks
    peaks = argrelmax(magnitude_smoothed)[0]

    # Get peak values
    peak_values = magnitude_smoothed[peaks]

    t = np.linspace(0, 15.0, magnitude_smoothed.size, endpoint=False)

    error = ((len(peaks)) - (true_steps_count[i - 1])) ** 2

    total_errors.append(error)
    step_counts.append(len(peaks))
    print("{}: True number of steps: {}, Predicted: {}, Error Squared: {}".format(i, true_steps_count[i - 1], len(peaks), error))

    if displayGraph:
        plt.figure(figsize=(20,20))
        plt.plot(t, magnitude_smoothed, 'b-', linewidth=2)

        plt.plot(t[peaks], magnitude_smoothed[peaks], 'ro', linewidth=2)

        plt.show()


print("\t MSE for Step Count: {}".format(np.average(total_errors)))

