



import os
import game_functions as gf
import datetime 
import pandas as pd
import sys 
import numpy as np 
import matplotlib.pyplot as plt
import random 
random.seed(0)

def group_and_calculate(df, group_by, calculate):

    df_group = df[group_by + calculate].groupby(group_by).agg({calculate[0]: ["mean", "min", "max"]}).reset_index()
    df_group.columns = group_by + ["mean", "min", "max"]
    return df_group

dataset = pd.read_csv("files/sudoku-3m.csv")
dataset["difficulty_int"] = np.round(dataset["difficulty"], 0)
all_tezavnosti = list(dataset["difficulty_int"].drop_duplicates())

print("Najtežji sudoku v datasetu ima težavnost", dataset["difficulty"].max())
print("Povprečna težavnost dataseta je", dataset["difficulty"].mean())

df = pd.read_csv("files/testing_set_results.csv")

print("Povprečna težavnost našega sample seta je:", df[df["seed"] == 0]["difficulty"].mean())
print("\n")

df_group = group_and_calculate(df, ["difficulty_int"], ["time"])
print("Difficulty rounded to integer and time:")
print(df_group)
print("\n")
plt.plot(df_group["difficulty_int"], df_group["mean"])
plt.title("Average solving time")
plt.ylabel("Time in seconds")
plt.xlabel("Difficulty rounded to integer")
plt.savefig("plots/average_solving_time_rounded.png")

df_group = group_and_calculate(df, ["difficulty"], ["time"])
print("Difficulty and time:")
print(df_group)
print("\n")
plt.plot(df_group["difficulty"], df_group["mean"])
plt.title("Average solving time")
plt.ylabel("Time in seconds")
plt.xlabel("Difficulty")
plt.savefig("plots/average_solving_time.png")

df_group = group_and_calculate(df, ["difficulty_int"], ["number_of_try"])
print("Difficulty rounded to integer and number_of_try:")
print(df_group)
print("\n")
plt.plot(df_group["difficulty_int"], df_group["mean"])
plt.title("Average number of solving with random solver")
plt.ylabel("Number of try")
plt.xlabel("Difficulty rounded to integer")
plt.savefig("plots/average_number_of_try.png")

df_group = group_and_calculate(df, ["difficulty_int"], ["depth"])
print("Difficulty rounded to integer and depth:")
print(df_group)
print("\n")
plt.plot(df_group["difficulty_int"], df_group["mean"])
plt.title("Average solving depth")
plt.ylabel("Depth")
plt.xlabel("Difficulty rounded to integer")
plt.savefig("plots/average_depth.png")


df = pd.read_csv("files/random_with_without_logic.csv")
print("\n")
df_group = group_and_calculate(df, ["difficulty_int", "logic"], ["time"])
print("Primerjava časa izračuna random solverja z in brez logike")
print(df_group)

df = pd.read_csv("files/hardest_sudoku_testing.csv")

print("\n")
print("Povprečni čas reševanja najtežjega sudokuja je", df["time"].mean())
print("V povprečju smo za iskanje potrebovali", df["number_of_try"].mean(), "ponovitev")
print("V povprečju je random solver z logiko dosegel globino", df["depth"].mean())

df = pd.read_csv("files/new_games.csv")

print("\n")
df_group = df[["m", "n", "difficulty", "generating time", "rating time"]].groupby(["m", "n"]).mean()
print(df_group)

najtezji_generiran = df["difficulty"].max() 
print("Najtežje generiran sudoku ima tezavnost", najtezji_generiran)
print(df[df["difficulty"] == najtezji_generiran])