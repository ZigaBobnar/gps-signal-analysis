
# Sattelite ID | PRN feedback (Specification of SPS Ranging Signal Characteristics - June 1995)
#    1   |     2, 6
#    2   |     3, 7
#    3   |     4, 8
#    4   |     5, 9
#    5   |     1, 9
#    6   |     2, 10
#    7   |     1, 8
#    8   |     2, 9
#    9   |     3, 10
#   10   |     2, 3
#   11   |     3, 4
#   12   |     5, 6
#   13   |     6, 7
#   14   |     7, 8
#   15   |     8, 9
#   16   |     9, 10
#   17   |     1, 4
#   18   |     2, 5
#   19   |     3, 6
#   20   |     4, 7
#   21   |     5, 8
#   22   |     6, 9
#   23   |     1, 3
#   24   |     4, 6
#   25   |     5, 7
#   26   |     6, 8
#   27   |     7, 9
#   28   |     8, 10
#   29   |     1, 6
#   30   |     2, 7
#   31   |     3, 8
#   32   |     4, 9
#   ***  |     5, 10
#   ***  |     4, 10
#   ***  |     1, 7
#   ***  |     2, 8
#   ***  |     4, 10
prn_feedbacks = [(1, [2, 6]), (2, [3, 7]), (3, [4, 8]), (4, [5, 9]), (5, [1, 9]), (6, [2, 10]), (7, [1, 8]), (8, [2, 9]), (9, [3, 10]), (10, [2, 3]), (11, [3, 4]), (12, [5, 6]), (13, [6, 7]), (14, [7, 8]), (15, [8, 9]), (16, [9, 10]), (17, [1, 4]), (18, [2, 5]), (19, [3, 6]), (20, [4, 7]), (21, [5, 8]), (22, [6, 9]), (23, [1, 3]), (24, [4, 6]), (25, [5, 7]), (26, [6, 8]), (27, [7, 9]), (28, [8, 10]), (29, [1, 6]), (30, [2, 7]), (31, [3, 8]), (32, [4, 9]), (33, [5, 10]), (34, [4, 10]), (35, [1, 7]), (36, [2, 8]), (37, [4, 10])]
def get_feedbacks_for_id(id):
    for prn in prn_feedbacks:
        if prn[0] == id:
            return prn
    return None

class GoldGenerator:
    def __init__(self) -> None:
        self.buff = [True for _ in range(10)] # Initialization vector 1111111111

    def get_next(self):
        input = self.get_feedback()
        output = self.buff[len(self.buff)-1]

        # Shift all bits right
        for i in reversed(range(len(self.buff) - 1)):
            self.buff[i+1] = self.buff[i]

        self.buff[0] = input

        return output

    def get_feedback(self):
        return False

  
class G1Generator(GoldGenerator):
    def get_feedback(self):
        # G1 code uses polynome 1+x^3+x^10
        # Feedback indexes: 3 and 10
        return (self.buff[3-1] ^ self.buff[10-1]) # XOR

class G2Generator(GoldGenerator):
    def get_feedback(self):
        # G2 code uses polynome 1+x^2+x^3+x^6+x^8+x^9+x^10
        # Feedback indexes: 2, 3, 6, 8, 9 and 10
        return (self.buff[2-1] ^ self.buff[3-1] ^ self.buff[6-1] ^ self.buff[8-1] ^ self.buff[9-1] ^ self.buff[10-1])


def create_G1_code():
    g1 = G1Generator()

    value = []
    for _ in range(1023):
        value.append(g1.get_next())

    return value

def create_G2_code():
    g2 = G2Generator()

    value = []
    for _ in range(1023):
        value.append(g2.get_next())

    return value

def create_G2i_code(id):
    g1 = G1Generator()
    g2 = G2Generator()
    feedback = get_feedbacks_for_id(id)
    if feedback == None:
        raise Exception(f'Invalid prn id: {id}')

    offset1 = feedback[1][0] - 1
    offset2 = feedback[1][1] - 1

    value = []

    for _ in range(1023):
        selection = g2.buff[offset1] ^ g2.buff[offset2]

        g1_val = g1.get_next()
        g2_val = g2.get_next()

        g2i = selection ^ g1_val

        value.append(g2i)

    return value
