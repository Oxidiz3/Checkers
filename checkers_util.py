"""
holds all of the variables and functions that change data from one type to another
"""
GRID_LENGTH = 3  # How many chars until you reach the actual board
row_length = 4
column_length = 4

whites_turn = True  # 0 is white 1 is black
can_jump = False
game_over = False

move_history = []

w_possible_jumps = []  # a1,c3
b_possible_jumps = []  # a1,c3

possible_board_pieces = ["w", "W", "b", "B"]
NUM_TO_AZ = {
    1: "A",
    2: "B",
    3: "C",
    4: "D",
    5: "E",
    6: "F",
    7: "G",
    8: "H",
    9: "I",
    10: "J",
    11: "K",
    12: "L",
    13: "M",
    14: "N",
    15: "O",
    16: "P",
    17: "Q",
    18: "R",
    19: "S",
    20: "T",
    21: "U",
    22: "V",
    23: "W",
    24: "X",
    25: "Y",
    26: "Z",
}
AZ_TO_NUM = {c: r for r, c in NUM_TO_AZ.items()}

current_board = {
    # "A": [],  # A is the row, then the elements+1 in the list will be the column
}


class BoardData:
    """ Holds all of the data to define a board """

    def __init__(self, rows, columns, outside_size):
        self.num_rows = rows
        self.num_columns = columns
        self.outside_size = outside_size
        self.even_row = ""
        self.odd_row = ""
        self.possible_board_icons = ["1", "0", "B", "W", "b", "w"]
        self.checkers = ["B", "W", "b", "w"]
        # default odd row "0, 1, 0, 1, 0, 1, 0, 1"

        # for even rows
        for num in range(1, columns + 1):
            if num % 2:
                self.even_row += "0"
            else:
                self.even_row += "1"

            if num < columns:
                self.even_row += ", "

        # for odd rows
        for num in range(1, columns + 1):
            if num % 2:
                self.odd_row += "1"
            else:
                self.odd_row += "0"
            if num < columns:
                self.odd_row += ", "


def get_middle_coords(start, end):
    """ takes beginning and end coordinates and returns the middle of the two """
    middle_row = chr(int((abs(ord(start[0]) + ord(end[0]))) / 2))
    middle_column = int(abs(int(start[1]) + int(end[1])) / 2)

    middle = middle_row + str(middle_column)

    return middle


def coord_to_icon(coord: str):
    """ gets coordinates and returns the corelating icon """
    row = current_board[coord[0]]
    column = int(coord[1]) - 1
    return row[column]
