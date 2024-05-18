



import os
import game_functions as gf
import datetime 
import pandas as pd
import sys 
import numpy as np 
import matplotlib.pyplot as plt
import random 

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

List_of_games = []
Tezavnosti = []

df_games = pd.read_csv("sudoku-3m.csv")

print("Najtežji sudoku v množici ima težacnost", df_games["difficulty"].max())
print("Povprečna težavnost množice je", df_games["difficulty"].mean())

df = df_games[["id", "difficulty"]].groupby("difficulty").count().reset_index()
df.columns = ["difficulty", "count"]
df["count"] = np.where(df["count"] > 100, 100, df["count"])
df.sort_values(by="difficulty")

# plt.bar(df["difficulty"], df["count"])
# plt.show()

random.seed(0)
df_games = df_games.head(200)

print("Najtežji sudoku v množici ima težavnost", df_games["difficulty"].max())
print("Povprečna težavnost množice je", df_games["difficulty"].mean())

puzzles = list(df_games["puzzle"])
tezavnosti = list(df_games["difficulty"])
for i in range(len(puzzles)): 
    sudoku = puzzles[i] 
    tezavnost = tezavnosti[i]
    game = read_sudoku(sudoku, 3, 3)
    List_of_games.append(game)
    Tezavnosti.append(tezavnost)

total_time_start = datetime.datetime.now()

times = []
tezavnosti_reseni = []
neuspesno_reseni = []
tezavnosti_nereseni = []

for i in range(len(List_of_games)):

    game = List_of_games[i]
    tezavnost = Tezavnosti[i]
    print("Igramo igro", str(i+1), "/", str(len(List_of_games)), "z tezavnostjo", tezavnost)
    print("Stevilo namigov:", gf.count_hints(game))

    start = datetime.datetime.now()

    solution = gf.random_solver(game, 3, 3, limit=30)

    end = datetime.datetime.now() 
    print("Trajanje:", end - start)

    if solution is None: 
        print("Neuspesno")
        neuspesno_reseni.append(end-start)
        tezavnosti_nereseni.append(tezavnost)
    else:
        print("Uspesno")
        times.append(end - start)
        tezavnosti_reseni.append(tezavnost)

    print("\n=============================\n")

total_time_end = datetime.datetime.now() 
slowest = np.argmax(times)
hardest = np.argmax(Tezavnosti)

print("Najtežji sudoku v množici ima težavnost", df_games["difficulty"].max())
print("Povprečna težavnost množice je", df_games["difficulty"].mean())
print("Uspešno smo rešili", len(times), "sudokujev")
print("Neuspešno smo rešili", len(neuspesno_reseni), "sudokujev")
print("Za to smo potrebovali", total_time_end - total_time_start)
print("V povprečju smo potrebovali", sum(times, datetime.timedelta(0)) / len(times))
print("Največ časa smo reševali sudoku s težavnostjo", Tezavnosti[slowest], "in za to potrebovali", times[slowest])
print("Najtežji sudoku ima težavnost", Tezavnosti[hardest], "in za reševanje smo potrebovali", times[hardest])

Df = pd.DataFrame([])
Df["difficulty"] = tezavnosti_reseni
Df["times"] = [t.total_seconds() for t in times]

Df = Df.groupby("difficulty").mean().reset_index()
Df.columns = ["difficulty", "times"]
Df = Df.sort_values(by = "difficulty")

plt.plot(Df["difficulty"], Df["times"])
plt.show()