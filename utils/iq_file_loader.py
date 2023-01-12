from struct import unpack
import numpy


def load_iq_file(file_path):
    samples = load_iq_file_as_interleaved_array(file_path)

    data = [ complex(x[0], x[1]) for x in zip(samples[0::2], samples[1::2]) ]

    return data


def load_iq_file_as_numpy(file_path):
    data = numpy.array(load_iq_file(file_path))

    return data


def load_iq_file_as_interleaved_array(file_path):
    f = open(file_path, 'rb')
    bytes = f.read(-1)
    f.close()

    samples = unpack('h' * (len(bytes) // 2), bytes)
    bytes = None

    return samples
