
from __future__ import print_function, division

import numpy as np

import sensormotion.signal1
import sensormotion as sm
import pandas as pd
import os
"""
This part of the code is for randomly generated signal 
sampling_rate = 100  # number of samples per second
seconds = 60
t = np.arange(0, seconds*sampling_rate) * 20  # times in milliseconds

np.random.seed(123)

x = 2*np.sin(t/30) + np.random.normal(0.5, 0.4, len(t))  # ML medio-lateral
y = 4*np.sin(t/80) + np.random.normal(1.0, 0.5, len(t))  # VT vertical
z = 3*np.sin(t/90) + np.random.normal(0.0, 0.4, len(t))  # AP antero-posterior
"""

from scipy.integrate import simps, trapz
dir = '../TrainingFiles'
NUM_OF_FILES = 1

sampling_rate = 175.2  # number of samples per second
seconds = 10
t = np.arange(0, seconds*sampling_rate) * 10  # times in milliseconds

for i in range(1,NUM_OF_FILES+1):
	df = pd.read_csv(os.path.join(dir,'Train_' + str(i) + '.csv'))
	
	x =df["load.txt.data.x"]
	
	
b, a = sm.signal1.build_filter(frequency=10,
                              sample_rate=100,
                              filter_type='low',
                              filter_order=4)

x_filtered = sm.signal1.filter_signal(b, a, signal=x)

peak_times, peak_values = sm.peak.find_peaks(time=t, signal=x_filtered,
                                             peak_type='valley',
                                             min_val=0.6, min_dist=30,
                                             plot=False)

											 
step_mean, step_sd, step_cov = sm.gait.step_time(peak_times=peak_times)
print("	")
print("Mean timing between all steps during the workout in Milli Seconds")
print(step_mean) #mean timing between all steps and peaks


