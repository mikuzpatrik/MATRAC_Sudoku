



import os
import game_functions as gf
import datetime 
import pandas as pd
import sys 
import numpy as np 
import matplotlib.pyplot as plt
import random 
random.seed(0)

def test_games(dataset, csv_file_name, sample_less_7 = 30, sample_more_7 = 10, seed_repeat = 10):
    df_games = dataset.copy()
    df_games["difficulty_int"] = np.round(df_games["difficulty"], 0)
    all_tezavnosti = list(df_games["difficulty_int"].drop_duplicates())
    random.seed(0)
    ids = [] 
    for tezavnost in all_tezavnosti: 
        list_of_indeks = list(df_games[df_games["difficulty_int"] == tezavnost]["id"])
        if tezavnost <= 7: 
            rand_ids = random.sample(list_of_indeks, sample_less_7)
        else: 
            rand_ids = random.sample(list_of_indeks, sample_more_7)
        ids += rand_ids 

    df_games = df_games[df_games["id"].isin(ids)]

    print("Vseh sudokujev v testni množici je", len(df_games))
    print("Najtežji sudoku v množici ima težavnost", df_games["difficulty"].max())
    print("Povprečna težavnost množice je", df_games["difficulty"].mean())

    puzzles = list(df_games["puzzle"])
    tezavnosti = list(df_games["difficulty"])
    tezavnosti_int = list(df_games["difficulty_int"])
    ids = list(df_games["id"])
    List_of_games = []
    for i in range(len(puzzles)): 
        sudoku = puzzles[i] 
        game = gf.read_sudoku(sudoku, 3, 3)
        List_of_games.append(game)


    Df = pd.DataFrame([])
    for i in range(len(List_of_games)):
        game = List_of_games[i]
        print("Igramo igro", str(i+1), "/", str(len(List_of_games)), "z tezavnostjo", tezavnosti[i])
        print("Stevilo namigov:", gf.count_hints(game))
        df_game = []
        for seed in range(seed_repeat):
            random.seed(seed)
            start = datetime.datetime.now()
            _, stevilo_poskusov, globina = gf.random_solver(game, 3, 3, with_logic=True)
            end = datetime.datetime.now() 
            time = end - start
            df_game.append([seed, ids[i], tezavnosti[i], tezavnosti_int[i], time.total_seconds(), stevilo_poskusov, globina])

        df_game = pd.DataFrame(df_game)

        Df = pd.concat([Df, df_game])

    Df.columns = ["seed", "id", "difficulty", "difficulty_int", "time", "number_of_try", "depth"]

    print(Df)

    Df.to_csv(csv_file_name)


def compare_random_logic(dataset, csv_file_name, sample = 2, max_tezavnost = 5, seed_repeat = 5):
    df_games = dataset.copy()
    df_games["difficulty_int"] = np.round(df_games["difficulty"], 0)
    all_tezavnosti = list(df_games["difficulty_int"].drop_duplicates())
    random.seed(0)
    ids = [] 
    for tezavnost in all_tezavnosti: 
        if tezavnost >= max_tezavnost:
            continue
        list_of_indeks = list(df_games[df_games["difficulty_int"] == tezavnost]["id"])
        rand_ids = random.sample(list_of_indeks, sample)
        ids += rand_ids 

    df_games = df_games[df_games["id"].isin(ids)]

    puzzles = list(df_games["puzzle"])
    tezavnosti = list(df_games["difficulty"])
    tezavnosti_int = list(df_games["difficulty_int"])
    ids = list(df_games["id"])
    List_of_games = []
    for i in range(len(puzzles)): 
        sudoku = puzzles[i] 
        game = gf.read_sudoku(sudoku, 3, 3)
        List_of_games.append(game)


    Df = pd.DataFrame([])
    for i in range(len(List_of_games)):
        print("Igramo igro", str(i+1), "/", str(len(List_of_games)), "z tezavnostjo", tezavnosti[i])
        for logic in [True, False]:
            game = List_of_games[i]
            df_game = []
            for seed in range(seed_repeat):
                random.seed(seed)
                start = datetime.datetime.now()
                _, stevilo_poskusov, globina = gf.random_solver(game, 3, 3, with_logic=logic)
                end = datetime.datetime.now() 
                time = end - start
                df_game.append([seed, ids[i], tezavnosti[i], tezavnosti_int[i], time.total_seconds(), stevilo_poskusov, globina, logic])

            df_game = pd.DataFrame(df_game)

            Df = pd.concat([Df, df_game])

    Df.columns = ["seed", "id", "difficulty", "difficulty_int", "time", "number_of_try", "depth", "logic"]

    print(Df)

    Df.to_csv(csv_file_name)


