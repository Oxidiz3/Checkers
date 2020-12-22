import PySimpleGUI as sg
import checkers

# black squares
bs = sg.Image("images/bs.png", pad=((0, 0), 0))
bs_b = sg.Image("images/bs_b.png", pad=((0, 0), 0))
bs_w = sg.Image("images/bs_w.png", pad=((0, 0), 0))
bs_kb = sg.Image("images/bs_kB.png", pad=((0, 0), 0))
bs_kw = sg.Image("images/bs_kW.png", pad=((0, 0), 0))

# Red squares
rs = sg.Image("images/rs.png", pad=((0, 0), 0))
rs_b = sg.Image("images/rs_b.png", pad=((0, 0), 0))
rs_w = sg.Image("images/rs_w.png", pad=((0, 0), 0))
rs_kb = sg.Image("images/rs_kB.png", pad=((0, 0), 0))
rs_kw = sg.Image("images/rs_kW.png", pad=((0, 0), 0))

ras = bool

d_tiles = {
    "1": bs,
    "0": rs,
}

d_checkers = {
    "b": [bs_b, rs_b],
    "w": [bs_w, rs_w],
    "B": [bs_kw, rs_kb],
    "W": [bs_kw, rs_kw],
}


# noinspection PyTypeChecker
input_layout = [
    [sg.T("Number of rows"), sg.Input(default_text=8)],
    [sg.T("Number of columns"), sg.Input(default_text=8)],
    [
        sg.T("Starting color"),
        sg.Radio("White", "Radio", default=True, key="_White"),
        sg.Radio("Black", "Radio"),
    ],
    [sg.Submit(), sg.Cancel()],
]


def get_input():
    window = sg.Window("Get Data", input_layout)
    event, values = window.read()
    while True:
        if event == sg.WIN_CLOSED or event == "Cancel":
            break
        if event == "Submit":
            checkers.row_length = values[0]
            checkers.column_length = values[1]
            checkers.starting_color = values["_White"]
            break

    window.close()


def board_to_image(current_board):
    board_length = len(current_board.keys())
    l_board = []
    ki = 0

    for key in current_board:
        ki += 1
        for tile in current_board[key]:
            if tile in d_checkers:
                # black background
                if ki < (board_length / 2) + 1:
                    l_board.append(d_checkers[tile][0])
                # White background
                else:
                    l_board.append(d_checkers[tile][1])

            elif tile in d_tiles:
                l_board.append(d_tiles[tile])
            else:
                print(f"ERROR: tile:{tile} not in list")

    return l_board


def load_board():
    right_frame = [
        [
            sg.T(
                "Example Move",
                size=(60, 5),
                key="MoveList",
                text_color="black",
                background_color="white",
            )
        ],
        [
            sg.T("Command:"),
            sg.Input("", size=(30, 5), key="Command", do_not_clear=False),
        ],
        [sg.Submit()],
    ]

    left_frame = [board_to_image(checkers.current_board)]

    layout = [
        [
            sg.Frame("Checker Board", left_frame, title_color="blue"),
            sg.Frame("Moves and Commands", right_frame, title_color="white"),
        ]
    ]

    window = sg.Window("Checker Board", layout)
    event, values = window.read()
    while True:
        if event == sg.WIN_CLOSED or event == "Cancel":
            break
        elif event == "Submit":
            checkers.command_list.append(values["Command"])
            window["MoveList"].update(checkers.command_list)


def __main__():
    get_input()
    d_board = checkers.place_beginning_checkers()
    board_to_image(d_board)
    load_board()


if __name__ == "__main__":
    __main__()
