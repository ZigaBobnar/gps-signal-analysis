from utils.sample_info import get_sample_info


def split_sample(input_path, output_path, num_samples, offset_samples=0):
    info = get_sample_info(input_path, sampling_frequency=1)

    offset_bytes = round(info['bytes_per_full_sample']*offset_samples)
    keep_bytes = round(info['bytes_per_full_sample']*num_samples)

    f = open(input_path, 'rb')
    f.seek(offset_bytes)
    new_file_content = f.read(keep_bytes)
    f.close()

    f = open(output_path, 'wb')
    f.write(new_file_content)
    f.close()
