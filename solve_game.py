# S poganjanjem skripte rešimo igro z osnovno / srednjo / napredno logiko 

import game_functions as gf 
import datetime 

# string = "..2.3...8.....8....31.2.....6..5.27..1.....5.2.4.6..31....8.6.5.......13..531.4.."
# string = ".......1.4.........2...........5.4.7..8...3....1.9....3..4..2...5.1........8.6..."
# lst = [[".",".",".",".",".",".",".","1","."],[".",".",".",".",".","2",".",".","3"],[".",".",".","4",".",".",".",".","."],[".",".",".",".",".",".","5",".","."],["4",".","1","6",".",".",".",".","."],[".",".","7","1",".",".",".",".","."],[".","5",".",".",".",".","2",".","."],[".",".",".",".","8",".",".","4","."],[".","3",".","9","1",".",".",".","."]]
# string = "" 
# for vrstica in lst:
#     substring = "" 
#     for el in vrstica:
#         substring += el
#     string += substring
# Hardest sudoku in the world 
# string = "8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4.."

# Se en tezek sudoku
# string = "1....7.9..3..2...8..96..5....53..9...1..8...26....4...3......1..41.....7..7...3.."

# test_string - solved
# string = ".179.36......8....9.....5.7.72.1.43....4.2.7..6437.25.7.1....65....3......56.172."

# test_string_2 - solved
# string = ".32..61..41..........9.1...5...9...4.6.....713...2...5...5.8.........519.57..986."

# sudoku_clanek - solved
# string = "2...8.3...6..7..84.3.5..2.9...1.54.8.........4.27.6...3.1..7.4.72..4..6...4.1...3"

# sudoku ga - solved
# string = "8.2..351..6..91..37.1...8946.8..4.21...258.6.92.31.4.....4.278...5.89...2....71.."

# random.seed(0) my sudoku - solved
# string = ".81......49...5..7.....78..5..3....6....492..2....1..5...9....48..25..7.....6..3."

# extreme_rating_sudoku.com - solved
# string = "....83.9.6.7...3..91........7.1...85...59......87......4..71.....6....5.8.......3"

# boxed-pair_test - solved
# string = ".16..78.3.9.8.....87...1.6..48...3..65...9.82.39...65..6.9...2..8...29369246..51."

# sudokus from page 
# difficulty: 253
# string = ".7.3...4.3...8.2..2.14.7...5.4....9..2.....5..1....7.3...9.63.2..2.3...9.6...2.8."
# difficulty: 451
# string = ".4...7.9..91.8....7.39.1....1..642.....5.8.....571..6....1.58.6....4.91..5.8...2."
# difficulty: 551
# string = "37...9..68..1.3.7.........8.2..8...5187...6425...2..1.7.........5.6.2..72..3...61"
# difficulty: 953
# string = "..3......8.946.7.22...186.......6.7...8...4...7.8.......294...55.6.328.7......2.."


game = []
for i in range(9):
    el = string[9*i:9*(i+1)]
    vrstica = []
    for znak in el:
        if znak == ".":
            vrstica.append(None)
        else:
            vrstica.append(int(znak))
    game.append(vrstica)

print("Stevilo namigov:", gf.count_hints(game))

start = datetime.datetime.now()
hints_before = 0
hints_now = gf.count_hints(game)
while hints_before != hints_now: 
    game, solvable = gf.naive_solver(game, 3, 3)
    hints_before = hints_now 
    hints_now = gf.count_hints(game)

solvable, solution, a, b, u = gf.advanced_solver(game, 3, 3, solutions=[], is_unique = True)

end = datetime.datetime.now() 

print("Trajanje:", end - start)