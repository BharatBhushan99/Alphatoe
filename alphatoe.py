lst = list(range(9))

def hash_table_init():
    hash_table = []
    for num in range(19683):
        new_board = board_structure()
        hash_table.append(new_board)
    return hash_table

class board_structure():
    
    def __init__(self):
        self.init = None
        self.turn = None
        self.depth = None
        self.board = None
        self.winner = None
        self.moves = ['-','-','-', '-', '-', '-', '-', '-', '-']
        self.score = -99

def init_boards():
    for num in range(19683):
        table[num].init = False

def board_depth(arg_board):
    markers = 0
    for element in arg_board:
        if element == 'X' or element == 'O':
            markers += 1
    return markers 

def turn_compute(arg_board):
    markers = board_depth(arg_board)
    
    if markers % 2 == 0 and markers != 9 and winner(arg_board) == '?':
        return 'X'
    elif markers % 2 == 1 and markers != 9 and winner(arg_board) == '?':
        return 'O'
    else:
        return '-'

def winner(arg_board):
    
    numX = None
    numO = None
    
    for i in range(8):
        numX = 0
        numO = 0
        for j in range(3):
            if arg_board[win_lst[i][j]] == 'X':
                numX += 1
            elif arg_board[win_lst[i][j]] == 'O':
                numO += 1
        if numX == 3:
            return 'X'
        elif numO == 3:
            return 'O'
            
    if board_depth(arg_board) == 9:
        return '-'
    else:
        return '?'

def init_board(arg_board):
    index = board_hash(arg_board)
    table[index].init = True
    table[index].turn = turn_compute(arg_board)
    table[index].depth = board_depth(arg_board)
    table[index].winner = winner(arg_board)
    table[index].board = arg_board.copy()

def join_graph(arg_board):
    copy_index = None
    index = board_hash(arg_board)
   # print("Arg_board in begining")
   # print(arg_board)
    board_copy = None
    
    if table[index].winner == 'X' or table[index].winner == 'O':
        for num in range(9):
            table[index].moves[num] = -1
    
    else:
        for num in range(9):
            if arg_board[num] == 'X' or arg_board[num] == 'O':
                table[index].moves[num] = -1
            else:
                board_copy = arg_board.copy()
                board_copy[num] = turn_compute(arg_board)
                table[index].turn = turn_compute(arg_board)
                copy_index = board_hash(board_copy)
                table[index].moves[num] = copy_index
                
                if table[copy_index].init != 1:
                    init_board(board_copy)
                    join_graph(board_copy)

def compute_score():
    
    min_num = None
    max_num = None
    
    i = 9
    while i > -1:
        
        for num in range(19683):
            min_num = 2
            max_num = -2
            
            if table[num].init == 1 and table[num].depth == i:
                
                if table[num].winner == '?':
                    if table[num].turn == 'X':
                        for k in range(9):
                            if table[num].moves[k] != -1:
                                if max_num < table[table[num].moves[k]].score:
                                    max_num = table[table[num].moves[k]].score
                        table[num].score = max_num   
                    elif table[num].turn == 'O':
                        for k in range(9):
                            if table[num].moves[k] != -1:
                                if min_num > table[table[num].moves[k]].score:
                                    min_num = table[table[num].moves[k]].score
                        table[num].score = min_num 
                else:
                    if table[num].winner == 'X':
                        table[num].score = 1
                    elif table[num].winner == 'O':
                        table[num].score = -1
                    else:
                        table[num].score = 0
        i -= 1

def best_mose(arg_board):
    index = None
    max_num = -2
    min_num = 2
    if table[arg_board].turn == 'X':
        for k in range(9):
            if table[arg_board].moves[k] != -1:
                if max_num < table[table[arg_board].moves[k]].score:
                    max_num = table[table[arg_board].moves[k]].score
                    index = k
    elif table[arg_board].turn == 'O':
        for k in range(9):
            if table[arg_board].moves[k] != -1:
                if min_num > table[table[arg_board].moves[k]].score:
                    min_num = table[table[arg_board].moves[k]].score
                    index = k
    return index     

win_lst = [[0,1,1+1],
           [3,3+1,5],
           [6,6+1,8],
           [0,3,6],
           [1,3+1,6+1],
           [1+1,5,8],
           [0,3+1,8],
           [2,2+2,6]]

def board_hash(arg_board):
    total = 0
    mult = 1
    for element in arg_board:
        if element == 'X':
            total += 2*mult
        elif element == 'O':
            total += 1*mult
        else:
            total += 0*mult
        mult *= 3
    return total    

def print_node(board_struct):
    print("**************************************************************\n")
    print(f"init={board_struct.init}\n")
    if board_struct.init:
        print(f"turn={board_struct.turn}\n")
        print(f"depth={board_struct.depth}\n")
        print( f"{board_struct.board[0]} | {board_struct.board[1]} | {board_struct.board[1+1]}\n--+---+--\n{board_struct.board[3]} | {board_struct.board[3+1]} | {board_struct.board[5]}\n--+---+--\n{board_struct.board[6]} | {board_struct.board[6+1]} | {board_struct.board[8]}\n")
        print(f"winner={board_struct.winner}\n")
        print(f"moves={board_struct.moves}\n")
        print(f"score={board_struct.score}\n")
    print("**************************************************************\n")

player_symbol = None
initial_board = list(range(9))
current_board = 0
next_board = -1
player_index = 99

table = hash_table_init()
init_boards()
init_board(initial_board.copy())
join_graph(initial_board.copy())
compute_score()

player_symbol = input("Player select your symbol (X or O): ")


while(table[current_board].turn in ['X', 'O']):
    print(f'{current_board}')
    if player_symbol == table[current_board].turn:
        while True:
            print_node(table[current_board])
            while True:
                try:
                    player_index = int(input("Select index [0-8]: "))
                except:
                    print("Incorrct input. Enter an index in [0-8]")
                else:
                    next_board = table[current_board].moves[player_index]
                    break
            if next_board != -1:
                break
            else:
                print("Incorrct input. Enter an index in [0-8]")
        current_board = next_board
    else:
        current_board = table[current_board].moves[best_mose(current_board)]
    print_node(table[current_board])
    
if table[current_board].winner == player_symbol:
    print("You won!")
        
elif table[current_board].winner == '-':
    print("Game tied.")
else:
    print("You lost")
