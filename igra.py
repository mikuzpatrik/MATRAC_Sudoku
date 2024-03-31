import pandas as pd 
import numpy as np 
import random 
from tabulate import tabulate
import copy

def gen_mapping():
    indeks_to_obmocje_map = {}
    obmocje_to_indeks_map = {i: [] for i in range(1, 10)}
    for i in range(9):
        for j in range(9): 
            obmocje = 3 * (i // 3) + j // 3 + 1 
            key = str(i) + " " + str(j)
            indeks_to_obmocje_map[key] = obmocje
            obmocje_to_indeks_map[obmocje] = obmocje_to_indeks_map[obmocje] + [key]
    return indeks_to_obmocje_map, obmocje_to_indeks_map 

def gen_grid(grid_size):
    vrstice = [[i for i in range(1, grid_size + 1)] for j in range(grid_size)]
    stolpci = [[] for j in range(grid_size)]
    if grid_size == 3:
        grid = [[None for i in range(grid_size)] for j in range(grid_size)]
        for i in range(grid_size):
            for j in range(grid_size):
                izbire = [el for el in vrstice[i] if el not in stolpci[j]]
                cifra = random.choice(izbire)
                vrstice[i].remove(cifra)
                grid[i][j] = cifra
                stolpci[j].append(cifra)
        return grid 
    elif grid_size == 9: 
        grid = [[None for i in range(grid_size)] for j in range(grid_size)]
        obmocja = [[] for k in range(grid_size)]
        mapping, mapping2 = gen_mapping()
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
    mapping, mapping2 = gen_mapping()
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
            mapping, mapping2 = gen_mapping()
            obmocje = mapping[str(i) + " " + str(j)]
            for el in mapping2[obmocje]:
                if game[int(el[0])][int(el[-1])] == num:
                    allowed = False
    return allowed

def count_input_options(game): 
    counter = {}
    possibles = {}
    for i in range(9):
        for j in range(9):
            if game[i][j] is None:
                counter[str(i) + " " + str(j)] = 0
                possibles[str(i) + " " + str(j)] = []
                for num in range(1, 10):
                    if try_num(game, num, i, j):
                        counter[str(i) + " " + str(j)] += 1
                        possibles[str(i) + " " + str(j)].append(num)
    return counter, possibles

def check_game(game): 
    if any(None in sub for sub in game):
        print("Igra ni koncana!")
        return False 
    else:
        for i in range(9):
            for j in range(9):
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

grid, game = get_game(9, 50)
plot_game(grid, game)

while True: 
    counter, possibles = count_input_options(game)
    print(possibles)
    solved = False
    for el in counter.items():
        if el[1] == 1: 
            i = int(el[0][0])
            j = int(el[0][-1])
            vrednost = possibles[el[0]]
            game[i][j] = vrednost[0]
            solved = True
            break 
    plot_game(grid, game)
    if not solved: 
        break 


# Solver idea: 
    # generiram igro 
    # Pogledam katera polja so None --> Tistim poljem priredim vse mozne vrednosti 
    # Polja katera imajo samo eno mozno vrednost se lahko izpolnijo 
    # Dinamicno ponavljam 
    # Tezava: Igra ni resena & In nobeno polje nima le ene moznosti 
        # Izberem eno moznost in zacnem resevati:
            # Ce resim --> OK 
            # Ce pridem do polja, ki nima moznih odgovorov: Fail --> Neustrezno
        
def solve_game():
    ...