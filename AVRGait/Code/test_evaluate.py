import pandas as pd
import os
import os.path
from os import listdir
from step_detector import *
from sklearn.externals import joblib

def get_step_count(df):
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

    return len(peaks)

def get_distance(df,peaks = None):
    if peaks == None:
        peaks = get_step_count(df)
    walking_distance_classifier = joblib.load('classifier.pkl')
    return walking_distance_classifier.predict(peaks)[0]

#Global variables
dir = '../TestingFiles'


summarySession = pd.read_csv(os.path.join(dir,"SessionsSummary.csv"))

for file in listdir(dir):

    if "SessionsSummary" not in file:
        print(file)

        # Read the file
        df = pd.read_csv(os.path.join(dir,file))

        # Change column names, parse dates and create magnitude column
        df['x']=df["load.txt.data.x"]
        df['y']=df["load.txt.data.y"]
        df['z']=df["load.txt.data.z"]

        df['magnitude'] = df.apply(lambda row: math.sqrt((row.x)**2 + (row.y)**2 + (row.z)**2),axis=1)
        df['time']= pd.to_datetime(df['epoch'], format='%Y-%m-%d %H:%M:%S.%f')

        ## Detect the number of steps ##
        step_count = get_step_count(df)

        ## Detect the walking distance ##
        walking_distance = get_distance(df,step_count)

        i = int(file.split("_")[1].split(".")[0])
        true_step_count = summarySession[summarySession.FileName == file.split(".")[0]].StepsCounts.values[0]
        true_distance = summarySession[summarySession.FileName == file.split(".")[0]].DistanceCovered.values[0]

        error_step = (step_count - (true_step_count)) ** 2
        error_distance = (walking_distance - (true_distance)) ** 2

        print("Steps: {}, Walking Distance: {}, Error Step: {}, Error Distance: {}".format(step_count,walking_distance,error_step,error_distance))


