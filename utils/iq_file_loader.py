from struct import unpack


def load_iq_file(file_path):
    f = open(file_path, 'rb')
    bytes = f.read(-1)
    f.close()

    samples = unpack('h' * (len(bytes) // 2), bytes)
    bytes = None

    data = [ complex(x[0], x[1]) for x in zip(samples[0::2], samples[1::2]) ]

    return data
