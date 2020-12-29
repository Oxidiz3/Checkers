"""
    Porter Mecham full game of checkers with procedural board lengths
    complete with jumping and kinging logic.
"""

import checkers_util as cu
from checkers_util import BoardData


board_data = BoardData(cu.row_length, cu.column_length, cu.GRID_LENGTH)

# Print
def print_header():
    """print's top of board"""

    print("\n\nCHECKER BOARD by\nPorter Mecham\n" + "_" * (cu.GRID_LENGTH + 1), end="")

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
    """print's bottom of board, whose move it is and whether there are any jumps"""
    print("_" * (cu.GRID_LENGTH + 1 + (board_data.num_columns * 3)))

    if len(cu.move_history) != 0:
        print("Last Move:", cu.move_history[-1])
    if cu.whites_turn:
        print("White's Turn")

        if len(cu.w_possible_jumps) > 0:
            print("You must jump")
            for jump in cu.w_possible_jumps:
                print(jump)
    else:
        print("Black's Turn")
        if len(cu.b_possible_jumps) > 0:
            for jump in cu.b_possible_jumps:
                print("You must jump")
                print(jump)


def print_board():
    """print's the checkerboard """
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
    """generates beginning boar

    Returns:
        Board_Data: returns the starting board
    """
    new_checker_board = []
    r_i = 0

    for row in create_board():
        r_i += 1
        new_row = ""

        # if on top half of the board place white checkers
        if r_i < board_data.num_rows / 2:
            for letter in row:
                if letter == "1":
                    new_row += "w"
                else:
                    new_row += letter
        # if on bottom half of the board place Black checkers
        elif r_i > (board_data.num_rows / 2) + 1:
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

    r_i = 1
    # put the default board to the current_board dict
    for row in new_checker_board:
        l_i = 0
        new_row = []
        # go through each letter
        for letter in row:
            # don't get the Grid on the outside of the board
            if l_i > cu.GRID_LENGTH:
                # make sure the board is getting only the right icons
                if letter in board_data.possible_board_icons:
                    new_row.append(letter)

            l_i += 1
        cu.current_board[cu.NUM_TO_AZ[r_i]] = new_row
        r_i += 1

    return cu.current_board


def create_board():
    """creates board out of settings in
        cu

    Returns:
        list: the finished checkboard
    """
    checker_board = []
    for row in range(1, board_data.num_rows + 1):
        if row % 2 == 0:
            checker_board.append(cu.NUM_TO_AZ[row] + " | " + board_data.even_row + " |")
        else:
            checker_board.append(cu.NUM_TO_AZ[row] + " | " + board_data.odd_row + " |")

    return checker_board


def look_for_possible_jumps_on_board():
    """see if any piece on board can jump then put jump in a list"""
    cu.w_possible_jumps.clear()
    cu.b_possible_jumps.clear()

    for row in cu.current_board:
        for col in range(1, cu.column_length + 1):
            coord = str(row) + str(col)
            icon = cu.coord_to_icon(coord)
            if icon in cu.possible_board_pieces:
                piece_can_jump(coord, icon)


# Move
def get_move():
    """get move from player(s) """
    print("Example Move: A1,B2")
    _move = input("What is your move\n").upper()
    interpret_move(_move)


def interpret_move(_move: str):
    """take move check if its a valid move then make it do it's logic

    Args:
        _move (str): move input from get_move()
    """
    start_pos = _move[0:2]
    end_pos = _move[3:5]

    if errors_in_input(_move):
        return

    # First Command
    if _move[0] in cu.current_board:
        start_row = cu.current_board[start_pos[0]]
        start_col = int(start_pos[1]) - 1
        start_icon = start_row[start_col]

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

    is_jump = move_is_jump(_move)
    if is_jump:
        if lawful_jump(_move, start_col, end_col):
            take_piece(_move)
        else:
            return
    do_king_logic(end_pos, start_icon)

    # set the first square to blank
    cu.current_board[start_pos[0]][int(start_pos[1]) - 1] = "1"

    # check for double jump
    if is_jump:
        board_coords = end_pos[0] + "," + end_pos[1]
        if piece_can_jump(end_pos, start_icon):
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
def valid_icon(icon) -> bool:
    """check if icon is valid

    Args:
        icon (str): icon

    Returns:
        bool: if icon is in possible board icons
    """
    return icon in board_data.possible_board_icons


def possible_piece(icon: str) -> bool:
    """is icon a checker piece?

    Args:
        icon (str): piece

    Returns:
        bool: if icon is a checker piece
    """
    if icon not in board_data.checkers:
        print(
            f"ERROR: Expected command to give coordinates to {board_data.checkers}, and instead got {icon}"
        )
        return False

    return True


def errors_in_input(_move: str) -> bool:
    """check for errors in input

    Args:
        _move (str): move from player

    Returns:
        bool: errors in input
    """
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
        print("ERROR: letter where there should be a number")
        return True

    return False


