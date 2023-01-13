from bpsk_dsss.utils import get_repeated_bits_count
from math import floor, log10


symbol_length_bits = 8 # bits per symbol
sample_rate = 32768 # samples per second
symbol_rate = 1 # symbols(characters) per second
sample_rate_power = round(log10(sample_rate))

modulation_carrier_frequency = 128
modulation_carrier_amplitude = 1

demodulation_filter_order = 6
demodulation_filter_cutoff_frequency = modulation_carrier_frequency/2

dsss_code_frequency = 32

original_signal_path = './data/test_bpsk_dsss.raw'
modulated_signal_path = './data/test_bpsk_dsss_modulated.raw'
decoded_signal_path = './data/test_bpsk_dsss_decoded.raw'
results_path = './data/results/'

# original_signal_data = 'Hello, World!'
original_signal_data = 'Prenosni sistemi'


plot_subsample_start = floor(1e4)
plot_subsample_length = floor(1e5)/4
plot_subsample_end = floor(plot_subsample_start + plot_subsample_length)
plot_subsample_downsample_factor = 1
plot_filetype = '.svg'
# plot_filetype = '.png'

# Test the configuration:
repeated_bits_count = get_repeated_bits_count(sample_rate, symbol_rate, symbol_length_bits)

noise_amplitude = 8
