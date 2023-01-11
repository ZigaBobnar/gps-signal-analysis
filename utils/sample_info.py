import os


# .dat format -> baseband IQ interleaved short
def get_sample_info(file_path, sampling_frequency):
    extension = os.path.splitext(file_path)[1]
    if extension == '.dat' or extension == '.bbnd_iq_short':
        file_type = 'baseband_IQ_interleaved_short'
        sample_channels = 2
        channel_sample_size_bytes = 2
    else:
        raise Exception(f'Unsupported sample file type! (extension {extension} not recognized)')

    bytes_per_full_sample = sample_channels*channel_sample_size_bytes

    fstat = os.stat(file_path)
    file_size_bytes = fstat.st_size

    total_samples_count = round(file_size_bytes/bytes_per_full_sample)
    total_duration_seconds = total_samples_count/sampling_frequency

    return {
        'file_type': file_type,
        'sample_channels': sample_channels,
        'channel_sample_size_bytes': channel_sample_size_bytes,
        'bytes_per_full_sample': bytes_per_full_sample,
        'file_size_bytes': file_size_bytes,
        'sampling_frequency': sampling_frequency,
        'total_samples_count': total_samples_count,
        'total_duration_seconds': total_duration_seconds,
    }


def print_sample_info(info):
    print(f'File type: {info["file_type"]}')
    print(f'Channels count: {info["sample_channels"]}')
    print(f'Channel sample size: {info["channel_sample_size_bytes"]} bytes')
    print(f'Bytes per full sample: {info["bytes_per_full_sample"]} bytes (all channels combined)')
    print(f'File size: {info["file_size_bytes"]} bytes {info["file_size_bytes"]/1000} kB, {info["file_size_bytes"]/1000/1000} MB, {info["file_size_bytes"]/1000/1000/1000} GB)')
    print(f'Sampling frequency: {info["sampling_frequency"]} samples/sec ({info["sampling_frequency"]/1000} ksps, {info["sampling_frequency"]/1000/1000} Msps)')
    print(f'Calculated total samples: {info["total_samples_count"]}')
    print(f'Calculated total duration: {info["total_duration_seconds"]} seconds ({round(info["total_duration_seconds"]/60, 2)} minutes)')
