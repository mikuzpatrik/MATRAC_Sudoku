import pandas as pd 
import numpy as np 
import random 
from tabulate import tabulate
import copy

def gen_mapping():
    indeks_to_obmocje_map = {}
    for i in range(9):
        for j in range(9): 
            if i < 3:
                if j < 3:
                    obmocje = 1
                elif j < 6:
                    obmocje = 4
                elif j < 9: 
                    obmocje = 7
            elif i < 6:
                if j < 3:
                    obmocje = 2
                elif j < 6:
                    obmocje = 5
                elif j < 9: 
                    obmocje = 8
            elif i < 9:
                if j < 3:
                    obmocje = 3
                elif j < 6:
                    obmocje = 6
                elif j < 9: 
                    obmocje = 9
            indeks_to_obmocje_map[str(i) + " " + str(j)] = obmocje 
    return indeks_to_obmocje_map 

def gen_mapping_2():
    indeks_to_obmocje_map = {}
    for i in range(4):
        for j in range(4): 
            if i < 2:
                if j < 2:
                    obmocje = 1
                elif j < 4:
                    obmocje = 3
            elif i < 4:
                if j < 2:
                    obmocje = 2
                elif j < 4:
                    obmocje = 4
            indeks_to_obmocje_map[str(i) + " " + str(j)] = obmocje 
    return indeks_to_obmocje_map 

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
        mapping = gen_mapping()
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

    print(np.array(grid))
    game = copy.deepcopy(grid)
    mapping = gen_mapping()
    inds = list(mapping.keys())
    inds = random.sample(inds, missing_cells)
    for el in inds: 
        i = int(el[0])
        j = int(el[-1])
        game[i][j] = None
    return grid, game

def plot_game(grid, game):
    print(tabulate(grid, tablefmt="rounded_grid"))
    print(tabulate(game, tablefmt="rounded_grid"))

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