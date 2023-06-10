import engine as oz
import os

def choose():

    difficulty = 0
    option = input("Would you like to play against a bot ? (y/n) : ")
    if option == "n":
        option = "player"
    else:
        option = "bot"
        difficulty = int(input("Choose a difficulty (1-6) : "))
        while (difficulty > 1 or difficulty > 6):
            print("⚠️ Please choose a valid difficulty ! ⚠️")
            difficulty = int(input("Choose a difficulty (1-6) : "))

    return option, difficulty

def game():

    option, difficulty = choose()



    global canvas
    global coin_level
    global is_one_turn
    global yellow_pos
    global red_pos

    red_pos = set()
    yellow_pos = set()

    coin_level = [6 for c in range(0, 7)]
    is_one_turn = True

    canvas = oz.Canvas("⚪")
    cam = oz.Camera(canvas, {"x" : 7, "y": 6}, {"x" : 0, "y" : 0}, "cam" )

    while True:
        os.system("cls")
        print(cam.render())
        print_possible_input(get_possible_input(coin_level))
        action = int(input("enter : ")) # gets the action given as an int
        if action in get_possible_input(coin_level):
            place_coin(action)


            if is_one_turn:
                if get_coin_alignment(red_pos)["connect"]:
                    print("🔴 wins !")
                    action = input("would you like to play again (y/n) : ")
                    if action == "n":
                        exit()
                    else:
                        game()
            elif get_coin_alignment(yellow_pos)["connect"]:
                print("🟡 wins !")
                action = input("would you like to play again (y/n) : ")
                if action == "n":
                    exit()
                else:
                    game()
                    return

            print(cam.render())

            is_one_turn = not is_one_turn  # just inverses
            if option == "bot":
                print("	√+-/*  Calculating Best Move...")
                place_coin(minmax(yellow_pos, red_pos, coin_level, difficulty, True)[1])
                is_one_turn = not is_one_turn  # just inverses
        else:
            print("! Invalid !")






def get_possible_input(input : list):
    input = []
    i = 0
    for c in coin_level:
        if c != 0:
            input.append(i)
        i += 1
    return input


def print_possible_input(input : list):
    out = ""
    for i in input:
        out += str(i) + " "
    print(out)

def place_coin(x : int):


    y = coin_level[x] -1

    char = "🟡"
    # yellow-case

    if is_one_turn:
        char = "🔴"
        red_pos.add((x, y))
        # red-case
    else:
        yellow_pos.add((x, y))

    # place coin
    coin = oz.Sprite(canvas, char, {"x" : x, "y" : y}, "coin")
    coin_level[x] -= 1



def get_coin_alignment(board):

    dict = {}

    is_connect = False
    align = 0

    for c in board:

        dict = check_align(c, board, 0, -1)
        align += dict["align"]
        if is_connect == False:
            is_connect = dict["connect"]

        dict = check_align(c, board,0, 1)
        align += dict["align"]
        if is_connect == False:
            is_connect = dict["connect"]

        dict = check_align(c, board,-1, 0)
        align += dict["align"]
        if is_connect == False:
            is_connect = dict["connect"]

        dict = check_align(c, board,1, 0)
        align += dict["align"]
        if is_connect == False:
            is_connect = dict["connect"]

        dict = check_align(c, board,-1, 1)
        align += dict["align"]
        if is_connect == False:
            is_connect = dict["connect"]

        dict = check_align(c, board,1, 1)
        align += dict["align"]
        if is_connect == False:
            is_connect = dict["connect"]

        dict = check_align(c, board,-1, -1)
        align += dict["align"]
        if is_connect == False:
            is_connect = dict["connect"]

        dict = check_align(c, board,1, -1)
        align += dict["align"]
        if is_connect == False:
            is_connect = dict["connect"]

    return {"align" : align, "connect" : is_connect}



def check_align(coin, list_pos, x=0, y=0):
    is_4_connect = False
    # left case
    align = 0
    for i in range(1, 4):

        if (coin[0] + i * x, coin[1] + i * y) in list_pos:
            align += 1
        else:
            break



    if align == 3:
        is_4_connect = True


    if align == 0:
        return {"align" : 0, "connect" : is_4_connect}

    return {"align" : pow(align, align), "connect" : is_4_connect}


def minmax(y_board, r_board, cf_level , depth, is_max, alpha=float("-inf"), beta=float("+inf")):
    if depth == 0 or get_coin_alignment(y_board)["connect"]:
        return get_coin_alignment(y_board)["align"] - get_coin_alignment(r_board)["align"] * 1.01, None

    if is_max:

        best_score = float("-inf")
        best_move = None

        for move in get_possible_input(cf_level):
            new_board = y_board.copy()
            new_cf_level = cf_level.copy()
            new_cf_level[move] -= 1
            new_board.add((move, new_cf_level[move]))
            score, _ = minmax(new_board, r_board, new_cf_level, depth - 1, False)
            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, score)
            if alpha >= beta:
                break

        return best_score, best_move

    else:

        best_score = float("inf")
        best_move = None

        for move in get_possible_input(cf_level):
            new_board = r_board.copy()
            new_cf_level = cf_level.copy()
            new_cf_level[move] -= 1
            new_board.add((move, new_cf_level[move]))
            score, _ = minmax(y_board, new_board, new_cf_level, depth - 1, True)
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, score)
            if beta <= alpha:
                break

        return best_score, best_move


game()
