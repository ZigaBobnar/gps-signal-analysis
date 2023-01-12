from bpsk_dsss.utils import get_repeated_bits_count
from math import floor


symbol_length_bits = 8 # bits per symbol
sample_rate = 4096 # samples per second
symbol_rate = 1 # symbols(characters) per second

modulation_carrier_frequency = 512
modulation_carrier_amplitude = 1

demodulation_filter_order = 6
demodulation_filter_cutoff_frequency = modulation_carrier_frequency/2

dsss_code_frequency = 128

original_signal_path = './data/test_bpsk_dsss.raw'
modulated_signal_path = './data/test_bpsk_dsss_modulated.raw'
decoded_signal_path = './data/test_bpsk_dsss_decoded.raw'

original_signal_data = 'Hello, World!'


# Test the configuration:
repeated_bits_count = get_repeated_bits_count(sample_rate, symbol_rate, symbol_length_bits)
