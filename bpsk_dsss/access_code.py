from utils.prn_codes import G1Generator, G2Generator, get_feedbacks_for_id


# This is a fake implementation of GPS PRN codes!
# Used to demo it with shorter codes

def create_access_code(id, code_length):
    g1 = G1Generator()
    g2 = G2Generator()
    feedback = get_feedbacks_for_id(id)
    if feedback == None:
        raise Exception(f'Invalid prn id: {id}')

    offset1 = feedback[1][0] - 1
    offset2 = feedback[1][1] - 1

    value = []

    for _ in range(code_length):
        selection = g2.buff[offset1] ^ g2.buff[offset2]

        g1_val = g1.get_next()
        g2_val = g2.get_next()

        g2i = selection ^ g1_val

        value.append(g2i)

    return value
