# TODO: proper double jump logic

grid_length = 3  # How many chars until you reach the actual board
row_length = 8
column_length = 8

turn = 0  # 0 is white 1 is black
command_list = []
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


default_board = BoardData(row_length, column_length, grid_length)
board_data = default_board

# Print
def print_header():
    for spaces in range(0, grid_length + 1):
        print("_", end="")

    # if there is two digits then print 2 "_" in between each letter
    # else print 1 digit
    for column in range(1, board_data.num_columns + 1):
        if column < 10:
            print(str(column) + "__", end="")
        else:
            print(str(column) + "_", end="")

    # print end line after you're done
    print("")


def print_footer():
    for spaces in range(0, grid_length + 1 + (board_data.num_columns * 3)):
        print("_", end="")
    print("\n", end="")


def print_board(board_dict):
    print("CHECKER BOARD by\nPorter Mecham")
    print_header()

    for key in board_dict:
        # print border
        print(key + " | ", end="")
        # print letter and a space
        for letter in board_dict[key]:
            print(letter + "  ", end="")
        # hit new line when done with a row
        print("\n", end="")
    # print the footer
    print_footer()


# Get Board
def place_beginning_checkers():
    new_checker_board = []
    ri = 0

    for row in get_board():
        ri += 1
        new_row = ""

        # if on top half of the board place white checkers
        if ri < board_data.num_rows / 2:
            for letter in row:
                if letter == "1":
                    new_row += "w"
                else:
                    new_row += letter
        # if on bottom half of the board place Black checkers
        elif ri > (board_data.num_rows / 2) + 1:
            for letter in row:
                if letter == "1":
                    new_row += "b"
                else:
                    new_row += letter
        # if in the middle of the board
        else:
            for letter in row:
                new_row += letter

        new_checker_board.append(new_row)

    ri = 1
    # put the default board to the current_board dict
    for row in new_checker_board:
        li = 0
        new_row = []
        # go through each letter
        for letter in row:
            # don't get the Grid on the outside of the board
            if li > grid_length:
                # make sure the board is getting only the right icons
                if letter in board_data.possible_board_icons:
                    new_row.append(letter)

            li += 1
        current_board[num_to_az[ri]] = new_row
        ri += 1

    return current_board


def get_board():
    checker_board = []
    ci = 1
    for row in range(1, board_data.num_rows + 1):
        if row % 2 == 0:
            checker_board.append(num_to_az[ci] + " | " + board_data.even_row + " |")
        else:
            checker_board.append(num_to_az[ci] + " | " + board_data.odd_row + " |")

        ci += 1

    return checker_board


# Move
def get_move():
    print("Example Move: A1,B2")
    _move = input("What is your move\n").upper()
    interpret_move(_move)


def check_icon(icon):
    if icon not in board_data.possible_board_icons:
        print(
            f"ERROR: Expected command to give coordinates to {board_data.possible_board_icons}, and instead got {icon}"
        )
        get_move()
        return False
    return True


def check_piece(icon):
    if icon not in board_data.checkers:
        print(
            f"ERROR: Expected command to give coordinates to {board_data.checkers}, and instead got {icon}"
        )
        get_move()
        return False

    return True


