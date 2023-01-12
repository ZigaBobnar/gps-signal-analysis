from math import cos, pi

def modulate_signal(signal, carrier_frequency, carrier_amplitude, sample_rate):
    output = []
    for i in range(len(signal)):
        # Modulate
        carrier_value = carrier_amplitude*cos(2*pi*i*carrier_frequency/sample_rate)
        sample_value = signal[i] * carrier_value

        output.append(sample_value)

    return output

def demodulate_signal(signal, carrier_frequency, carrier_amplitude, sample_rate):
    output = []
    for i in range(len(signal)):
        # De-modulate
        carrier_value = (1/carrier_amplitude) * cos(2*pi*i*carrier_frequency/sample_rate)
        sample_value = signal[i] * carrier_value

        output.append(sample_value)

    return output
