# S poganjanjem skripte generiramo igre in jih klasificiramo kot lahke / srednje / tezke 

import game_functions as gf 
import sys 
import random 
import pandas as pd
import datetime

# m = 3; n = 3
# game, grid = gf.get_game(m, n)
# print(game)
# print(grid)

# tezavnost, ocena = gf.get_rating(grid, game, m, n)
# print(tezavnost, ocena)
# sys.exit() 

dimenzije = [(3, 3), (2, 3), (2, 4)]

def generate_games(dimenzije, max_count, csv_file_name):
    random.seed(0)
    global_count = 0
    df = []
    for dimenzija in dimenzije: 
        print("Igre za dimenzijo", dimenzija)
        count = 0
        m, n = dimenzija 
        while count < max_count:
            try:
                start_generate = datetime.datetime.now()
                game, grid, unique = gf.get_game(m, n)
                end_generate = datetime.datetime.now()
                string = game_to_string(game)
                start_rating = datetime.datetime.now()
                tezavnost = gf.rate_game(grid, game, m, n)
                end_rating = datetime.datetime.now()
                trajanje_generate = end_generate - start_generate
                trajanje_rating = end_rating - start_rating
                if tezavnost is None:
                    ... 
                else:
                    hints = gf.count_hints(game)
                    count += 1
                    global_count += 1
                    df.append([global_count, m, n, game_to_string(game), game_to_string(grid), hints, tezavnost, unique, trajanje_generate.total_seconds(), trajanje_rating.total_seconds()])
                    print("Imamo igro stevilka", count)
            except:
                ...
    
    df = pd.DataFrame(df)
    df.columns = ["ID", "m", "n", "game", "solution", "hints", "difficulty", "unique", "generating time", "rating time"]
    df.to_csv(csv_file_name)