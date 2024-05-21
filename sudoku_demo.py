



import os
import game_functions as gf
import datetime 
import pandas as pd
import sys 
import numpy as np 
import matplotlib.pyplot as plt
import random 

random.seed(0)

def read_sudoku(string, m, n): 
    game = []
    for i in range(m*n):
        el = string[m*n*i:m*n*(i+1)]
        vrstica = []
        for znak in el:
            if znak == ".":
                vrstica.append(None)
            else:
                vrstica.append(int(znak))
        game.append(vrstica)
    return game

def generate_csv(dataset):
    df_games = dataset.copy()
    df_games["difficulty_int"] = np.round(df_games["difficulty"], 0)
    all_tezavnosti = list(df_games["difficulty_int"].drop_duplicates())
    random.seed(0)
    ids = [] 
    for tezavnost in all_tezavnosti: 
        list_of_indeks = list(df_games[df_games["difficulty_int"] == tezavnost]["id"])
        if tezavnost <= 7: 
            rand_ids = random.sample(list_of_indeks, 30)
        else: 
            rand_ids = random.sample(list_of_indeks, 10)
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
        game = read_sudoku(sudoku, 3, 3)
        List_of_games.append(game)


    Df = pd.DataFrame([])
    for i in range(len(List_of_games)):
        game = List_of_games[i]
        print("Igramo igro", str(i+1), "/", str(len(List_of_games)), "z tezavnostjo", tezavnosti[i])
        print("Stevilo namigov:", gf.count_hints(game))
        df_game = []
        for seed in range(10):
            random.seed(seed)
            start = datetime.datetime.now()
            _, stevilo_poskusov, globina = gf.random_solver(game, 3, 3)
            end = datetime.datetime.now() 
            time = end - start
            df_game.append([seed, ids[i], tezavnosti[i], tezavnosti_int[i], time.total_seconds(), stevilo_poskusov, globina])

        df_game = pd.DataFrame(df_game)

        Df = pd.concat([Df, df_game])

    Df.columns = ["seed", "id", "difficulty", "difficulty_int", "time", "number_of_try", "depth"]

    print(Df)

    # Df.to_csv("testing_set_results.csv")

# df = pd.read_csv("testing_set_results.csv")
# print(df)

# def group_and_calculate(df, group_by, calculate):

#     df_group = df[[group_by, calculate]].groupby(group_by).agg({calculate: ["mean", "min", "max"]}).reset_index()
#     df_group.columns = [group_by, "mean", "min", "max"]
#     return df_group

# df_group_int = group_and_calculate(df, "difficulty_int", "time")
# plt.plot(df_group_int["difficulty_int"], df_group_int["mean"])
# # plt.plot(df_group_int["difficulty_int"], df_group_int["min"])
# # plt.plot(df_group_int["difficulty_int"], df_group_int["max"])
# # plt.legend(["mean", "min", "max"])
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


def compare_random_logic(dataset):
    df_games = dataset.copy()
    df_games["difficulty_int"] = np.round(df_games["difficulty"], 0)
    all_tezavnosti = list(df_games["difficulty_int"].drop_duplicates())
    random.seed(0)
    ids = [] 
    for tezavnost in all_tezavnosti: 
        if tezavnost >= 5:
            continue
        list_of_indeks = list(df_games[df_games["difficulty_int"] == tezavnost]["id"])
        rand_ids = random.sample(list_of_indeks, 1)
        ids += rand_ids 

    df_games = df_games[df_games["id"].isin(ids)]

    puzzles = list(df_games["puzzle"])
    tezavnosti = list(df_games["difficulty"])
    tezavnosti_int = list(df_games["difficulty_int"])
    ids = list(df_games["id"])
    List_of_games = []
    for i in range(len(puzzles)): 
        sudoku = puzzles[i] 
        game = read_sudoku(sudoku, 3, 3)
        List_of_games.append(game)


    Df = pd.DataFrame([])
    for i in range(len(List_of_games)):
        for logic in [True, False]:
            game = List_of_games[i]
            print("Igramo igro", str(i+1), "/", str(len(List_of_games)), "z tezavnostjo", tezavnosti[i])
            print("Stevilo namigov:", gf.count_hints(game))
            print("Uporabljamo logiko:", logic)
            df_game = []
            for seed in range(5):
                random.seed(seed)
                start = datetime.datetime.now()
                _, stevilo_poskusov, globina = gf.random_solver(game, 3, 3, with_logic=logic)
                end = datetime.datetime.now() 
                time = end - start
                print("Random seed:", seed)
                print("Čas izvajanja:", time)
                df_game.append([seed, ids[i], tezavnosti[i], tezavnosti_int[i], time.total_seconds(), stevilo_poskusov, globina, logic])

            df_game = pd.DataFrame(df_game)

            Df = pd.concat([Df, df_game])

    Df.columns = ["seed", "id", "difficulty", "difficulty_int", "time", "number_of_try", "depth", "logic"]

    print(Df)

    Df.to_csv("random_with_without_logic.csv")


def test_on_hardest_sudoku():
    hardest_game = "8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4.."
    game = read_sudoku(hardest_game, 3, 3)


    df_game = []
    for seed in range(10):
        print("Random see:", seed)
        random.seed(seed)
        start = datetime.datetime.now()
        _, stevilo_poskusov, globina = gf.random_solver(game, 3, 3, with_logic=True)
        end = datetime.datetime.now() 
        time = end - start
        print("Čas izvajanja:", time)
        df_game.append([seed, time.total_seconds(), stevilo_poskusov, globina])

    df_game = pd.DataFrame(df_game)

    df_game.columns = ["seed", "time", "number_of_try", "depth"]

    print(df_game)

    df_game.to_csv("hardest_sudoku_testing.csv")



dataset = pd.read_csv("sudoku-3m.csv")

print("Najtežji sudoku v datasetu ima težavnost", dataset["difficulty"].max())
print("Povprečna težavnost dataseta je", dataset["difficulty"].mean())

# Poberem 100 sudokujev vsake tezavnosti, pri cemer tezavnost zaokrozim na celo stevilo
dataset["difficulty_int"] = np.round(dataset["difficulty"], 0)
all_tezavnosti = list(dataset["difficulty_int"].drop_duplicates())

# generate_csv(dataset)

test_on_hardest_sudoku()

compare_random_logic(dataset)

