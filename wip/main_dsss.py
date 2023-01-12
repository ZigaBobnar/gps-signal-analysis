from math import floor, pi, sin
from utils.prn_codes import create_G2i_code
from utils.iq_file_loader import load_iq_file, load_iq_file_as_interleaved_array, load_iq_file_as_numpy
import pylab as plt
import numpy as np
from numpy import fft
from scipy.signal import periodogram, welch, correlate, correlation_lags

import matplotlib.pyplot as plt
from matplotlib import rcParams


sample_rate = 4e6 # 4 Msps
data_sample_rate = 50 # 50 bps
samples_count_for_data_sample = floor(sample_rate/data_sample_rate)
prn_frequency = 1.023e6
samples_count_for_prn_sample = round(sample_rate/prn_frequency) # TODO! Possible source of error - rounding 3.91 to 4!!

prn_id = 20
code_frequency = prn_frequency / 1023
# code_frequency = 1023e3


# f = 154*10.23e6 # Carrier frequency
# sample_rate = 1.0e-11

# signal = load_iq_file_as_numpy('./data/sample-10_data_symbols-800000_samples.dat')
# signal = load_iq_file_as_numpy('./data/sample-2_data_symbols-160000_samples.dat')
# signal = load_iq_file_as_numpy('./data/sample-1_data_symbols-80000_samples.dat')
# signal = load_iq_file('./data/sample-xl.dat')
# signal = [x*10 for x in signal] # Signal amplification

# De-complexing the signal:
signal = load_iq_file_as_interleaved_array('./data/sample-1_data_symbols-80000_samples.dat')
signal = [ x[0] + x[1] for x in zip(signal[0::2], signal[1::2]) ]

length = len(signal)


g2i = [1 if x else 0 for x in create_G2i_code(prn_id)] # 0, 1
g2i_ask = [-1 if x==0 else 1 for x in g2i] # -1, 1

g2i_samples = np.array([x for x in g2i_ask])*10
g2i_samples = np.repeat(g2i_samples, samples_count_for_prn_sample)
# g2i_samples = np.tile(g2i_samples, floor(length/samples_count_for_prn_sample/1023))


# Perform the correlation within single code interval (shift code)
code_length = len(g2i)
code_symbol_length_in_samples = sample_rate/code_frequency
code_length_in_samples = round(code_symbol_length_in_samples*code_length)
sample_time = 1/sample_rate


samples_for_convolution = code_length_in_samples*1

fig, ax = plt.subplots(3)

# ax[0].clear()
# ax[1].clear()
# ax[2].clear()

ax[0].plot(signal)
ax[1].plot(g2i_samples)
# ax[1].plot(correlations)
# ax[2].plot(signal_sample_decode)

# plt.pause(0.1)


# correlation = correlate(signal, g2i_samples, mode='valid', method='fft')
correlation = correlate(signal, g2i_samples, mode='valid', method='fft')
# correlation /= np.max(correlation) # Normalization
lags = correlation_lags(len(g2i_samples), len(signal))


print(correlation)
ax[2].plot(correlation)
print(f'Max correlation: {np.max(correlation)}')

plt.show()
exit()

if True:
# for sample_offset in range(len(signal)//samples_for_convolution):
    # signal_sample = signal[sample_offset+samples_for_convolution//2 : sample_offset+samples_for_convolution//2 + samples_for_convolution]
    signal_sample = signal

    correlations = []
    max_c = 0
    max_n = 0

    for n in range(len(g2i)):
        correlation = 0

        # for i in range(samples_for_convolution):
        #     code_position = round(i//code_symbol_length_in_samples+n) % code_length

        #     correlation += abs(signal_sample[i]*g2i[code_position])*sample_time

        correlation = sum([abs(signal_sample[i]*g2i[round(i//code_symbol_length_in_samples+n) % code_length])*sample_time for i in range(samples_for_convolution)])

        correlations.append(correlation)

        if correlation > max_c:
                max_c = correlations[n]
                max_n = n


    print(f'max_correlation: {max_c}, {max_n}')
    # signal_sample_decode = [signal_sample[i] for i in range(samples_for_convolution)]
    signal_sample_decode = [(signal_sample[i]*g2i_ask[round(i//code_symbol_length_in_samples+max_n) % code_length]) for i in range(samples_for_convolution)]
    # print(signal_sample_decode)

    ax[0].clear()
    ax[1].clear()
    ax[2].clear()

    ax[0].plot(g2i_samples)
    ax[0].plot(signal_sample)
    ax[1].plot(correlations)
    ax[2].plot(signal_sample_decode)

    plt.pause(0.1)


plt.show()
