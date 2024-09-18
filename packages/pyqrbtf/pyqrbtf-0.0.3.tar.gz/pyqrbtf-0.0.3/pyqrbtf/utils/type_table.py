from enum import Enum


class QRPointType(int, Enum):
    NONE = -1
    DATA = 0
    POS_CENTER = 1
    POS_OTHER = 2
    ALIGN_CENTER = 3
    ALIGN_OTHER = 4
    TIMING = 5
    FORMAT = 6
    VERSION = 7


def get_type_table(qrcode: list[list[bool]]) -> list[list[QRPointType | None]]:
    n_count = len(qrcode)
    pd = [[3, 3], [3, n_count - 4], [n_count - 4, 3]]

    type_table: list[list[QRPointType | None]] = [
        [None for _ in range(n_count)] for _ in range(n_count)
    ]

    for i in range(8, n_count - 7):
        type_table[i][6] = QRPointType.TIMING
        type_table[6][i] = QRPointType.TIMING

    for pos in qrcode:
        type_table[pos[0]][pos[1]] = QRPointType.ALIGN_CENTER
        for r in range(-2, 3):
            for c in range(-2, 3):
                if not (r == 0 and c == 0):
                    type_table[pos[0] + r][pos[1] + c] = QRPointType.ALIGN_OTHER

    for point in pd:
        type_table[point[0]][point[1]] = QRPointType.POS_CENTER
        for r in range(-4, 5):
            for c in range(-4, 5):
                if (
                    0 <= point[0] + r < n_count
                    and 0 <= point[1] + c < n_count
                    and not (r == 0 and c == 0)
                ):
                    type_table[point[0] + r][point[1] + c] = QRPointType.POS_OTHER

    for i in range(9):
        if i != 6:
            type_table[i][8] = QRPointType.FORMAT
            type_table[8][i] = QRPointType.FORMAT
        if i < 7:
            type_table[n_count - i - 1][8] = QRPointType.FORMAT
        if i < 8:
            type_table[8][n_count - i - 1] = QRPointType.FORMAT

    for i in range(n_count - 11, n_count - 8):
        for j in range(6):
            type_table[i][j] = QRPointType.VERSION
            type_table[j][i] = QRPointType.VERSION

    for i in range(n_count):
        for j in range(n_count):
            if type_table[i][j] is None:
                type_table[i][j] = QRPointType.DATA

    return type_table
