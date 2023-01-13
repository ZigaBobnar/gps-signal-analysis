from math import floor


def get_repeated_bits_count(sample_rate, symbol_rate, symbol_length_bits):
    repeated_bits_count = sample_rate/symbol_rate/symbol_length_bits

    if floor(repeated_bits_count) != repeated_bits_count:
        print(f'Not supported: bit repeats count is not an integer number! {repeated_bits_count}')
        exit(-1)
    repeated_bits_count = floor(repeated_bits_count)

    return repeated_bits_count

def write_bit_signal(file_path, signal):
    buffer = bytearray()
    for x in signal:
        buffer.append(x)

    f = open(file_path, 'wb')
    f.write(buffer)
    f.close()

def write_byte_signal(file_path, signal):
    buffer = bytearray()
    for x in signal:
        buffer.append(x & 0xFF)

    f = open(file_path, 'wb')
    f.write(buffer)
    f.close()
