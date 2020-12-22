# TODO: proper double jump logic
# TODO: Try Jumping
import checkers_util as cu
from checkers_util import BoardData


board_data = BoardData(cu.row_length, cu.column_length, cu.grid_length)

# Print
def print_header():
    print("_" * (cu.grid_length + 1), end="")

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
    print("_" * (cu.grid_length + 1 + (board_data.num_columns * 3)))

    if len(cu.move_history) != 0:
        print("Last Move:", cu.move_history[-1])
    if cu.whites_turn:
        print("White's Turn")
    else:
        print("Black's Turn")


def print_board():
    board_dict = cu.current_board

    print("CHECKER BOARD by\nPorter Mecham")
    print_header()

    for key in board_dict:
        # print border
        print(key + " | ", end="")
        # print letter and a space
        for letter in board_dict[key]:
            print(letter + "  ", end="")

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
            if li > cu.grid_length:
                # make sure the board is getting only the right icons
                if letter in board_data.possible_board_icons:
                    new_row.append(letter)

            li += 1
        cu.current_board[cu.num_to_az[ri]] = new_row
        ri += 1

    return cu.current_board


def get_board():
    checker_board = []
    ci = 1
    for row in range(1, board_data.num_rows + 1):
        if row % 2 == 0:
            checker_board.append(cu.num_to_az[ci] + " | " + board_data.even_row + " |")
        else:
            checker_board.append(cu.num_to_az[ci] + " | " + board_data.odd_row + " |")

        ci += 1

    return checker_board


# Move
def get_move():
    print("Example Move: A1,B2")
    _move = input("What is your move\n").upper()
    interpret_move(_move)


def valid_icon(icon):
    print(
        f"ERROR: Expected command to give coordinates to {board_data.possible_board_icons}, and instead got {icon}"
    )
    return icon in board_data.possible_board_icons


def possible_piece(icon):
    if icon not in board_data.checkers:
        print(
            f"ERROR: Expected command to give coordinates to {board_data.checkers}, and instead got {icon}"
        )
        get_move()
        return False

    return True


def interpret_move(_move):
    cu.has_jumped = False

    # if the move isn't long enough length to be the right command send error
    if len(_move) != 5:
        if _move.lower() == "print board":
            print_board()
        elif _move.lower() == "exit":
            global game_over
            game_over = True
            return

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
    if _move[0] in cu.current_board:
        start_row = cu.current_board[first_move[0]]
        start_col = int(first_move[1]) - 1
        start_icon = start_row[start_col]

        print(start_icon)

        # Second Command
        if _move[3] in cu.current_board:
            end_row = cu.current_board[second_move[0]]
            end_col = int(second_move[1]) - 1
            end_icon = end_row[end_col]

            r_jump_size = abs(ord(str(_move[0])) - ord(str(_move[3])))
            c_jump_size = abs(start_col - end_col)

            middle_row = chr(int((abs(ord(_move[0]) + ord(_move[3]))) / 2))
            middle_column = int(abs(start_col + end_col) / 2)
            middle_icon = cu.current_board[middle_row][middle_column]

            # ERROR CHECKING---------------------------------
            if not possible_piece(start_icon):
                print("ERROR: not a valid place to begin your move")
                get_move()
                return

            if not valid_icon(end_icon):
                print("ERROR: not a valid place to end your move")
                get_move()
                return

            # If they don't land on an empty square
            if end_icon != "1":
                print("ERROR: End square is occupied")
                get_move()
                return

            # Black Specific Errors --------------------------------

            # if it's black's turn and you move a white piece
            if start_icon.lower() == "w":
                if not cu.whites_turn:
                    print("ERROR: you tried to move a white piece on blacks turn")
                    get_move()
                    return

                # Don't allow backwards moves
                if start_icon == "w":
                    if ord(str(_move[0])) - ord(str(_move[3])) > 0:
                        print("ERROR: Can't move backwards without a King")
                        get_move()
                        return

            # White Specific Errors --------------------------------
            # if it's white's turn and you move a black piece
            if start_icon.lower == "b":
                if cu.whites_turn:
                    print("ERROR: you tried to move a Black piece on Whites turn")
                    get_move()
                    return

                # Don't allow backwards moves
                if start_icon == "b":
                    if ord(str(_move[0])) - ord(str(_move[3])) < 0:
                        print("ERROR: Can't move backwards without a King")
                        get_move()
                        return

            # Make sure if jumping it's a proper jump
            if c_jump_size != 1 or r_jump_size != 1:
                if c_jump_size != 2 or r_jump_size != 2:
                    print("ERROR: you can only move 1 column at a time")
                    get_move()
                    return

                # if there is no checker to jump then don't allow the jump
                if middle_icon == "1" or middle_icon == "0":
                    print("ERROR: You can only move 1 row at a time")
                    get_move()
                    return

                cu.has_jumped = True

            # ERROR CHECKING------------------------------------

            # JUMPING
            if cu.has_jumped:
                # Take piece
                cu.current_board[middle_row][middle_column] = "1"
                cu.has_jumped = True

            # King them if they're on the last row of opposing side
            if second_move[0] == "A" and start_icon == "b":
                cu.current_board[second_move[0]][int(second_move[1]) - 1] = "B"
            elif (
                second_move[0] == chr(ord("A") + board_data.num_rows - 1)
                and start_icon == "w"
            ):
                cu.current_board[second_move[0]][int(second_move[1]) - 1] = "W"
            else:
                # set the moved to square as having a piece
                cu.current_board[second_move[0]][int(second_move[1]) - 1] = start_icon

            # set the first square to blank
            cu.current_board[first_move[0]][int(first_move[1]) - 1] = "1"

            if not cu.has_jumped:
                cu.whites_turn = not cu.whites_turn

            # save move to move_history
            cu.move_history.append(first_move + second_move)
            return
    else:
        print(f"{_move[0]} is not in current_board")
        print(cu.current_board)


def check_win():
    num_black = 0
    num_white = 0
    for key in cu.current_board:
        for row in cu.current_board[key]:
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
    cu.current_board = place_beginning_checkers()
    while not game_over:
        print_board()
        get_move()
        if not game_over:
            game_over = check_win()
