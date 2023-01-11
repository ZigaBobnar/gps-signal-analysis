from utils.conversion import bits_list_to_hex
from utils.prn_codes import G1Generator, G2Generator, create_G1_code, create_G2_code


def shift(register, feedback, output):
    """GPS Shift Register
    
    :param list feedback: which positions to use as feedback (1 indexed)
    :param list output: which positions are output (1 indexed)
    :returns output of shift register:
    
    """
    
    # calculate output
    out = [register[i-1] for i in output]
    if len(out) > 1:
        out = sum(out) % 2
    else:
        out = out[0]
        
    # modulo 2 add feedback
    fb = sum([register[i-1] for i in feedback]) % 2
    
    # shift to the right
    for i in reversed(range(len(register[1:]))):
        register[i+1] = register[i]
        
    # put feedback in position 1
    register[0] = fb
    
    return out


#
# G1
#

g1_bits_original = []
G1 = [1 for i in range(10)]
for i in range(1023):
    g1_bits_original.append(shift(G1, [3, 10], [10]))



G1gen = G1Generator()
g1_bits = []
for i in range(1023):
    g1_bits.append(1 if G1gen.get_next() else 0)



if g1_bits == g1_bits_original:
    if create_G1_code() == g1_bits_original:
        print('**** G1 test success ****')
    else:
        print('---- G1 test failed! (create_G1_code() function is broken) ----')
else:
    print('---- G1 test failed! ----')

    print(f'G1 (original):\n{bits_list_to_hex(g1_bits_original)}')
    print(f'G1 (test):\n{bits_list_to_hex(g1_bits)}')

#
# G2
#

g2_bits_original = []
G2 = [1 for i in range(10)]
for i in range(1023):
    g2_bits_original.append(shift(G2, [2,3,6,8,9,10], [10]))


G2gen = G2Generator()
g2_bits = []
for i in range(1023):
    g2_bits.append(1 if G2gen.get_next() else 0)


if g2_bits == g2_bits_original:
    if create_G2_code() == g2_bits_original:
        print('**** G2 test success ****')
    else:
        print('---- G2 test failed! (create_G2_code() function is broken) ----')
else:
    print('---- G2 test failed! ----')

    print(f'G2 (original):\n{bits_list_to_hex(g2_bits_original)}')
    print(f'G2 (test):\n{bits_list_to_hex(g2_bits)}')



#
# C/A short test (sat 24 - feedback: 2,6)
#

bits_ca_short_original = []
G1 = [1 for i in range(10)]
G2 = [1 for i in range(10)]
for i in range(20):
    bits_ca_short_original.append(
      (
        shift(G1, [3, 10], [10]) +
        shift(G2, [2,3,6,8,9,10], [2, 6])
      ) % 2)


G1gen = G1Generator()
G2gen = G2Generator()
bits_ca_short = []
for i in range(20):
    phase = G2gen.buff[2-1] ^ G2gen.buff[6-1]
    G2gen.get_next()

    bits_ca_short.append(
      1 if (
        phase ^
        G1gen.get_next()
      ) else 0)



if bits_ca_short == bits_ca_short_original:
    print('**** CA short test success ****')
else:
    print('---- CA short test failed! ----')

    print(f'CA short (original):\n{bits_list_to_hex(bits_ca_short_original)}\n{bits_ca_short_original}')
    print(f'CA short (test):\n{bits_list_to_hex(bits_ca_short)}\n{bits_ca_short}')


#
# C/A (sat 24 - feedback: 2,6)
#

bits_ca_original = []
G1 = [1 for i in range(10)]
G2 = [1 for i in range(10)]
for i in range(1023):
    bits_ca_original.append(
      (
        shift(G1, [3, 10], [10]) +
        shift(G2, [2,3,6,8,9,10], [2, 6])
      ) % 2)


G1gen = G1Generator()
G2gen = G2Generator()
bits_ca = []
for i in range(1023):
    phase = G2gen.buff[2-1] ^ G2gen.buff[6-1]
    G2gen.get_next()

    bits_ca.append(
      1 if (
        phase ^
        G1gen.get_next()
      ) else 0)



if bits_ca == bits_ca_original:
    print('**** CA test success ****')
else:
    print('---- CA test failed! ----')

    print(f'CA (original):\n{bits_list_to_hex(bits_ca_original)}\n{bits_ca_original}')
    print(f'CA (test):\n{bits_list_to_hex(bits_ca)}\n{bits_ca}')

