grid_length = 3  # How many chars until you reach the actual board
row_length = 8
column_length = 8

whites_turn = True  # 0 is white 1 is black

move_history = []
has_jumped = False

num_to_az = {
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
current_board = {
    # "A": [],  # A is the row, then the elements+1 in the list will be the column
}


class BoardData:
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
