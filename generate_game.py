# S poganjanjem skripte generiramo igre in jih klasificiramo kot lahke / srednje / tezke 

import game_functions as gf 
import sys 
import random 
import pandas as pd
random.seed(0)

def game_to_string(game): 
    string = "" 
    for el in game: 
        for znak in el: 
            if znak is None: 
                string += "."
            else:
                string += str(znak)
    return string 

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
df = []
for dimenzija in dimenzije: 
    count = 0
    m, n = dimenzija 
    while count < 1:
        try:
            game, grid, unique = gf.get_game(m, n)
            string = game_to_string(game)
            tezavnost = gf.rate_game(grid, game, m, n)
            if tezavnost is None: 
                print("Igra ne bo veljavna!!")
            else:
                hints = gf.count_hints(game)
                print(tezavnost)
                gf.plot_game(game)
                count += 1
                global_count += 1
                print("\n------------------------\n")
                df.append([global_count, m, n, game_to_string(game), game_to_string(grid), hints, tezavnost, unique])
        except:
            ...
 
df = pd.DataFrame(df)
df.columns = ["ID", "m", "n", "game", "solution", "hints", "difficulty", "unique"]

print(df)