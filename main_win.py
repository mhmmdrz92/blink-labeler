from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

from plot import eegplot


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('ui/main.ui', self)

        self.setWindowTitle('Artifact Labeler')
        self.setWindowIcon(QIcon('ui/logo.png'))
        self.connector()
        self.ui_setup()
        self.data = None
        self.srate = None
        self.gain = None
        self.figure = None
        self.canvas = None
        self.widget = None
        self.x_axis = None
        self.start = None
        self.end = None
        self.file_name = None
        self.labeled_data = []
        self.win = 0.3
        self.overlap = 0
        self.ch_index = 0
        os.makedirs('results', exist_ok=True)

    def ui_setup(self):
        self.show()

    def connector(self):
        self.btn_browse.clicked.connect(self.browse_file)
        self.btn_start.clicked.connect(self.start_labelling)
        self.btn_oa.clicked.connect(self.labelling)
        self.btn_noa.clicked.connect(self.labelling)
        self.btn_back.clicked.connect(self.correction)

    def browse_file(self):
        fileaddress, _ = QFileDialog.getOpenFileName(None, "csv file", filter='*.csv')
        if fileaddress:
            self.txt_path.setText(fileaddress)
            self.txt_path.setEnabled(False)
            self.btn_start.setEnabled(True)
            self.file_name = fileaddress.split('/')[-1].split('.')[0]

    def start_labelling(self):
        try:
            self.btn_browse.setEnabled(False)
            self.btn_start.setEnabled(False)
            self.btn_back.setEnabled(False)
            data = np.loadtxt(self.txt_path + '.csv', delimiter=',', dtype=np.float32)
            self.srate = int(self.spinBox_fs.value())
            if self.srate > 256:
                data = self.resample(data)
                self.srate = 256

            # eegplot(data[0:2, :], srate, 'EEG')

            filters = self.design_filters(self.srate)
            data = signal.filtfilt(filters['notch1'][0], filters['notch1'][1], data)
            data = signal.filtfilt(filters['notch2'][0], filters['notch2'][1], data)
            data = signal.filtfilt(filters['bandpass'][0], filters['bandpass'][1], data)

            # eegplot(data[0:2, :], srate, 'EEG')

            self.data = data  # - np.mean(data)
            self.data = self.data[[0, 1], :]
            # self.gain = 1
            self.make_data()
        except Exception as e:
            print('start_labelling', e)

    def make_data(self):
        try:
            i = self.overlap
            if i * self.win * self.srate + self.win * self.srate > self.data.shape[1]:
                print('Maximum len reached')
                self.ch_index += 1
                self.overlap = 0
                i = 0
                # if self.ch_index > 2:
                if self.ch_index > 1:
                    print('finished')
                    self.finishing()
                    return

            self.start = int(i * self.win * self.srate)
            self.end = int(i * self.win * self.srate + self.win * self.srate)
            # print(self.ch_index, self.start, self.end)
            window_data = self.data[self.ch_index, self.start: self.end]
            self.x_axis = np.arange(self.start, self.end)

            self.plot(window_data)
        except Exception as e:
            print('make_data', e)

    def plot(self, data):
        try:
            self.clear_layout(self.lyt_plot)
            plt.close(self.figure)
            self.figure = plt.figure()
            self.canvas = FigureCanvasQTAgg(self.figure)
            self.canvas.setContentsMargins(0, 0, 0, 0)
            self.widget = QWidget()
            self.widget.setContentsMargins(0, 0, 0, 0)

            layout = QVBoxLayout()
            layout.setSpacing(0)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(self.canvas)
            self.widget.setLayout(layout)
            self.widget.setMinimumSize(400, 400)
            self.lyt_plot.addWidget(self.widget)

            ax = self.figure.add_subplot(111)
            # data = data / self.gain
            # data -= np.mean(data)
            data = signal.detrend(data)
            plt.ylim([-200, 200])
            ax.axhline(y=80, color='r', linestyle='-')
            ax.axhline(y=-80, color='r', linestyle='-')
            ax.set_aspect(0.5)
            ax.plot(self.x_axis, data)
            ax.set_xlabel('Samples')
            ax.set_ylabel('Amplitude (uV)')
            self.canvas.draw()

            self.btn_oa.setEnabled(True)
            self.btn_noa.setEnabled(True)
            self.btn_back.setEnabled(True)
        except Exception as e:
            print('plot', e)

    def labelling(self):
        try:
            self.btn_oa.setEnabled(False)
            self.btn_noa.setEnabled(False)
            self.btn_back.setEnabled(False)
            sender = self.sender().objectName()
            ch_index = self.ch_index
            if ch_index == 2:
                ch_index = 16
            if sender == 'btn_oa':
                print('Ch:', ch_index+1, '--', '[', self.start, self.end, ']', '->', 'OA.')
                self.labeled_data.append([ch_index, self.start, self.end, 1])
            else:
                print('Ch:', ch_index+1, '--', '[', self.start, self.end, ']', '->', 'NOA.')
                self.labeled_data.append([ch_index, self.start, self.end, 0])
            self.overlap += 0.5
            self.make_data()
        except Exception as e:
            print('labelling', e)

    def correction(self):
        try:
            self.labeled_data.pop(-1)
            self.overlap -= 0.5
            self.make_data()
        except Exception as e:
            print(e)

    def finishing(self):
        try:
            self.clear_layout(self.lyt_plot)
            with open('results/' + self.file_name + '.txt', 'w') as f:
                for item in self.labeled_data:
                    f.write("%s\n" % item)
            self.data = None
            self.srate = None
            self.figure = None
            self.canvas = None
            self.widget = None
            self.x_axis = None
            self.start = None
            self.end = None
            self.file_name = None
            self.labeled_data = []
            self.overlap = 0
            self.ch_index = 0
            self.btn_browse.setEnabled(True)
        except Exception as e:
            print('finishing', e)

    def resample(self, data):
        data = np.array(data)
        signals = data.transpose()
        new_rate = 256
        number_of_samples = round(signals.shape[0] * float(new_rate) / self.srate)
        resampled = np.zeros((number_of_samples, signals.shape[1]))
        for ch in range(signals.shape[1]):
            resampled[:, ch] = signal.resample(signals[:, ch], number_of_samples)
        return resampled.transpose().tolist()

    @staticmethod
    def design_filters(s_rate):
        filters = {}
        output = signal.butter(N=5, Wn=np.array([45, 55]), btype='bandstop', analog=False, output='ba', fs=s_rate)
        filters['notch1'] = [output[0], output[1]]  # b, a
        output = signal.butter(N=5, Wn=np.array([95, 105]), btype='bandstop', analog=False, output='ba', fs=s_rate)
        filters['notch2'] = [output[0], output[1]]  # b, a
        output = signal.butter(N=5, Wn=np.array([0.53, 32]), btype='bandpass', analog=False, output='ba', fs=s_rate)
        filters['bandpass'] = [output[0], output[1]]  # b, a
        return filters

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())
