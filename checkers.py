# TODO: proper double jump logic
import checkers_util as cu
from checkers_util import BoardData


board_data = BoardData(cu.row_length, cu.column_length, cu.grid_length)

# Print
def print_header():
    print("CHECKER BOARD by\nPorter Mecham\n" + "_" * (cu.grid_length + 1), end="")

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
    for row in range(1, board_data.num_rows + 1):
        if row % 2 == 0:
            checker_board.append(cu.num_to_az[row] + " | " + board_data.even_row + " |")
        else:
            checker_board.append(cu.num_to_az[row] + " | " + board_data.odd_row + " |")

    return checker_board


# Move
def get_move():
    print("Example Move: A1,B2")
    _move = input("What is your move\n").upper()
    interpret_move(_move)


def interpret_move(_move):
    start_pos = _move[0:2]
    end_pos = _move[3:5]

    if errors_in_input(_move):
        return

    # First Command
    if _move[0] in cu.current_board:
        start_row = cu.current_board[start_pos[0]]
        start_col = int(start_pos[1]) - 1
        start_icon = start_row[start_col]

        print(start_icon)
    else:
        print(f"{start_pos} is not in current_board")
        print(cu.current_board)
        return

    # Second Command
    if _move[3] in cu.current_board:
        end_row = cu.current_board[end_pos[0]]
        end_col = int(end_pos[1]) - 1
        end_icon = end_row[end_col]
    else:
        print(f"{end_pos} is not in current_board")
        print(cu.current_board)
        return

    if errors_in_move(_move, start_icon, end_icon):
        return

    if not bad_jump(_move, start_col, end_col):
        return
    do_king_logic(end_pos, start_icon)

    # set the first square to blank
    cu.current_board[start_pos[0]][int(start_pos[1]) - 1] = "1"

    if can_jump_piece(end_pos, start_icon):
        cu.can_jump = True
        print(end_pos, "can jump a piece")
    else:
        cu.can_jump = False

    if not cu.can_jump:
        cu.whites_turn = not cu.whites_turn

    # save move to move_history
    cu.move_history.append(start_pos + end_pos)
    return


# Error Check
def valid_icon(icon):
    return icon in board_data.possible_board_icons


def possible_piece(icon):
    if icon not in board_data.checkers:
        print(
            f"ERROR: Expected command to give coordinates to {board_data.checkers}, and instead got {icon}"
        )
        return False

    return True


def errors_in_input(_move):
    if len(_move) != 5:
        if _move.lower() == "print board":
            print_board()
        elif _move.lower() == "exit":
            cu.game_over = True
            return True
        else:
            print(f"ERROR: expected 5 characters not {len(_move)}")
            return True
    # if there is a letter where there should be a number
    if _move[1].isalpha() or _move[4].isalpha():
        print(f"ERROR: letter where there should be a number")
        return True

    if can_jump_piece:
        if _move not in cu.possible_jumps:
            print("You must jump with")
            for jump in cu.possible_jumps:
                print(jump)
            return True

    return False


def errors_in_move(_move, start_icon, end_icon) -> bool:
    if not possible_piece(start_icon):
        print("ERROR: not a valid place to begin your move")
        return True

    if not valid_icon(end_icon):
        print(
            f"ERROR: Expected command to give coordinates to {board_data.possible_board_icons}, and instead got {end_icon}"
        )
        return True

    # If they don't land on an empty square
    if end_icon != "1":
        print("ERROR: End square is occupied")
        return True

    # Black Specific Errors --------------------------------

    # if it's black's turn and you move a white piece
    if start_icon.lower() == "w":
        if not cu.whites_turn:
            print("ERROR: you tried to move a white piece on blacks turn")
            return True

        # Don't allow backwards moves
        if start_icon == "w":
            if ord(str(_move[0])) - ord(str(_move[3])) > 0:
                print("ERROR: Can't move backwards without a King")
                return True

    # White Specific Errors --------------------------------
    # if it's white's turn and you move a black piece
    if start_icon.lower == "b":
        if cu.whites_turn:
            print("ERROR: you tried to move a Black piece on Whites turn")
            return True

        # Don't allow backwards moves
        if start_icon == "b":
            if ord(_move[0]) - ord(_move[3]) < 0:
                print("ERROR: Can't move backwards without a King")
                return True

    return False


# Error Check end


# Logic
def bad_jump(_move, start_col, end_col) -> bool:
    jump = False
    middle_row = chr(int((abs(ord(_move[0]) + ord(_move[3]))) / 2))
    middle_column = int(abs(start_col + end_col) / 2)
    middle_icon = cu.current_board[middle_row][middle_column]

    r_jump_size = abs(ord(_move[0]) - ord(_move[3]))
    c_jump_size = abs(start_col - end_col)

    # ERROR CHECKING
    # Make sure if attempting jump it's a proper jump
    if c_jump_size != 1 or r_jump_size != 1:
        if c_jump_size != 2 or r_jump_size != 2:
            print("ERROR: you can only move 1 column at a time")
            return False

        # if there is no checker to jump then don't allow the jump
        if middle_icon == "1" or middle_icon == "0":
            print("ERROR: You can only move 1 row at a time")
            return False

        jump = True

    #  movement
    if jump:
        # Take piece
        cu.current_board[middle_row][middle_column] = "1"

    return True