def interpret_move(_move):
    global turn

    # if the move isn't long enough length to be the right command send error
    if len(_move) != 5:
        print(f"ERROR: expected 5 characters not {len(_move)}")
        get_move()
        return
    # if there is a letter where there should be a number
    if _move[1].isalpha() or _move[4].isalpha():
        print(f"ERROR: letter where there should be a number")
        return

    first_move = _move[0:2]
    second_move = _move[3:5]

    # First Command
    if _move[0] in current_board:
        start_row = current_board[first_move[0]]
        start_col = int(first_move[1]) - 1
        start_icon = start_row[start_col]

        print(start_icon)
        # make sure the icon is valid
        if not check_piece(start_icon):
            print("ERROR: not a valid place to begin your move")
            get_move()
            return

        # Second Command
        if _move[3] in current_board:
            end_row = current_board[second_move[0]]
            end_col = int(second_move[1]) - 1
            end_icon = end_row[end_col]

            # ERROR CHECKING---------------------------------
            # if it's black's turn and you move a white piece
            if start_icon == "w" or start_icon == "W":
                if turn == 1:
                    print("ERROR: you tried to move a white piece on blacks turn")
                    get_move()
                    return

            # if it's white's turn and you move a black piece
            if start_icon == "b" or start_icon == "B":
                if turn == 0:
                    print("ERROR: you tried to move a Black piece on Whites turn")
                    get_move()
                    return

            # Don't allow backwards moves
            if start_icon == "w":
                if ord(str(_move[0])) - ord(str(_move[3])) > 0:
                    print("ERROR: Can't move backwards without a King")
                    get_move()

            # Don't allow backwards moves
            if start_icon == "b":
                if ord(str(_move[0])) - ord(str(_move[3])) < 0:
                    print("ERROR: Can't move backwards without a King")
                    get_move()

            # make sure the icon is valid
            if not check_icon(end_icon):
                print("ERROR: not a valid place to end your move")
                get_move()
                return
            # ERROR CHECKING---------------------------------

            # if the place they want to move is open then let them move
            if end_icon == "1":
                r_jump_size = abs(ord(str(_move[0])) - ord(str(_move[3])))
                c_jump_size = abs(start_col - end_col)

                # Don't allow jumps farther then one diagonal
                # get unicode number of string and make sure they're together
                if c_jump_size > 1 or r_jump_size > 1:
                    if c_jump_size > 2 or r_jump_size > 2:
                        print("ERROR: you can only move 1 column at a time")
                        get_move()
                        return
                    if c_jump_size == 2 and r_jump_size == 2:
                        middle_row = chr(int((abs(ord(_move[0]) + ord(_move[3]))) / 2))
                        middle_column = int(abs(start_col + end_col) / 2)
                        middle_icon = current_board[middle_row][middle_column]

                        # if there is no checker then don't allow the jump
                        if middle_icon == "1" or middle_icon == "0":
                            print("ERROR: You can only move 1 row at a time")
                            get_move()
                            return
                        else:
                            # Take piece
                            current_board[middle_row][middle_column] = "1"
                            # give player another turn to double jump
                            turn = (turn + 1) % 2

                # King them if they're on the last row of opposing side
                if second_move[0] == "A" and start_icon == "b":
                    current_board[second_move[0]][int(second_move[1]) - 1] = "B"
                    current_board[first_move[0]][int(first_move[1]) - 1] = "1"
                    turn = (turn + 1) % 2
                    return
                elif (
                    second_move[0] == chr(ord("A") + board_data.num_rows - 1)
                    and start_icon == "w"
                ):
                    current_board[second_move[0]][int(second_move[1]) - 1] = "W"
                    current_board[first_move[0]][int(first_move[1]) - 1] = "1"
                    turn = (turn + 1) % 2
                    return
                else:
                    # set the moved to square as having a piece
                    current_board[second_move[0]][int(second_move[1]) - 1] = start_icon
                    # set the first square to blank
                    current_board[first_move[0]][int(first_move[1]) - 1] = "1"
                    print(f"Moving {first_move} to {second_move}")

                    # should switch back and forth between 1 and 0
                    turn = (turn + 1) % 2

            else:
                print("ERROR: End square is occupied")
                get_move()
                return
    else:
        print(f"{_move[0]} is not in current_board")
        print(current_board)


def check_win():
    num_black = 0
    num_white = 0
    for key in current_board:
        for row in current_board[key]:
            if "w" in row or "W" in row:
                num_white += 1
            if "b" in row or "B" in row:
                num_black += 1

    if num_black == 0:
        print("WHITE HAS WON")
        print(f"White {num_white}, Black {num_black}")
        return True
    if num_white == 0:
        print("BLACK HAS WON")
        print(f"White {num_white}, Black {num_black}")
        return True


def initialize():
    place_beginning_checkers()
    # check for the things


# Main
if __name__ == "__main__":
    # initialize
    game_over = False
    current_board = place_beginning_checkers()
    while not game_over:
        print_board(current_board)
        get_move()
        game_over = check_win()
