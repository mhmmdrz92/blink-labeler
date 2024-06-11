import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib.collections import LineCollection


def eegplot(eeg_data, srate, title, fig=None, block=False):
    """
    the function to plot eeg data
    :param eeg_data: get eeg data
    :param srate: sampling rate of eeg signal
    :param title: string of plot title
    :return: plot the data
    """
    eeg_data = np.array(eeg_data)
    eeg_data[:-1, :] = signal.detrend(eeg_data[:-1, :], axis=-1, type='linear')
    n_samples, n_rows = np.shape(eeg_data)[1], np.shape(eeg_data)[0]

    # normalize each column to be able to show
    for i in range(n_rows):
        eeg_data[i, :] = eeg_data[i, :] - np.mean(eeg_data[i, :])
        eeg_data[i, :] = eeg_data[i, :] / (np.std(eeg_data[i, :]) + 1)

    if fig is None:
        fig = plt.figure("EEG plot of {}".format(title))

    axes = plt.axes()
    # Load the EEG data
    data = np.transpose(eeg_data)
    t = np.arange(n_samples) / srate

    # Plot the EEG
    ticklocs = []
    axes.set_xlim(0, t.max())
    # ax2.set_xticks(np.arange(10))

    segs = []
    y1 = 0
    for i in range(n_rows):
        dmin = data[:, i].min()
        dmax = data[:, i].max()
        dr = (dmax - dmin)
        segs.append(np.column_stack((t, data[:, i])))
        ticklocs.append(y1)
        y1 = y1 + dr

    y0 = data[:, 0].min()
    axes.set_ylim(y0, y1)

    offsets = np.zeros((n_rows, 2), dtype=float)
    offsets[:, 1] = ticklocs

    colors = [mcolors.to_rgba(c)
              for c in plt.rcParams['axes.prop_cycle'].by_key()['color']]
    lines = LineCollection(segs, offsets=offsets, transOffset=None, linewidths=0.5,
                           colors=colors, linestyle='solid')
    axes.add_collection(lines)

    # Set the yticks to use axes coordinates on the y axis
    axes.set_yticks(ticklocs)

    ch_name_list = []
    for i in range(n_rows):
        ch_name_list.append('CH '+str(i))
    axes.set_yticklabels(ch_name_list)

    axes.set_xlabel('Time (s)')
    plt.suptitle(title)

    plt.tight_layout()
    # plt.show()
