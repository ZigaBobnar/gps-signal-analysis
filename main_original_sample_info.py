from utils.sample_info import get_sample_info, print_sample_info


# Sample information:
# Name: 2013_04_04_GNSS_SIGNAL_at_CTTC_SPAIN
# Hardware: USRP 1.0 Rev 4.5 with DBSRX v2. Usung onboard local oscillator
# Capture Date: 2013/04/04,06:24:58 UTC
# Capture settings:
# - Sample size: Baseband IQ Interleaved Short (ishort)
# - Sampling frequency: 4.0 MSPS
# - Signal time: 100 seconds
# - Location: Roof of CTTC building (aproximatted coordinates 40.396764 N, 3.713379 E)
# - Antenna: Novatel GPS-600 active antenna

# Input file is in format of interleaved I and Q, every sample is 16-byte short with low-endianness
# Like this: I0, Q0, I1, Q1, I2, Q2, ...

file_path = '../2013_04_04_GNSS_SIGNAL_at_CTTC_SPAIN.tar/2013_04_04_GNSS_SIGNAL_at_CTTC_SPAIN/2013_04_04_GNSS_SIGNAL_at_CTTC_SPAIN.dat'
sampling_frequency = 4e6 # 4Msps

print_sample_info(get_sample_info(file_path, sampling_frequency))


# Results:
# File type: baseband_IQ_interleaved_short
# Channels count: 2
# Channel sample size: 2 bytes
# Bytes per full sample: 4 bytes (all channels combined)
# File size: 1600000000 bytes 1600000.0 kB, 1600.0 MB, 1.6 GB)
# Sampling frequency: 4000000.0 samples/sec (4000.0 ksps, 4.0 Msps)
# Calculated total samples: 400000000
# Calculated total duration: 100.0 seconds (1.67 minutes)



# Actual decoded data info (from GNSS-SDR):
# PRN, Doppler shift
# PRN-01, +7032 Hz
# PRN-11, +5474 Hz
# PRN-17, +9873 Hz
# PRN-20, +8284 Hz
# PRN-23, +10900 Hz
# PRN-32, +6384 Hz
# Available GPS sattelite PRNs: 01, 08, 11, 16, 17, 20, 23, 24, 32