def can_jump_piece(piece_coordinates, icon) -> bool:
    possible_jump = False

    pos = piece_coordinates
    row = cu.az_to_num[pos[0]]
    col = int(pos[1])

    possible_surroundings_coord = []
    jumpable_pieces_coord = []

    # fill out surrounding_pieces if surrounding_pieces[x] == 0 then it should be taken as no piece
    if row + 2 <= cu.row_length:
        if col + 2 <= cu.column_length:
            coord_0 = str(cu.num_to_az[row + 1]) + str(col + 1)
            jumpable_pieces_coord.append(coord_0)
            possible_surroundings_coord.append(
                str(col + 2) + str(cu.num_to_az[row + 2])
            )
        else:
            possible_surroundings_coord.append(0)
        if col - 2 > 0:
            coord_1 = str(cu.num_to_az[row + 1]) + str(col - 1)
            jumpable_pieces_coord.append(coord_1)
            possible_surroundings_coord.append(
                str(col - 2) + str(cu.num_to_az[row + 2])
            )
        else:
            possible_surroundings_coord.append(0)
            jumpable_pieces_coord.append(0)
    if row - 2 > 0:
        if col - 2 in cu.current_board:
            coord_2 = str(cu.num_to_az[row - 1]) + str(col - 1)
            jumpable_pieces_coord.append(coord_2)
            possible_surroundings_coord.append(
                str(col - 2) + str(cu.num_to_az[row - 2])
            )
        else:
            jumpable_pieces_coord.append(0)
            possible_surroundings_coord.append(0)
        if col + 2 in cu.current_board:
            coord_3 = str(cu.num_to_az[row - 1]) + str(col + 1)
            jumpable_pieces_coord.append(coord_3)
            possible_surroundings_coord.append(
                str(col - 2) + str(cu.num_to_az[row - 2])
            )
        else:
            jumpable_pieces_coord.append(0)
            possible_surroundings_coord.append(0)

    print(possible_jump)
    print(cu.possible_jumps)

    # check surroundings for jumpable piece
    if icon == "w":
        i = 0
        for piece_coord in jumpable_pieces_coord[0:1]:
            if not piece_coord == 0:
                middle_icon = cu.current_board[piece_coord[0]][int(piece_coord[1])]

                print("Piece:", piece_coord)
                if middle_icon == "b" or middle_icon == "B":
                    cu.possible_jumps.append(
                        str(pos + "," + possible_surroundings_coord[i])
                    )
                    possible_jump = True
            i += 1
    elif icon == "W":
        i = 0
        for piece_coord in jumpable_pieces_coord[0:3]:
            if not piece_coord == 0:
                middle_icon = cu.current_board[piece_coord[0]][int(piece_coord[1])]

                if middle_icon == "b" or middle_icon == "B":
                    cu.possible_jumps.append(
                        str(pos + "," + possible_surroundings_coord[i])
                    )
                    possible_jump = True
            i += 1
    if icon == "b":
        i = 2
        for piece_coord in possible_surroundings_coord[2:3]:
            if not piece_coord == 0:
                middle_icon = cu.current_board[piece_coord[0]][int(piece_coord[1])]
                if middle_icon == "w" or middle_icon == "W":
                    cu.possible_jumps.append(
                        str(pos + "," + possible_surroundings_coord[i])
                    )
                    possible_jump = True
                i += 1
    elif icon == "B":
        i = 0
        for piece_coord in possible_surroundings_coord[0:3]:
            if not piece_coord == 0:
                middle_icon = cu.current_board[piece_coord[0]][int(piece_coord[1])]
                if middle_icon == "w" or middle_icon == "W":
                    cu.possible_jumps.append(
                        str(pos + "," + possible_surroundings_coord[i])
                    )
                    possible_jump = True
            i += 1

    return possible_jump


def do_king_logic(second_move, start_icon):
    # King them if they're on the last row of opposing side
    if second_move[0] == "A" and start_icon == "b":
        cu.current_board[second_move[0]][int(second_move[1]) - 1] = "B"
    elif (
        second_move[0] == chr(ord("A") + board_data.num_rows - 1) and start_icon == "w"
    ):
        cu.current_board[second_move[0]][int(second_move[1]) - 1] = "W"
    else:
        # set the moved to square as having a piece
        cu.current_board[second_move[0]][int(second_move[1]) - 1] = start_icon


# Logic End


def check_win():
    num_black = 0
    num_white = 0

    # get num blacks and whites in board
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


# Main
if __name__ == "__main__":
    # initialize
    cu.current_board = place_beginning_checkers()
    while not cu.game_over:
        print_board()
        get_move()
        if not cu.game_over:
            cu.game_over = check_win()
