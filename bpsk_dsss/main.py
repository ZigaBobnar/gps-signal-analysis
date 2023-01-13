from math import floor
from matplotlib import pyplot
import numpy
from scipy.fft import fft, fftfreq
from bpsk_dsss.dsss import despread_signal, spread_signal
from bpsk_dsss.filtering import low_pass_filter_butterworth
from bpsk_dsss.bpsk import demodulate_signal, modulate_signal
from bpsk_dsss.plot import save_plot, show_plot
from bpsk_dsss import settings
from bpsk_dsss.digital_signal import bipolar_signal_to_binary, decode_binary_signal_to_bit_probabilities, get_bits_from_probabilities, get_symbols_from_bits, sample_digital_signal, upsample_signal


def get_subsample_slice(signal, slice_length_factor=1):
    if slice_length_factor == 1:
        return signal[settings.plot_subsample_start:settings.plot_subsample_end:settings.plot_subsample_downsample_factor]

    return signal[settings.plot_subsample_start:floor(settings.plot_subsample_start+(settings.plot_subsample_length*slice_length_factor)):settings.plot_subsample_downsample_factor]


###
# Original data signal sampling
###

original_signal_bytes = settings.original_signal_data.encode('ascii')
print(f'Poslano:\t{[x for x in original_signal_bytes]}')
sampled_original_signal = sample_digital_signal(original_signal_bytes, settings.sample_rate, settings.symbol_rate, settings.symbol_length_bits)
original_signal_negative_positive = [-1 if x==0 else 1 for x in sampled_original_signal]

x_axis_samples = numpy.arange(len(sampled_original_signal))
x_axis_seconds = x_axis_samples/settings.sample_rate
x_axis_subsamples = get_subsample_slice(x_axis_samples)

# show_plot(sampled_original_signal)
# show_plot(original_signal_negative_positive)

fig = pyplot.figure(figsize=[10,4])
ax = pyplot.subplot(111)
l = ax.plot(x_axis_samples, sampled_original_signal, c='0.2', linewidth=1.0)

ax.set_xlabel('Vzorec n')
ax.set_ylabel('Vrednost vzorca')
# ax.set_title('')
# ax.set_xlim(0, 24)
ax.set_ylim(-0.1, 1.1)
ax.set_yticks(numpy.arange(0, 2, 1))
# ax.grid('on')

save_plot('original_sampled_bits')
# pyplot.show()



fig = pyplot.figure(figsize=[10,4])
ax = pyplot.subplot(111)
l = ax.plot(x_axis_subsamples, get_subsample_slice(original_signal_negative_positive), c='0.2', linewidth=1.0)

ax.set_xlabel('Vzorec n')
ax.set_ylabel('Vrednost vzorca')
# ax.set_title('')
# ax.set_xlim(0, 24)
ax.set_ylim(-1.1, 1.1)
ax.set_yticks(numpy.arange(-1, 2, 1))
# ax.grid('on')

save_plot('original_sampled_bits_shifted_to_neg_pos_one')
# pyplot.show()

###

###
# DSSS Direct Sequence Spread Spectrum
###

dsss_signal = spread_signal(original_signal_negative_positive, 1, settings.sample_rate, settings.dsss_code_frequency)


fig = pyplot.figure(figsize=[10,4])
ax = pyplot.subplot(111)
l = ax.plot(x_axis_subsamples, get_subsample_slice(dsss_signal), c='0.2', linewidth=1.0)

ax.set_xlabel('Vzorec n')
ax.set_ylabel('Vrednost vzorca')
# ax.set_title('')
# ax.set_xlim(0, 24)
ax.set_ylim(-1.1, 1.1)
ax.set_yticks(numpy.arange(-1, 2, 1))
# ax.grid('on')

save_plot('dsss_signal_spreading')
# pyplot.show()





