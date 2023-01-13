from math import floor
from bpsk_dsss.utils import get_repeated_bits_count


def sample_digital_signal(signal_bytes, sample_rate, symbol_rate, symbol_length_bits):
    repeated_bits_count = get_repeated_bits_count(sample_rate, symbol_rate, symbol_length_bits)

    signal = []
    for byte in signal_bytes:
        for n in range(symbol_length_bits):
            bit = (byte >> n) & 1
            for _ in range(repeated_bits_count):
                signal.append(bit)

    return signal


def upsample_signal(signal, factor):
    if floor(factor) != factor:
        raise Exception(f'Cannot upsample by rational factor: {factor}')

    output = []
    for sample in signal:
        for _ in range(factor):
            output.append(sample)

    return output


def bipolar_signal_to_binary(signal):
    return [1 if x > 0 else 0 for x in signal]

def decode_binary_signal_to_bit_probabilities(signal, sample_rate, symbol_rate, symbol_length_bits):
    repeated_bits_count = get_repeated_bits_count(sample_rate, symbol_rate, symbol_length_bits)

    bit_possibilities = []
    for i in range(len(signal)//repeated_bits_count):
        bit_value = 0
        for n in range(repeated_bits_count):
            value = signal[n + i*repeated_bits_count]
            if value > 0:
                bit_value += 1
        bit_value /= repeated_bits_count
        bit_possibilities.append(bit_value)

    return bit_possibilities

def get_bits_from_probabilities(probabilities, threshold=0.5):
    return [1 if x >= threshold else 0 for x in probabilities]


def get_symbols_from_bits(bits, symbol_length_bits):
    symbols = []

    total_possible_symbols = len(bits)//symbol_length_bits
    for i in range(total_possible_symbols):
        symbol_offset = i*symbol_length_bits

        symbol = 0
        for n in range(symbol_length_bits):
            bit_value = bits[n + symbol_offset]
            symbol |= bit_value << n

        symbols.append(symbol)

    return symbols