def test_on_hardest_sudoku(csv_file_name, seed_repeat = 10):
    hardest_game = "8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4.."
    game = gf.read_sudoku(hardest_game, 3, 3)

    df_game = []
    for seed in range(seed_repeat):
        print("Random seed:", seed)
        random.seed(seed)
        start = datetime.datetime.now()
        _, stevilo_poskusov, globina = gf.random_solver(game, 3, 3, with_logic=True)
        end = datetime.datetime.now() 
        time = end - start
        print("Čas izvajanja:", time)
        df_game.append([seed, time.total_seconds(), stevilo_poskusov, globina])

    df_game = pd.DataFrame(df_game)
    df_game.columns = ["seed", "time", "number_of_try", "depth"]
    df_game.to_csv(csv_file_name)

def generate_games(dimenzije, csv_file_name, max_count = 20):
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
                    df.append([global_count, m, n, gf.game_to_string(game), gf.game_to_string(grid), hints, tezavnost, unique, trajanje_generate.total_seconds(), trajanje_rating.total_seconds()])
                    print("Imamo igro stevilka", count)
            except:
                ...
    
    df = pd.DataFrame(df)
    df.columns = ["ID", "m", "n", "game", "solution", "hints", "difficulty", "unique", "generating time", "rating time"]
    df.to_csv(csv_file_name)

def get_csv_files(): 
    dataset = pd.read_csv("sudoku-3m.csv")
    dimenzije = [(3, 3), (2, 3), (2, 4)]
    test_games(dataset, csv_file_name="files/testing_set_results.csv")
    compare_random_logic(dataset, csv_file_name="files/random_with_without_logic.csv", sample = 2)
    test_on_hardest_sudoku(csv_file_name="files/hardest_sudoku_testing.csv")
    generate_games(dimenzije=dimenzije, csv_file_name="files/new_games.csv")

# funkcija get_csv_files() generira csv-je
# get_csv_files()


def group_and_calculate(df, group_by, calculate):

    df_group = df[[group_by, calculate]].groupby(group_by).agg({calculate: ["mean", "min", "max"]}).reset_index()
    df_group.columns = [group_by, "mean", "min", "max"]
    return df_group

# df_group_int = group_and_calculate(df, "difficulty_int", "time")
# plt.plot(df_group_int["difficulty_int"], df_group_int["mean"])
# plt.plot(df_group_int["difficulty_int"], df_group_int["min"])
# plt.plot(df_group_int["difficulty_int"], df_group_int["max"])
# plt.legend(["mean", "min", "max"])
# plt.show()


# df_group = group_and_calculate(df, "difficulty", "time")
# plt.plot(df_group["difficulty"], df_group["mean"])
# plt.show()


# df_group = group_and_calculate(df, "difficulty_int", "number_of_try")
# plt.plot(df_group["difficulty_int"], df_group["mean"])
# plt.show()


# df_group = group_and_calculate(df, "difficulty_int", "depth")
# plt.plot(df_group["difficulty_int"], df_group["mean"])
# plt.show()

# dataset = pd.read_csv("sudoku-3m.csv")
# dataset["difficulty_int"] = np.round(dataset["difficulty"], 0)
# all_tezavnosti = list(dataset["difficulty_int"].drop_duplicates())

# print("Najtežji sudoku v datasetu ima težavnost", dataset["difficulty"].max())
# print("Povprečna težavnost dataseta je", dataset["difficulty"].mean())

# Poberem 100 sudokujev vsake tezavnosti, pri cemer tezavnost zaokrozim na celo stevilo
# dataset["difficulty_int"] = np.round(dataset["difficulty"], 0)
# all_tezavnosti = list(dataset["difficulty_int"].drop_duplicates())

# generate_csv(dataset)

# compare_random_logic(dataset)

# test_on_hardest_sudoku()