fig = pyplot.figure(figsize=[10,4])
ax = pyplot.subplot(111)
l = ax.plot(x_axis_subsamples, get_subsample_slice(numpy.roll([x+0.02 for x in original_signal_negative_positive], -100)), c='0.5', linewidth=0.7, linestyle='dashdot')
l = ax.plot(x_axis_subsamples, get_subsample_slice(dsss_signal), c='0.2', linewidth=1.0)

ax.set_xlabel('Vzorec n')
ax.set_ylabel('Vrednost vzorca')
# ax.set_title('')
# ax.set_xlim(0, 24)
ax.set_ylim(-1.1, 1.1)
ax.set_yticks(numpy.arange(-1, 2, 1))
# ax.grid('on')

save_plot('dsss_spread_signal_and_original_signal_combo')
# pyplot.show()







###

# signal_for_modulation = original_signal_negative_positive
signal_for_modulation = dsss_signal

###
# BPSK modulation of signal
###

modulated_signal = modulate_signal(signal_for_modulation, settings.modulation_carrier_frequency, settings.modulation_carrier_amplitude, settings.sample_rate)

fig = pyplot.figure(figsize=[10,4])
ax = pyplot.subplot(111)
l = ax.plot(get_subsample_slice(x_axis_samples, 0.2), get_subsample_slice(signal_for_modulation, 0.2), c='0.5', linewidth=0.4, linestyle='dashdot')
l = ax.plot(get_subsample_slice(x_axis_samples, 0.2), get_subsample_slice(modulated_signal, 0.2), c='0.2', linewidth=1.0)

ax.set_xlabel('Vzorec n')
ax.set_ylabel('Vrednost')
# ax.set_title('')
# ax.set_xlim(0, 24)
# ax.set_ylim(-1.1, 1.1)
# ax.set_yticks(numpy.arange(-1, 2, 1))
# ax.grid('on')

save_plot('bpsk_modulated_dsss_signal')
# pyplot.show()









###
# Transmission channel, adding random noise
###

noise_signal = numpy.random.normal(scale=settings.noise_amplitude, size=len(modulated_signal))
noisy_signal = modulated_signal + noise_signal

fig = pyplot.figure(figsize=[10,4])
ax = pyplot.subplot(111)
l = ax.plot(get_subsample_slice(x_axis_samples, 0.2), get_subsample_slice(noisy_signal, 0.2), c='0.3', linewidth=0.8)
l = ax.plot(get_subsample_slice(x_axis_samples, 0.2), get_subsample_slice(modulated_signal, 0.2), c='0.9', linewidth=0.5)

ax.set_xlabel('Vzorec n')
ax.set_ylabel('Vrednost')
# ax.set_title('')
# ax.set_xlim(0, 24)
# ax.set_ylim(-1.1, 1.1)
# ax.set_yticks(numpy.arange(-1, 2, 1))
# ax.grid('on')

save_plot('transmitted_signal_with_noise')
# pyplot.show()












###

# signal_for_demodulation = modulated_signal
signal_for_demodulation = noisy_signal

###
# BPSK signal demodulation
###

demodulated_signal = demodulate_signal(signal_for_demodulation, settings.modulation_carrier_frequency, settings.modulation_carrier_amplitude, settings.sample_rate)
filtered_demodulated_signal = low_pass_filter_butterworth(demodulated_signal, settings.sample_rate, settings.demodulation_filter_order, settings.demodulation_filter_cutoff_frequency)

# show_plot(demodulated_signal)
# show_plot(filtered_demodulated_signal)

fig = pyplot.figure(figsize=[10,4])
ax = pyplot.subplot(111)
l = ax.plot(get_subsample_slice(x_axis_samples, 0.2), get_subsample_slice(demodulated_signal, 0.2), c='0.3', linewidth=0.8)
l = ax.plot(get_subsample_slice(x_axis_samples, 0.2), get_subsample_slice(modulated_signal, 0.2), c='0.9', linewidth=0.8, linestyle='dotted')

