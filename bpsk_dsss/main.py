from bpsk_dsss.dsss import despread_signal, spread_signal
from bpsk_dsss.filtering import low_pass_filter_butterworth
from bpsk_dsss.bpsk import demodulate_signal, modulate_signal
from bpsk_dsss.utils import show_plot
from bpsk_dsss import settings
from bpsk_dsss.digital_signal import bipolar_signal_to_binary, decode_binary_signal_to_bit_probabilities, get_bits_from_probabilities, get_symbols_from_bits, sample_digital_signal


###
# Original data signal sampling
###

original_signal_bytes = settings.original_signal_data.encode('ascii')
print(f'Transmitting:\t{[x for x in original_signal_bytes]}')
sampled_original_signal = sample_digital_signal(original_signal_bytes, settings.sample_rate, settings.symbol_rate, settings.symbol_length_bits)
original_signal_negative_positive = [-1 if x==0 else 1 for x in sampled_original_signal]

# show_plot(sampled_original_signal)
# show_plot(original_signal_negative_positive)





###

###
# DSSS Direct Sequence Spread Spectrum
###

dsss_signal = spread_signal(original_signal_negative_positive, 1, settings.sample_rate, settings.dsss_code_frequency)

# show_plot(dsss_signal, original_signal_negative_positive)






###

# signal_for_modulation = original_signal_negative_positive
signal_for_modulation = dsss_signal

###
# BPSK modulation of signal
###

modulated_signal = modulate_signal(signal_for_modulation, settings.modulation_carrier_frequency, settings.modulation_carrier_amplitude, settings.sample_rate)

# show_plot(modulated_signal)





###

signal_for_demodulation = modulated_signal

###
# BPSK signal demodulation
###

demodulated_signal = demodulate_signal(signal_for_demodulation, settings.modulation_carrier_frequency, settings.modulation_carrier_amplitude, settings.sample_rate)
filtered_demodulated_signal = low_pass_filter_butterworth(demodulated_signal, settings.sample_rate, settings.demodulation_filter_order, settings.demodulation_filter_cutoff_frequency)

# show_plot(demodulated_signal)
# show_plot(filtered_demodulated_signal)






###

###
# DSSS Despreading
###

dsss_despreaded_signal = despread_signal(filtered_demodulated_signal, 1, settings.sample_rate, settings.dsss_code_frequency)

# show_plot(dsss_despreaded_signal)





###

###
# Decode signal
###

binary_signal = bipolar_signal_to_binary(dsss_despreaded_signal)
decoded_bit_probabilities = decode_binary_signal_to_bit_probabilities(binary_signal, settings.sample_rate, settings.symbol_rate, settings.symbol_length_bits)
decoded_bits = get_bits_from_probabilities(decoded_bit_probabilities)
decoded_symbols = get_symbols_from_bits(decoded_bits, settings.symbol_length_bits)
# show_plot(binary_signal)
# show_plot(decoded_bit_probabilities)
# show_plot(decoded_bits)



print(f'Received:\t{decoded_symbols}')

if (''.join([chr(x) for x in decoded_symbols]) != original_signal_bytes.decode('ascii')):
    print('Result is corrupted.')
else:
    print('Success.')
    print('Result: ' + ''.join([chr(x) for x in decoded_symbols]))