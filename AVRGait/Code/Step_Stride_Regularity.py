
from __future__ import print_function, division

import numpy as np

import sensormotion as sm

import pandas as pd
import os


from scipy.integrate import simps, trapz
dir = '../TrainingFiles'
NUM_OF_FILES = 1

for i in range(1,NUM_OF_FILES+1):
	df = pd.read_csv(os.path.join(dir,'Train_' + str(i) + '.csv'))
	
	x =df["load.txt.data.x"]
	y =df["load.txt.data.y"]
	z =df["load.txt.data.z"]
	

sampling_rate = 175.2  # number of samples per second
seconds = 10
t = np.arange(0, seconds*sampling_rate) * 10  # times in milliseconds

b, a = sm.signal1.build_filter(frequency=10,
                              sample_rate=100,
                              filter_type='low',
                              filter_order=4)

x_filtered = sm.signal1.filter_signal(b, a, signal=x)

def step_regularity(autocorr_peak_values):

    peaks_half = autocorr_peak_values[autocorr_peak_values.size // 2 :]

    assert len(peaks_half) >= 3, (
        "Not enough autocorrelation peaks detected. Plot the "
        "autocorrelation signal to visually inspect peaks"
    )

    ac_lag0 = peaks_half[0]  # autocorrelation value at lag 0
    ac_d1 = peaks_half[1]  # first dominant period i.e. a step (left-right)
    ac_d2 = peaks_half[2]  # second dominant period i.e. a stride (left-left)

    step_reg = ac_d1 / ac_lag0
    stride_reg = ac_d2 / ac_lag0

    return step_reg, stride_reg
    print(step_reg)
    print(stride_reg)
    print("Hi")

peak_times, peak_values = sm.peak.find_peaks(time=t, signal=x_filtered,
                                             peak_type='valley',
                                             min_val=0.6, min_dist=30,
                                             plot=True)

step_reg, stride_reg = step_regularity(peak_values)


print(" ")
print("Step Regularity is:")
print(step_reg)
print(" ")
print("Stride Regularity is:")
print(stride_reg)