ax.set_xlabel('Vzorec n')
ax.set_ylabel('Vrednost')
# ax.set_title('')
# ax.set_xlim(0, 24)
# ax.set_ylim(-1.1, 1.1)
# ax.set_yticks(numpy.arange(-1, 2, 1))
# ax.grid('on')

save_plot('bpsk_demodulated_dsss_signal')
# pyplot.show()







fig = pyplot.figure(figsize=[10,4])
ax = pyplot.subplot(111)
# l = ax.plot(x_axis_subsamples, get_subsample_slice(filtered_demodulated_signal), c='0.6', linewidth=1.0)

l = ax.plot(x_axis_subsamples, get_subsample_slice(demodulated_signal), c='0.3', linewidth=0.8)
l = ax.plot(x_axis_subsamples, get_subsample_slice(modulated_signal), c='0.5', linewidth=0.1, linestyle='dotted')
l = ax.plot(x_axis_subsamples, get_subsample_slice(filtered_demodulated_signal), c='0.9', linewidth=1.0)

ax.set_xlabel('Vzorec n')
ax.set_ylabel('Vrednost')
# ax.set_title('')
# ax.set_xlim(0, 24)
# ax.set_ylim(-1.1, 1.1)
# ax.set_yticks(numpy.arange(-1, 2, 1))
# ax.grid('on')

save_plot('bpsk_demodulated_dsss_signal_low_pass_filtered')
# pyplot.show()






###

###
# DSSS Despreading
###

dsss_despreaded_signal = despread_signal(filtered_demodulated_signal, 1, settings.sample_rate, settings.dsss_code_frequency)


fig = pyplot.figure(figsize=[10,4])
ax = pyplot.subplot(111)
l = ax.plot(x_axis_subsamples, get_subsample_slice(dsss_despreaded_signal), c='0.6', linewidth=1.0)

ax.set_xlabel('Vzorec n')
ax.set_ylabel('Vrednost')
# ax.set_title('')
# ax.set_xlim(0, 24)
# ax.set_ylim(-1.1, 1.1)
# ax.set_yticks(numpy.arange(-1, 2, 1))
# ax.grid('on')

save_plot('despreaded_dsss_signal')
# pyplot.show()








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



fig = pyplot.figure(figsize=[10,4])
ax = pyplot.subplot(111)
l = ax.plot(x_axis_subsamples, get_subsample_slice(binary_signal), c='0.6', linewidth=1.0)

ax.set_xlabel('Vzorec n')
ax.set_ylabel('Vrednost')
# ax.set_title('')
# ax.set_xlim(0, 24)
# ax.set_ylim(-1.1, 1.1)
# ax.set_yticks(numpy.arange(-1, 2, 1))
# ax.grid('on')

save_plot('decoded_binary_signal_from_despreaded')
# pyplot.show()



fig = pyplot.figure(figsize=[10,4])
ax = pyplot.subplot(111)
l = ax.plot(x_axis_subsamples, get_subsample_slice([(x*2)-1 for x in binary_signal]), c='0.6', linewidth=1.0)
l = ax.plot(x_axis_subsamples, get_subsample_slice(dsss_despreaded_signal), c='0.2', linewidth=1.0)

ax.set_xlabel('Vzorec n')
ax.set_ylabel('Vrednost')
# ax.set_title('')
# ax.set_xlim(0, 24)
# ax.set_ylim(-1.1, 1.1)
# ax.set_yticks(numpy.arange(-1, 2, 1))
# ax.grid('on')

save_plot('decoded_binary_signal_from_despreaded_and_despreaded_combo')
# pyplot.show()





fig = pyplot.figure(figsize=[10,4])
ax = pyplot.subplot(111)
l = ax.plot(numpy.arange(len(decoded_bits)*10), upsample_signal(decoded_bits, 10), c='0.2', linewidth=1.0)

