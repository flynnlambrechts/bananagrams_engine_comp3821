VERTICAL = 1
HORIZONTAL = 0
MAX_LIMIT = 50
NO_SPACE_FOR_WORD = (-1, -1)
ANCHOR_IS_PREFIX = 0
ANCHOR_IS_SUFFIX = 1

letter_count = {'A': 196745, 'B': 47310, 'C': 102008, 'D': 85376, 'E': 287058, 'F': 30331,
                'G': 71315, 'H': 63613, 'I': 229895, 'J': 4240, 'K': 23873, 'L': 133085,
                'M': 73708, 'N': 170300, 'O': 168711, 'P': 76371, 'Q': 4301, 'R': 177701,
                'S': 245015, 'T': 165990, 'U': 84212, 'V': 23418, 'W': 19567, 'X': 7216,
                'Y': 41123, 'Z': 12279}

letter_distribution = {"A": 13, "B": 3, "C": 3, "D": 6, "E": 18, "F": 3, "G": 4,
                       "H": 3, "I": 12, "J": 2, "K": 2, "L": 5, "M": 3, "N": 8,
                       "O": 11, "P": 3, "Q": 2, "R": 9, "S": 6, "T": 9, "U": 6,
                       "V": 3, "W": 3, "X": 2, "Y": 3, "Z": 2}

is_prefix_of = {'A': 16194, 'B': 15218, 'C': 25015, 'D': 16619, 'E': 11330, 'F': 10633, 'G': 9351, 'H': 10524, 'I': 9604, 'J': 2311, 'K': 3361, 'L': 8058,
                'M': 15811, 'N': 6564, 'O': 8895, 'P': 24327, 'Q': 1411, 'R': 15014, 'S': 31986, 'T': 14563, 'U': 9522, 'V': 4590, 'W': 5921, 'X': 309, 'Y': 1036, 'Z': 1159}
is_suffix_of = {'A': 5560, 'B': 371, 'C': 6121, 'D': 25039, 'E': 28261, 'F': 534, 'G': 20216, 'H': 3293, 'I': 1601, 'J': 12, 'K': 2327, 'L': 8586,
                'M': 4620, 'N': 12003, 'O': 1887, 'P': 1547, 'Q': 10, 'R': 14784, 'S': 107294, 'T': 13933, 'U': 379, 'V': 45, 'W': 610, 'X': 583, 'Y': 19551, 'Z': 159}
pair_start_count = {'A': 16, 'B': 5, 'C': 1, 'D': 4, 'E': 13, 'F': 3, 'G': 3, 'H': 5, 'I': 6, 'J': 2, 'K': 4, 'L': 3,
                    'M': 7, 'N': 5, 'O': 17, 'P': 4, 'Q': 1, 'R': 1, 'S': 4, 'T': 4, 'U': 8, 'V': 0, 'W': 2, 'X': 2, 'Y': 4, 'Z': 3}
pair_end_count = {'A': 15, 'B': 2, 'C': 0, 'D': 4, 'E': 15, 'F': 3, 'G': 2, 'H': 6, 'I': 14, 'J': 0, 'K': 1, 'L': 2,
                  'M': 6, 'N': 5, 'O': 17, 'P': 2, 'Q': 0, 'R': 4, 'S': 5, 'T': 5, 'U': 6, 'V': 0, 'W': 3, 'X': 3, 'Y': 7, 'Z': 0}
