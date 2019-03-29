
import matplotlib.pyplot as pltc
import numpy as np
import sensormotion.signal1
import sensormotion as sm
import pandas as pd
import os

from scipy.integrate import simps, trapz
dir = '../TrainingFiles'
NUM_OF_FILES = 1

for i in range(1,NUM_OF_FILES+1):
	df = pd.read_csv(os.path.join(dir,'Train_' + str(i) + '.csv'))
	
	x =df["load.txt.data.x"]

sampling_rate = 175.2  # number of samples per second
seconds = 10
time = np.arange(0, seconds*sampling_rate) * 10  # times in milliseconds


print(len(x))
print(len(time))
x_counts = sm.pa.convert_counts(x, time, integrate='trapezoid')
#y_counts = sm.pa.convert_counts(y, time, integrate='trapezoid')
#z_counts = sm.pa.convert_counts(z, time, integrate='trapezoid')
vm = sm.signal1.vector_magnitude(x_counts)
categories, time_spent = sm.pa.cut_points(vm, set_name='butte_preschoolers', n_axis=1)

def convert_counts(x, time, time_scale='s', epoch=60, rectify='full',
                   integrate='trapezoid', plot=True, fig_size=(12, 5)):

    assert len(x) == len(time), 'signal and time must be the same length'
    assert np.all(np.diff(time) > 0), 'time signal is not fully ascending'
    assert integrate == 'simpson' or integrate == 'trapezoid', \
        'integrate method must either be simpson or trapezoid'

    x = np.asarray(x)
    time = np.asarray(time)

    # convert time to seconds
    if time_scale == 'ms':
        time = time/1000
    elif time_scale == 's':
        time = time

    # calculate time diff
    time = time - time[0]

    assert max(time) > epoch, 'length of signal time shorter than epoch size'

    # rectify signal
    x = sensormotion.signal.rectify_signal(x, rectify)

    # interpolate missing times values to get exact epochs
    boundary_count = int(max(time) / epoch) + 1
    boundary_times = [i*epoch for i in range(boundary_count)]
    missing_times = np.setdiff1d(boundary_times, time)  # epoch times to interp

    x = np.append(x, np.interp(missing_times, time, x))  # interpolate x values
    time = np.append(time, missing_times)

    # sort new time and signal arrays together
    sort_idx = time.argsort()
    time = time[sort_idx]
    x = x[sort_idx]

    # get index of each epoch/boundary value for slicing
    boundary_idx = np.where(np.isin(time, boundary_times))[0]

    # integrate each epoch using Simpson's rule
    counts = np.ones(len(boundary_idx) - 1)  # preallocate array

    for i in range(len(counts)):
        lower = boundary_idx[i]
        upper = boundary_idx[i+1] + 1  # upper bound should be inclusive

        cur_signal = x[lower:upper]
        cur_time = time[lower:upper]

        if integrate == 'simpson':
            counts[i] = simps(cur_signal, cur_time)
        elif integrate == 'trapezoid':
            counts[i] = trapz(cur_signal, cur_time)

    # plot counts
    if plot:
        f, ax = pltc.subplots(1, 1, figsize=fig_size)

        ax.bar(boundary_times[1:], counts, width=epoch-5)

        pltc.xticks(boundary_times[1:],
                   ['{} - {}'.format(boundary_times[i], boundary_times[i+1])
                    for i, x in enumerate(boundary_times[1:])])

        for tick in ax.get_xticklabels():
            tick.set_rotation(45)

        pltc.suptitle('Physical activity counts', size=16)
        pltc.xlabel('Time window (seconds)')
        pltc.ylabel('PA count')
        pltc.show()

    return counts


def cut_points(x, freedson_adult, n_axis = 1, plot=True, fig_size=(10, 5)):
   

    # new cut-point sets should be added to this dictionary
    sets = {'butte_preschoolers': {1: {'sedentary': [-np.inf, 239],
                                       'light'    : [240, 2119],
                                       'moderate' : [2120, 4449],
                                       'vigorous' : [4450, np.inf]},
                                   3: {'sedentary': [-np.inf, 819],
                                       'light'    : [820, 3907],
                                       'moderate' : [3908, 6111],
                                       'vigorous' : [6112, np.inf]}
                                   },
            'freedson_adult'    : {1: {'sedentary'    : [-np.inf, 99],
                                       'light'        : [100, 1951],
                                       'moderate'     : [1952, 5724],
                                       'vigorous'     : [5725, 9498],
                                       'very vigorous': [9499, np.inf]},
                                   3: {'light'        : [-np.inf, 2690],
                                       'moderate'     : [2691, 6166],
                                       'vigorous'     : [6167, 9642],
                                       'very vigorous': [9643, np.inf]}
                                   },
            'freedson_children' : {1: {'sedentary'    : [-np.inf, 149],
                                       'light'        : [150, 499],
                                       'moderate'     : [500, 3999],
                                       'vigorous'     : [4000, 7599],
                                       'very vigorous': [7600, np.inf]}
                                   },
            'keadle_women'      : {1: {'sedentary': [-np.inf, 99],
                                       'light'    : [100, 1951],
                                       'moderate' : [1952, np.inf]},
                                   3: {'sedentary': [-np.inf, 199],
                                       'light'    : [200, 2689],
                                       'moderate' : [2690, np.inf]}
                                   }
            }

    try:
        cur_set = sets[set_name][n_axis]
        print('Cut-point set: {} (axis count: {})...'.format(set_name, n_axis))

        for i in cur_set:
            print('{}: {} to {}'.format(i, cur_set[i][0], cur_set[i][1]))
    except KeyError:
        print('Error: cut-point set not found. Make sure the set name and/or '
              'number of axes are correct')
        raise

    # categorize counts
    category = []
    for count in x:
        for intensity in cur_set:
            if cur_set[intensity][0] <= count <= cur_set[intensity][1]:
                category.append(intensity)
                break

    # count time spent
    category_unique, category_count = np.unique(category, return_counts=True)
    time_spent = np.asarray((category_unique, category_count))

    # plot counts with intensity categories
    if plot:
        boundaries = [(item, cur_set[item][0]) for item in cur_set]
        boundaries.sort(key=lambda x: x[1])

        f, ax = pltc.subplots(1, 1, figsize=fig_size)

        ax.bar(range(1, len(x)+1), x)

        for line in boundaries[1:]:
            if line[1] < max(x):
                pltc.axhline(line[1], linewidth=1, linestyle='--', color='k')
                t = pltc.text(0.4, line[1], line[0], backgroundcolor='w')
                t.set_bbox(dict(facecolor='w', edgecolor='k'))

        pltc.xticks(range(1, len(x)+1))

        pltc.suptitle('Physical activity counts and intensity', size=16)
        pltc.xlabel('Epoch (length: 60 seconds)')
        pltc.ylabel('PA count')
        pltc.show()

    return category, time_spent