ax.set_xlabel('Vzorec n')
ax.set_ylabel('Vrednost')
# ax.set_title('')
# ax.set_xlim(0, 24)
# ax.set_ylim(-1.1, 1.1)
# ax.set_yticks(numpy.arange(-1, 2, 1))
# ax.grid('on')

save_plot('decoded_bit_sequence')
# pyplot.show()




fig = pyplot.figure(figsize=[10,4])
ax = pyplot.subplot(111)
l = ax.plot(x_axis_samples, numpy.roll(sampled_original_signal, -1000)+0.005, c='0.4', linewidth=1.0)
l = ax.plot(x_axis_samples, sample_digital_signal(original_signal_bytes, settings.sample_rate, settings.symbol_rate, settings.symbol_length_bits), c='0.2', linewidth=1.0)


ax.set_xlabel('Vzorec n')
ax.set_ylabel('Vrednost')
# ax.set_title('')
# ax.set_xlim(0, 24)
# ax.set_ylim(-1.1, 1.1)
# ax.set_yticks(numpy.arange(-1, 2, 1))
# ax.grid('on')

save_plot('decoded_bit_sequence_and_original_signal_bits_combo')
# pyplot.show()





# Spectrums
original_signal_spectrum = fft(signal_for_modulation)
original_signal_bpsk_without_dsss_specturm = fft(modulate_signal(signal_for_modulation, settings.modulation_carrier_frequency, settings.modulation_carrier_amplitude, settings.sample_rate))
bpsk_dsss_clean_signal_spectrum = fft(dsss_signal)
noisy_signal_spectrum = fft(noisy_signal)
fft_frequencies = fftfreq(len(signal_for_modulation), 1/settings.sample_rate)





fig = pyplot.figure(figsize=[10,4])
ax = pyplot.subplot(111)
# l = ax.plot(fft_frequencies, original_signal_bpsk_without_dsss_specturm, c='0.6', linewidth=1.0)
# l = ax.plot(fft_frequencies[idx], bpsk_dsss_clean_signal_spectrum[idx], c='0.6', linewidth=1.0)
# l = ax.plot(fft_frequencies, noisy_signal_spectrum, c='0.6', linewidth=1.0)

ax.set_yscale('log')
ax.set_xscale('log')
l = ax.plot(fft_frequencies, numpy.abs(original_signal_spectrum), c='0.2', linewidth=1.0)
# l = ax.stem(fft_frequencies, numpy.abs(bpsk_dsss_clean_signal_spectrum), 'b', markerfmt=" ", basefmt='-b')
# l = ax.stem(fft_frequencies, numpy.abs(bpsk_dsss_clean_signal_spectrum), 'b', markerfmt=" ", basefmt='-b')

ax.set_xlabel('Frekvenca [Hz]')
ax.set_ylabel('FFT amplituda |X(f)|')
# ax.set_title('')
# ax.set_xlim(0, 24)
# ax.set_ylim(-1.1, 1.1)
# ax.set_yticks(numpy.arange(-1, 2, 1))
# ax.grid('on')

save_plot('spectrum_source')
# pyplot.show()





fig = pyplot.figure(figsize=[10,4])
ax = pyplot.subplot(111)
# l = ax.plot(fft_frequencies, original_signal_bpsk_without_dsss_specturm, c='0.6', linewidth=1.0)
# l = ax.plot(fft_frequencies[idx], bpsk_dsss_clean_signal_spectrum[idx], c='0.6', linewidth=1.0)
# l = ax.plot(fft_frequencies, noisy_signal_spectrum, c='0.6', linewidth=1.0)

ax.set_yscale('log')
ax.set_xscale('log')
l = ax.plot(fft_frequencies, numpy.abs(original_signal_bpsk_without_dsss_specturm), c='0.2', linewidth=1.0)
# l = ax.stem(fft_frequencies, numpy.abs(bpsk_dsss_clean_signal_spectrum), 'b', markerfmt=" ", basefmt='-b')
# l = ax.stem(fft_frequencies, numpy.abs(bpsk_dsss_clean_signal_spectrum), 'b', markerfmt=" ", basefmt='-b')

