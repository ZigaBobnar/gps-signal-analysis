from utils.prn_codes import create_G1_code, create_G2_code, create_G2i_code
from utils.conversion import bits_list_to_hex

g1 = create_G1_code()
print(f'G1 code is:\n{bits_list_to_hex(g1)}\n{"".join([("1" if x else "0") for x in g1])}')

g2 = create_G2_code()
print(f'G2 code is:\n{bits_list_to_hex(g2)}\n{"".join([("1" if x else "0") for x in g2])}')

g2_24 = create_G2i_code(24)
print(f'G2_24 code is:\n{bits_list_to_hex(g2_24)}\n{"".join([("1" if x else "0") for x in g2_24])}')
