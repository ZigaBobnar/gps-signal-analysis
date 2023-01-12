from bpsk_dsss import settings
from math import floor

repeated_bits_count = settings.sample_rate/settings.symbol_rate/settings.symbol_length

if floor(repeated_bits_count) != repeated_bits_count:
    print(f'Not supported: bit repeats count is not an integer number! {repeated_bits_count}')
    exit(-1)
repeated_bits_count = floor(repeated_bits_count)


f = open(settings.original_signal_path, 'rb')
signal_bits_as_bytes = f.read()
f.close()


signal_buffer = bytearray()

signal_data = ''
total_possible_symbols = floor(len(signal_bits_as_bytes)/settings.symbol_length/repeated_bits_count)
for j in range(total_possible_symbols):
    symbol_offset = j*repeated_bits_count*settings.symbol_length

    symbol = 0
    bit_probabilities = []
    for n in range(settings.symbol_length):
        bit_offset = symbol_offset + n*repeated_bits_count

        bit_value = 0
        for i in range(repeated_bits_count):
            bit_value += signal_bits_as_bytes[bit_offset+i]

        bit_probability = bit_value/repeated_bits_count
        bit_value = (1 if bit_probability >= 0.5 else 0) & 1

        bit_probabilities.append(bit_probability)
        symbol |= bit_value << n

    print(f'{bit_probabilities} => {symbol}\t= \'{chr(symbol)}\'')
    signal_data += chr(symbol)


print(signal_data)
