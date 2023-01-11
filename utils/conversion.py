def bits_list_to_bytes(bits_list):
    bytes = [sum(b*2**x for b,x in zip(byte[::-1],range(8))) for byte in zip(*([iter(bits_list)]*8))]

    return bytes


def bytes_to_hex(bytes):
    return ''.join('{:02x}'.format(x) for x in bytes)


def bits_list_to_hex(bits_list):
    return bytes_to_hex(bits_list_to_bytes(bits_list))
