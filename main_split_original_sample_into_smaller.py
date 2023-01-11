from utils.sample_cutting import split_sample


file_path = '../2013_04_04_GNSS_SIGNAL_at_CTTC_SPAIN.tar/2013_04_04_GNSS_SIGNAL_at_CTTC_SPAIN/2013_04_04_GNSS_SIGNAL_at_CTTC_SPAIN.dat'
output_path = './data/sample.dat'
throwaway_first_samples = 1e3
total_samples = 1e5

split_sample(file_path, output_path, total_samples, throwaway_first_samples)
