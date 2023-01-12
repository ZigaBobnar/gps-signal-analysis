from math import floor
from utils.sample_cutting import split_sample


file_path = '../2013_04_04_GNSS_SIGNAL_at_CTTC_SPAIN.tar/2013_04_04_GNSS_SIGNAL_at_CTTC_SPAIN/2013_04_04_GNSS_SIGNAL_at_CTTC_SPAIN.dat'
sampling_frequency = 4e6 # 4 Msps


# Get shorter sample
# output_path = './data/sample.dat'
# throwaway_first_samples = 1e3
# total_samples = 1e5
# split_sample(file_path, output_path, total_samples, throwaway_first_samples)


# Get the signal that contains at least 10 data bits for DSSS
data_rate = 50 # 50 bps
data_symbols = 10
throwaway_first_samples = floor(sampling_frequency*10e-3) # Remove first 5 ms
total_samples = floor((sampling_frequency / data_rate) * data_symbols)
output_path = f'./data/sample-{data_symbols}_data_symbols-{total_samples}_samples.dat'
split_sample(file_path, output_path, total_samples, throwaway_first_samples)

# Get the signal that contains at least 2 data bits for DSSS
data_rate = 50 # 50 bps
data_symbols = 2
throwaway_first_samples = floor(sampling_frequency*10e-3) # Remove first 5 ms
total_samples = floor((sampling_frequency / data_rate) * data_symbols)
output_path = f'./data/sample-{data_symbols}_data_symbols-{total_samples}_samples.dat'
split_sample(file_path, output_path, total_samples, throwaway_first_samples)

# Get the signal that contains at least 1 data bits for DSSS
data_rate = 50 # 50 bps
data_symbols = 1
throwaway_first_samples = floor(sampling_frequency*10e-3) # Remove first 5 ms
total_samples = floor((sampling_frequency / data_rate) * data_symbols)
output_path = f'./data/sample-{data_symbols}_data_symbols-{total_samples}_samples.dat'
split_sample(file_path, output_path, total_samples, throwaway_first_samples)
