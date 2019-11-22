import random
#code goes to here.
EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}
USER = BLACK
AI = WHITE

UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

def squares():
    return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]

def initial_board():
#
    board = [OUTER] * 100
    for i in squares():
        board[i] = EMPTY

    board[44], board[45] = WHITE, BLACK
    board[54], board[55] = BLACK, WHITE
    return board

def print_board(board):
#
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
    for row in range(1, 9):
        begin, end = 10*row + 1, 10*row + 9
        rep += '%d %s\n' % (row, ' '.join(board[begin:end]))
    return rep

print_board(board = [OUTER] * 100)

#Mina Guo

#list all the legal moves -> int for moves xy
def all_valid_moves(player,board):
    return [sq for sq in squares() if is_valid(sq, board, player)]

#see if there're any valid moves -> True / False
def any_valid_moves(player, board):
    return any(is_valid(sq, board, player) for sq in squares())


#check the game status -> return tuple or int
def game_status(player, board):
    #there are valid moves, keep playing.
    if any_valid_moves(player, board) == True:
        return True
    else:
        opp = next_player(player)
        if score(player,board) > score(opp, board):
            return (player,1)
        elif score(player,board) < score(opp, board):
            return (opp,1)
        else:
            return (player, opp, 1)

#check score (difference in my pieces and opponent's)
def score(player, board):
    mine, oppo = 0,0
    opp = BLACK
    if player is WHITE:
        opp = BLACK
    else:
        opp = WHITE
    for sq in squares():
        piece = board[sq]
        if piece == player: 
            mine += 1
        elif piece == opp: oppo += 1
    return mine-oppo

#Yongyi Li

#validation -> return True or False
#(x,y) the new movement
def is_valid(move,board,player):
    if move/10 < 9 and move%10 < 9 and move/10 > 0 and move%10 > 0 and board[move] == '.' and max_score(move,player,board)>0:
        return True
    return False

#check if there's any reversion and reverse it if True
#-> return board and number of reversed pieces.
def reversion(move,board,player):
    count = 0
    cur = move
    flip = []
    for i in DIRECTIONS:
        cur = move
        cur += i
        while board[cur] == next_player(player):
            count += 1
            cur += i
        if board[cur] == player:
            flip.append(i)
        else:
            count = 0
    for i in flip:
        cur = move
        cur += i
        while board[cur] == next_player(player):
            board[cur] = player
            cur += i
    board[move] = player
    return board,count

#determine which player -> return player_id / player_name
def next_player(cur_player):
    if cur_player == BLACK:
        return WHITE
    return BLACK

#Mina & Yongyi
###STRATEGY###
#AI using random choice
def easy(board,player):
    return random.choice(all_valid_moves(player,board))

#score calculation for local max
def max_score(move,player,board):
    count = 0
    cur = move
    for i in DIRECTIONS:
        cur = move
        cur += i
        tmp = 0
        while board[cur] == next_player(player) and cur <89:
            tmp += 1
            cur += i
        if board[cur] != player:
            tmp = 0
        count += tmp
    return count

#AI using local max
def medium(board,player):
    move = -1
    max_count = -1
    for i in all_valid_moves(player,board):
        sc = max_score(i,player,board)
        if sc > max_count:
            move = i
            max_count = sc
    return move

square_weights = [
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
    0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
    0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
    0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
    0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
    0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
    0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
    0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
]
max_value = sum(map(abs, square_weights))
min_value = -max_value
#alpha_beta_value calculation for alpha-beta search
def alpha_beta_value(player, board):
    diff = score(player, board)
    if diff <0:
        return min_value
    elif diff > 0:
        return max_value
    return diff
    
#alpha-beta search
def alphabeta(player, board, alpha, beta, depth, evaluate):
    if depth == 0:
        return evaluate, None
    def value(board, alpha, beta):
        return -alphabeta(next_player(player), board, -beta, -alpha, depth-1, evaluate)[0]
    
    valid_moves = all_valid_moves(player, board)
    if not valid_moves:
        if not any_valid_moves(next_player(player), board):
            return alpha_beta_value(player,board), None
    best_move = valid_moves[0]
    for move in valid_moves:
        if alpha >= beta:
            break
            board,_ = reversion(move,board,player)
            val = value(board, alpha,beta)
            if val > alpha:
                alpha = val
                best_move = move
    return alpha, best_move

#alpha-beta search -> move
def hard(depth, evaluate, board):
    def decision(player, board):
        best = alphabeta(player, board, min_value, max_value, depth, evaluate)[1]
        if is_valid(best,board,player):
            return best
        else:
            return decision(player,board)
    return decision(WHITE, board)

#get move according to strategy and reversion -> return move(tuple)
def get_move(player,board,mode):
    if player == USER:
        while 1:
            move = input('Input your move:\n')
            try:
                move = int(move)
            except:
                print('Please enter a number')
                continue 
            if is_valid(move,board,player):
                break
            else:
                print('Invalid Input.')
        return move
    else:
        if mode == 'Easy':
            move = easy(board,player)
        if mode == 'Medium':
            move = medium(board,player)
        if mode == 'Hard':
            move = hard(5,player,board)
            #move = hard(5,next_player(player),board)
        return move
        
#play the game by calling get_move according to black / white strategies
#-> return board
def play(mode):
    board = initial_board()
    player = USER
    print_board(board)
    while 1:
        move = get_move(player,board,mode)
        reversion(move,board,player)
        print_board(board)
        player = next_player(player)
        result = game_status(player,board)
        if result != True:
            if len(result) == 3:
                print("Tie")
            else:
                print("Winner:",result[0])
            break
        

if __name__ == '__main__':
    while 1:
        mode = input("Select a game mode:Easy/Medium/Hard:\n")
        if mode in ['Easy','Medium','Hard']:
            break
    play(mode)

