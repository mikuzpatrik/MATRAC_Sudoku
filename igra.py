import pandas as pd 
import numpy as np 
import random 
from tabulate import tabulate
import copy
import sys 

def gen_mapping(N):
    n = int(np.sqrt(N))
    indeks_to_obmocje_map = {}
    obmocje_to_indeks_map = {i: [] for i in range(1, N+1)}
    for i in range(N):
        for j in range(N): 
            obmocje = n * (i // n) + j // n + 1 
            key = str(i) + " " + str(j)
            indeks_to_obmocje_map[key] = obmocje
            obmocje_to_indeks_map[obmocje] = obmocje_to_indeks_map[obmocje] + [key]
    return indeks_to_obmocje_map, obmocje_to_indeks_map 

def get_list_of_index(N): 
    lst = []
    for i in range(N):
        for j in range(N): 
            lst.append((i, j))
    random.shuffle(lst)
    return lst

print(get_list_of_index(9))

def gen_grid(grid_size):
    vrstice = [[i for i in range(1, grid_size + 1)] for j in range(grid_size)]
    stolpci = [[] for j in range(grid_size)]
    if int(np.sqrt(grid_size)) == np.sqrt(grid_size): 
        grid = [[None for i in range(grid_size)] for j in range(grid_size)]
        obmocja = [[] for k in range(grid_size)]
        mapping, mapping2 = gen_mapping(grid_size)
        for i in range(grid_size):
            for j in range(grid_size):
                obmocje = mapping[str(i) + " " + str(j)]
                izbire = [el for el in vrstice[i] if el not in stolpci[j] and el not in obmocja[obmocje-1]]
                cifra = random.choice(izbire)
                vrstice[i].remove(cifra)
                grid[i][j] = cifra
                stolpci[j].append(cifra)
                obmocja[obmocje-1].append(cifra)
        return grid
    else:
        print("Trenutno ne podpira te mreze")
        return []

def try_num(game, num, i, j):
    allowed = True
    if game[i][j] is not None:
        allowed = False
    else:
        if num in game[i]:
            allowed = False
        elif num in np.transpose(game)[j]:
            allowed = False
        else:
            mapping, mapping2 = gen_mapping(len(game))
            obmocje = mapping[str(i) + " " + str(j)]
            for el in mapping2[obmocje]:
                if game[int(el[0])][int(el[-1])] == num:
                    allowed = False
    return allowed

def count_input_options(game): 
    N = len(game) 
    counter = {}
    possibles = {}
    for i in range(N):
        for j in range(N):
            if game[i][j] is None:
                counter[str(i) + " " + str(j)] = 0
                possibles[str(i) + " " + str(j)] = []
                for num in range(1, N+1):
                    if try_num(game, num, i, j):
                        counter[str(i) + " " + str(j)] += 1
                        possibles[str(i) + " " + str(j)].append(num)
    return counter, possibles

def check_game(game): 
    N = len(game)
    if any(None in sub for sub in game):
        print("Igra ni koncana!")
        return False 
    else:
        for i in range(N):
            for j in range(N):
                num = game[i][j]
                if game[i].count(num) == 1:
                    vrstica_check = True 
                if np.transpose(game)[j].count(num) == 1:
                    stolpec_check = True 
            mapping, mapping2 = gen_mapping()
            obmocje = mapping[str(i) + " " + str(j)]
            num_count = 0
            for el in mapping2[obmocje]:
                if game[int(el[0])][int(el[-1])] == num:
                    num_count += 1
            if num_count == 1:
                obmocje_check = True 
        if vrstica_check and stolpec_check and obmocje_check:
            print("Igra je pravilno resena")
            return True
        else:
            print("Igra ni pravilno resena")
            return False 

def naive_solver(game):
    try_game = copy.deepcopy(game)
    while True: 
        counter, possibles = count_input_options(try_game)
        if possibles == {}:
            return try_game, True 
        solved = False
        for el in counter.items():
            if el[1] == 1: 
                i = int(el[0][0])
                j = int(el[0][-1])
                vrednost = possibles[el[0]]
                try_game[i][j] = vrednost[0]
                solved = True
                break 
        if not solved: 
            break
    return try_game, solved

def advanced_solver(game, minimax_moznosti = 0, stevilo_odlocitev = 0, solutions = []):
    # If possible try naive solver, if it is not working go for advance 
    game, solved = naive_solver(game)
    counter, possibles = count_input_options(game)
    if 0 in list(counter.values()):
        # print("Izpis")
        return False, False, False, False
    get_best_index = {}
    if solved:
        if solutions == []:
            print("Prva rešitev")
            solutions.append(game)
            return True, game, minimax_moznosti, stevilo_odlocitev
        else:
            print("Že imamo rešitev")
            if game == solutions[0]:
                print("Gre za isto rešitev")
                return True, game, minimax_moznosti, stevilo_odlocitev
            else:
                print("Te rešitve ne sprejmemo")
                print("Sudoku ni enolično rešljiv!")
                return False, None, None, None
    # Pogledam v katere indekse lahko vpisem neko stevilo moznih cifer 
    for el in counter.keys():
        count = counter[el]
        if count in list(get_best_index.keys()):
            get_best_index[count] = get_best_index[count] + [el]
        else:
            get_best_index[count] = [el]
    mini_count = min(list(get_best_index.keys()))
    if mini_count > minimax_moznosti:
        minimax_moznosti = mini_count
    for indeks in list(get_best_index[mini_count]):
        values = possibles[indeks]
        for num in values:
            a, b = int(indeks[0]), int(indeks[-1])
            try_solve = copy.deepcopy(game)
            try_solve[a][b] = num
            solvable, try_solve, moznosti, odlocitve = advanced_solver(try_solve, minimax_moznosti, stevilo_odlocitev+1)
            if not try_solve:
                break
        if not try_solve:
            break
    if len(solutions) == 1 and solvable:
        return True, try_solve, moznosti, odlocitve
    elif not solvable:
        print("Sudoku ni enolično rešljiv")
        print(minimax_moznosti, stevilo_odlocitev)
        return False, None, None, None
    else:
        return False, try_solve, moznosti, odlocitve

def is_game_valid(game, i, j):
    try_game = copy.deepcopy(game)
    try_game[i][j] = None 
    solvable, _, _, _ = advanced_solver(try_game)
    return solvable

def get_game(grid_size):
    grid = None
    while grid is None:
        try:
            grid = gen_grid(grid_size)
        except:
            pass

    game = copy.deepcopy(grid)
    # mapping, _ = gen_mapping(grid_size)
    inds = get_list_of_index(grid_size)
    for n in range(len(inds)):
        print(n, "/ 81") 
        el = inds[n]
        i = int(el[0])
        j = int(el[-1])
        preizkus = is_game_valid(game, i, j)
        print(preizkus)
        if preizkus:
            game[i][j] = None
        else:
            ... 
    return grid, game

grid, game = get_game(9)

def plot_game(game):
    # print(tabulate(grid, tablefmt="rounded_grid"))
    print(tabulate(game, tablefmt="rounded_grid"))
    
print(game)
plot_game(game)

solvable, try_solve, moznosti, odlocitve = advanced_solver(game)

print(solvable, try_solve, moznosti, odlocitve)

def save_game(game):
    pd.DataFrame(game).to_csv('game.csv', index=False)
    

def read_game():
    game = pd.read_csv('game.csv')
    return game


def prepare_and_classify_game(N):
    lst = get_list_of_index(N)
    print(lst)
    grid, game = get_game(9, 35)
    plot_game(grid, game)

# prepare_and_classify_game(9)