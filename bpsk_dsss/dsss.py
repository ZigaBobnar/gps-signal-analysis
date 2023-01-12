from bpsk_dsss.access_code import create_access_code


def spread_signal(signal, id, sample_frequency, dsss_code_frequency):
    code_length = 32

    code = create_access_code(id, code_length)
    code_dsss_sequence = [1 if x else -1 for x in code]

    code_samples_repeats = sample_frequency//dsss_code_frequency
    code_length = len(code_dsss_sequence)

    output = []

    for i in range(len(signal)):
        value = signal[i]

        code_index = ((0 if i==0 else i//code_samples_repeats) % code_length)
        # print(code_index)
        code_value = code_dsss_sequence[code_index]

        value = value*code_value

        output.append(value)


    return output


def despread_signal(signal, id, sample_frequency, dsss_code_frequency):
    code_length = 32

    code = create_access_code(id, code_length)
    code_dsss_sequence = [1 if x else -1 for x in code]

    code_samples_repeats = sample_frequency//dsss_code_frequency
    code_length = len(code_dsss_sequence)

    output = []

    for i in range(len(signal)):
        value = signal[i]

        code_index = ((0 if i==0 else i//code_samples_repeats) % code_length)
        # print(code_index)
        code_value = code_dsss_sequence[code_index]

        value = value*code_value

        output.append(value)


    return output