ax.set_xlabel('Frekvenca [Hz]')
ax.set_ylabel('FFT amplituda |X(f)|')
# ax.set_title('')
# ax.set_xlim(0, 24)
# ax.set_ylim(-1.1, 1.1)
# ax.set_yticks(numpy.arange(-1, 2, 1))
# ax.grid('on')

save_plot('spectrum_bpsk')
# pyplot.show()








fig = pyplot.figure(figsize=[10,4])
ax = pyplot.subplot(111)
# l = ax.plot(fft_frequencies, original_signal_bpsk_without_dsss_specturm, c='0.6', linewidth=1.0)
# l = ax.plot(fft_frequencies[idx], bpsk_dsss_clean_signal_spectrum[idx], c='0.6', linewidth=1.0)
# l = ax.plot(fft_frequencies, noisy_signal_spectrum, c='0.6', linewidth=1.0)

ax.set_yscale('log')
ax.set_xscale('log')
# l = ax.plot(fft_frequencies, numpy.abs(original_signal_bpsk_without_dsss_specturm))
l = ax.plot(fft_frequencies, numpy.abs(bpsk_dsss_clean_signal_spectrum), c='0.2', linewidth=1.0)
# l = ax.stem(fft_frequencies, numpy.abs(bpsk_dsss_clean_signal_spectrum), 'b', markerfmt=" ", basefmt='-b')
# l = ax.stem(fft_frequencies, numpy.abs(bpsk_dsss_clean_signal_spectrum), 'b', markerfmt=" ", basefmt='-b')

ax.set_xlabel('Frekvenca [Hz]')
ax.set_ylabel('FFT amplituda |X(f)|')
# ax.set_title('')
# ax.set_xlim(0, 24)
# ax.set_ylim(-1.1, 1.1)
# ax.set_yticks(numpy.arange(-1, 2, 1))
# ax.grid('on')

save_plot('spectrum_dsss_bpsk')
# pyplot.show()




fig = pyplot.figure(figsize=[10,4])
ax = pyplot.subplot(111)
# l = ax.plot(fft_frequencies, original_signal_bpsk_without_dsss_specturm, c='0.6', linewidth=1.0)
# l = ax.plot(fft_frequencies[idx], bpsk_dsss_clean_signal_spectrum[idx], c='0.6', linewidth=1.0)
# l = ax.plot(fft_frequencies, noisy_signal_spectrum, c='0.6', linewidth=1.0)

ax.set_yscale('log')
ax.set_xscale('log')
# l = ax.plot(fft_frequencies, numpy.abs(original_signal_bpsk_without_dsss_specturm))
l = ax.plot(fft_frequencies, numpy.abs(noisy_signal_spectrum), c='0.2', linewidth=1.0)
# l = ax.stem(fft_frequencies, numpy.abs(bpsk_dsss_clean_signal_spectrum), 'b', markerfmt=" ", basefmt='-b')
# l = ax.stem(fft_frequencies, numpy.abs(bpsk_dsss_clean_signal_spectrum), 'b', markerfmt=" ", basefmt='-b')

ax.set_xlabel('Frekvenca [Hz]')
ax.set_ylabel('FFT amplituda |X(f)|')
# ax.set_title('')
# ax.set_xlim(0, 24)
# ax.set_ylim(-1.1, 1.1)
# ax.set_yticks(numpy.arange(-1, 2, 1))
# ax.grid('on')

save_plot('spectrum_dsss_bpsk_noisy')
# pyplot.show()


















print(f'Sprejeto:\t{decoded_symbols}')

if (''.join([chr(x) for x in decoded_symbols]) != original_signal_bytes.decode('ascii')):
    print('Result is corrupted.')
else:
    # print('Success.')
    print('Rezultat: ' + ''.join([chr(x) for x in decoded_symbols]))