def errors_in_move(_move: str, start_icon: str, end_icon: str) -> bool:
    """check if move is a valid move
    Returns:
        bool: if errors in move
    """
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

    # if it's black's turn and you move a white piece
    if start_icon.lower() == "w":
        if not cu.whites_turn:
            print("ERROR: you tried to move a white piece on blacks turn")
            return True
        else:
            # if they aren't jumping and they must jump
            if len(cu.w_possible_jumps) > 0:
                if _move not in cu.w_possible_jumps:
                    return True

        # Don't allow backwards moves
        if start_icon == "w":
            if ord(str(_move[0])) - ord(str(_move[3])) > 0:
                print("ERROR: Can't move backwards without a King")
                return True

    # White Specific Errors --------------------------------
    # if it's white's turn and you move a black piece
    if start_icon.lower() == "b":
        if cu.whites_turn:
            print("ERROR: you tried to move a Black piece on Whites turn")
            return True
        else:
            # if they aren't jumping and they must jump
            if len(cu.b_possible_jumps) > 0:
                if not cu.whites_turn:
                    if _move not in cu.b_possible_jumps:
                        return True

        # Don't allow backwards moves
        if start_icon == "b":
            if ord(_move[0]) - ord(_move[3]) < 0:
                print("ERROR: Can't move backwards without a King")
                return True

    return False


# Error Check end


# Logic
def move_is_jump(_move) -> bool:
    # Make sure jumping to empty space and not over or under jumping
    jump = False

    r_jump_size = abs(ord(_move[0]) - ord(_move[3]))
    c_jump_size = abs(int(_move[1]) - int(_move[4]))

    if c_jump_size != 1 or r_jump_size != 1:
        jump = True

    return jump


def lawful_jump(_move, start_col, end_col) -> bool:
    # Make sure jumping to empty space and not over or under jumping
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

    return jump


def take_piece(_move):
    start_col = int(_move[1])
    end_col = int(_move[4])

    # change letters to numbers then get average then return to letter
    middle_row = chr(int((abs(ord(_move[0]) + ord(_move[3]))) / 2))
    middle_column = int(abs(start_col + end_col) / 2) - 1
    cu.current_board[middle_row][middle_column] = "1"


def piece_can_jump(piece_coordinates, icon) -> bool:
    can_jump = False

    pos = piece_coordinates
    row = cu.AZ_TO_NUM[pos[0]]
    col = int(pos[1])

    close_coords = []
    empty_far_coords = []
    jumpable_pieces_coord = []

    if icon == "b" or icon.isupper():
        if row - 2 > 0:
            # tile exists
            if col + 2 <= cu.column_length:
                tile = str(cu.NUM_TO_AZ[row - 2]) + str(col + 2)
                # tile is empty
                if cu.coord_to_icon(tile) == "1":
                    empty_far_coords.append(tile)
                else:
                    empty_far_coords.append(0)
            else:
                empty_far_coords.append(0)
            if col - 2 > 0:
                tile = str(cu.NUM_TO_AZ[row - 2]) + str(col - 2)
                # tile is empty
                if cu.coord_to_icon(tile) == "1":
                    empty_far_coords.append(tile)
                else:
                    empty_far_coords.append(0)
            else:
                empty_far_coords.append(0)
    else:
        # if it's a white stick in two blanks so it's in the right spot
        empty_far_coords.append(0)
        empty_far_coords.append(0)

    if icon == "w" or icon.isupper():
        if row + 2 <= cu.row_length:
            # tile exists
            if col + 2 <= cu.column_length:
                tile = str(cu.NUM_TO_AZ[row + 2]) + str(col + 2)
                # tile is empty
                if cu.coord_to_icon(tile) == "1":
                    empty_far_coords.append(tile)
                else:
                    empty_far_coords.append(0)
            else:
                empty_far_coords.append(0)
            if col - 2 > 0:
                tile = str(cu.NUM_TO_AZ[row + 2]) + str(col - 2)
                # tile is empty
                if cu.coord_to_icon(tile) == "1":
                    empty_far_coords.append(tile)
                else:
                    empty_far_coords.append(0)
            else:
                empty_far_coords.append(0)

    # get inside coords
    for coord in empty_far_coords:
        if coord != 0:
            close_coords.append(cu.get_middle_coords(piece_coordinates, coord))
        else:
            close_coords.append(0)

    # check if inside coords are jumpable pieces
    for index, coord in enumerate(close_coords):
        x = 0

        if coord != 0:
            coord_icon = cu.coord_to_icon(coord)
            if icon.lower() == "w":
                # white attack
                if coord_icon.lower() == "b":
                    # have empty space to jump to
                    if empty_far_coords[index] != 0:
                        x = coord
                        can_jump = True

            elif icon.lower() == "b":
                # black attack
                if coord_icon.lower() == "w":
                    # have empty space to jump to
                    if empty_far_coords[index] != 0:
                        x = coord
                        can_jump = True

        if x != 0:
            jumpable_pieces_coord.append(x)

            if icon.lower() == "w":
                cu.w_possible_jumps.append(
                    str(piece_coordinates + "," + empty_far_coords[index])
                )
            else:
                cu.b_possible_jumps.append(
                    str(piece_coordinates + "," + empty_far_coords[index])
                )

    return can_jump


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
        print_board()
        print("WHITE HAS WON")
        print(f"White {num_white}, Black {num_black}")
        return True
    if num_white == 0:
        print_board()
        print("BLACK HAS WON")
        print(f"White {num_white}, Black {num_black}")
        return True


# Main
if __name__ == "__main__":
    # initialize
    cu.current_board = place_beginning_checkers()
    while not cu.game_over:
        look_for_possible_jumps_on_board()
        print_board()
        get_move()
        if not cu.game_over:
            cu.game_over = check_win()
