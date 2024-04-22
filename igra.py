import pandas as pd 
import numpy as np 
import random 
from tabulate import tabulate
import copy

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


def get_game(grid_size, missing_cells):
    grid = None
    while grid is None:
        try:
            grid = gen_grid(grid_size)
        except:
            pass

    game = copy.deepcopy(grid)
    mapping, mapping2 = gen_mapping(grid_size)
    inds = list(mapping.keys())
    inds = random.sample(inds, missing_cells)
    for el in inds: 
        i = int(el[0])
        j = int(el[-1])
        game[i][j] = None
    return np.array(grid), np.array(game)

def plot_game(grid, game):
    # print(tabulate(grid, tablefmt="rounded_grid"))
    print(tabulate(game, tablefmt="rounded_grid"))


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

random.seed(0)

grid, game = get_game(9, 60)
plot_game(grid, game)

def naive_solver(game):
    while True: 
        counter, possibles = count_input_options(game)
        if possibles == {}:
            return True 
        solved = False
        for el in counter.items():
            if el[1] == 1: 
                i = int(el[0][0])
                j = int(el[0][-1])
                vrednost = possibles[el[0]]
                game[i][j] = vrednost[0]
                solved = True
                break 
        if not solved: 
            break
        else:
            return game, solved
    return game, solved

def advanced_solver(game):
    # If possible try naive solver, if it is not working go for advance 
    print(game)
    game, solved = naive_solver(game)
    print("Naive solver finished")
    counter, possibles = count_input_options(game)
    print("Counter:", counter)
    print("Possible:", possibles)
    get_best_index = {}
    if solved:
        print("Game is solved!!!")
        return game
    # Pogledam v katere indekse lahko vpisem neko stevilo moznih cifer 
    for el in counter.keys():
        count = counter[el]
        if count in list(get_best_index.keys()):
            get_best_index[count] = get_best_index[count] + [el]
        else:
            get_best_index[count] = [el]
    mini_count = min(list(get_best_index.keys()))
    for indeks in list(get_best_index[mini_count]):
        values = possibles[indeks]
        for num in values:
            a, b = int(indeks[0]), int(indeks[-1])
            try_solve = copy.deepcopy(game)
            try_solve[a][b] = num
            try_solve = advanced_solver(try_solve)
            if solved:
                plot_game(grid, try_solve)
    return try_solve


advanced_solver(game)



def save_game(game):
    pd.DataFrame(game).to_csv('game.csv', index=False)
    

def read_game():
    game = pd.read_csv('game.csv')
    return game




# Ideja za rankiranje razlicnih sudokujev: 
#   --> Ce je sudoku resen s pomocjo Naive solverja potem je avtomaticno lahek 
#   --> Ce potrebujemo backtracking potem je ali srednji ali pa tezek
#   --> Srednji sudoku je ce imamo backtrack manj kot 5x in nikoli vec kot 2 moznosti
#   --> Tezak sudoku je ce imamo backtrack vec kot 5x ali pa kdaj vec kot 2 moznosti
#   --> Tezava: Enolicnost resevanja --> Ce ima sudoku vec resitev (ni enolicen) je dodatna zahtevnost 
