# S poganjanjem skripte generiramo igre in jih klasificiramo kot lahke / srednje / tezke 

import game_functions as gf 
import sys 
import random 

random.seed(0)
# m = 3; n = 3
# game, grid = gf.get_game(m, n)
# print(game)
# print(grid)

# tezavnost, ocena = gf.get_rating(grid, game, m, n)
# print(tezavnost, ocena)
# sys.exit() 

random.seed(0)

dimenzije = [(3, 3), (2, 4), (4, 2), (5, 2), (2, 5)]
dimenzije = [(3, 3)]
global_count = 0
for dimenzija in dimenzije: 
    count = 0
    m, n = dimenzija 
    while count < 25:
        count += 1
        global_count += 1
        try:
            game, grid = gf.get_game(m, n)
        except:
            ...
        string = gf.game_to_string(game)
        tezavnost, ocena = gf.get_rating(grid, game, m, n)
        print(tezavnost, ocena)

        name = "games/sudoku_game_" + str(global_count) + "_size_" + str(m) + "_" + str(n) + "_zahtevnost_" + tezavnost + "_" + str(ocena) + ".txt"
        
        with open(name, "w") as text_file:
            text_file.write(string)