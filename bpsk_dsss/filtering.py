from scipy.signal import butter, lfilter


def low_pass_filter_butterworth(signal, sample_rate, order, cutoff_frequency):
    b, a = butter(order, cutoff_frequency, fs=sample_rate, btype='low', analog=False)
    return lfilter(b, a, signal)

