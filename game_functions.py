# game_functions contains all the functions used in generate_game and solve_game 


import pandas as pd 
import numpy as np 
import random 
from tabulate import tabulate
import copy
import sys 
import itertools

# strategys https://www.sudokuwiki.org/Intersection_Removal#IR

def gen_mapping(m, n):
    # Imamo bloke m * n
    N = m * n
    indeks_to_obmocje_map = {}
    obmocje_to_indeks_map = {i: [] for i in range(N)}
    for i in range(N):
        for j in range(N): 
            key = str(i) + " " + str(j)
            obmocje = n * (i // n) + j // m 
            indeks_to_obmocje_map[key] = obmocje
            obmocje_to_indeks_map[obmocje] = obmocje_to_indeks_map[obmocje] + [key]
    return indeks_to_obmocje_map, obmocje_to_indeks_map 

def get_list_of_index(m, n): 
    lst = []
    for i in range(m*n):
        for j in range(m*n): 
            lst.append((i, j))
    random.shuffle(lst)
    return lst

def gen_grid(m, n):
    grid_size = m * n
    vrstice = [[i for i in range(1, grid_size+1)] for j in range(grid_size)]
    stolpci = [[] for j in range(grid_size)]

    grid = [[None for i in range(grid_size)] for j in range(grid_size)]
    obmocja = [[] for k in range(grid_size)]
    mapping, mapping2 = gen_mapping(m, n)

    for i in range(grid_size):
        for j in range(grid_size):
            obmocje = mapping[str(i) + " " + str(j)]
            izbire = [el for el in vrstice[i] if el not in stolpci[j] and el not in obmocja[obmocje]]
            cifra = random.choice(izbire)
            vrstice[i].remove(cifra)
            grid[i][j] = cifra
            stolpci[j].append(cifra)
            obmocja[obmocje].append(cifra)
    return grid

def try_num(game, m, n, num, i, j):
    allowed = True
    if game[i][j] is not None:
        allowed = False
    else:
        if num in game[i]:
            allowed = False
        elif num in np.transpose(game)[j]:
            allowed = False
        else:
            mapping, mapping2 = gen_mapping(m, n)
            obmocje = mapping[str(i) + " " + str(j)]
            for el in mapping2[obmocje]:
                if game[int(el[0])][int(el[-1])] == num:
                    allowed = False
    return allowed

def count_input_options(game, m, n): 
    N = m*n
    counter = {}
    possibles = {}
    for i in range(N):
        for j in range(N):
            if game[i][j] is None:
                counter[str(i) + " " + str(j)] = 0
                possibles[str(i) + " " + str(j)] = []
                for num in range(1, N+1):
                    if try_num(game, m, n, num, i, j):
                        counter[str(i) + " " + str(j)] += 1
                        possibles[str(i) + " " + str(j)].append(num)
    return counter, possibles

def prestej_pojavitve(nabor_seznamov):
    stevila = []
    for lst in nabor_seznamov:
        for el in lst:
            if el not in stevila:
                stevila.append(el)
    opcije = []
    for el in stevila:
        pojavitev = 0
        indeks = None 
        for i in range(len(nabor_seznamov)):
            if el in nabor_seznamov[i]:
                pojavitev += 1 
                indeks = i
        if pojavitev == 1:
            opcije.append((el, indeks))
    return opcije 

def check_sudoku(grid, m, n):
    vrstica_ok = True 
    stolpec_ok = True
    obmocje_ok = True 
    _, map2 = gen_mapping(m, n)
    for vrstica in grid:
        if len(vrstica) == len(set(vrstica)):
            vrstica_ok = vrstica_ok and True 
        else:
            vrstica_ok = vrstica_ok and False 
    for stolpec in np.transpose(grid):
        if len(stolpec) == len(set(stolpec)):
            stolpec_ok = stolpec_ok and True 
        else:
            stolpec_ok = stolpec_ok and False 
    for obmocje in range(m*n):
        lst = []
        for el in map2[obmocje]:
            i, j = int(el.split(" ")[0]), int(el.split(" ")[-1])
            lst.append(grid[i][j])
        if len(lst) == len(set(lst)):
            obmocje_ok = obmocje_ok and True 
        else:
            obmocje_ok = obmocje_ok and False 
    return vrstica_ok and stolpec_ok and obmocje_ok 
    

def fill_rows_and_cols(game, m, n):
    # check for rows 
    count, possibles = count_input_options(game, m, n)
    for N in range(len(game)):
        values = []
        keys = []
        for el in list(possibles.keys()):
            el_lst = el.split(" ")
            i, j = int(el_lst[0]), int(el_lst[-1])
            if i == N: 
                values.append(possibles[el])
                keys.append(el)
        opcije = prestej_pojavitve(values)
        for el in opcije:
            stevilo, indeks = el
            key = keys[indeks]
            key_lst = key.split(" ")
            i, j = int(key_lst[0]), int(key_lst[1])
            game[i][j] = stevilo

    # check for cols
    for N in range(m*n):
        values = []
        keys = []
        for el in list(possibles.keys()):
            el_lst = el.split(" ")
            i, j = int(el_lst[0]), int(el_lst[-1])
            if j == N: 
                values.append(possibles[el])
                keys.append(el)
        opcije = prestej_pojavitve(values)
        for el in opcije:
            stevilo, indeks = el
            key = keys[indeks]
            key_lst = key.split(" ")
            i, j = int(key_lst[0]), int(key_lst[-1])
            game[i][j] = stevilo

    # check for cells 
    _, map2 = gen_mapping(m, n)
    for N in range(m*n):
        inds = map2[N]
        values = []
        keys = []
        for el in list(possibles.keys()):
            if el in inds:
                values.append(possibles[el])
                keys.append(el)
        opcije = prestej_pojavitve(values)
        for el in opcije:
            stevilo, indeks = el
            key = keys[indeks]
            key_lst = key.split(" ")
            i, j = int(key_lst[0]), int(key_lst[-1])
            game[i][j] = stevilo
        
    return game

def pointed_pairs(counter, possibles, m, n):
    to_drop = []
    map, map2 = gen_mapping(m, n)
    # Pogledam za vrstice in stolpce (pointed pairs)
    Vrstice, Stolpci, Obmocja, Keys_Vrstice, Keys_Stolpci, Keys_Obmocja = {}, {}, {}, {}, {}, {}
    for N in range(m*n):
        # Pogledam za n-to vrstico/stolpec/obmocje katera polja so prosta in katere vrednosti lahko tja zapisem 
        vrstice = []
        stolpci = []
        obmocja = []
        keys_vrstice = []
        keys_stolpci = []
        keys_obmocja = []
        for el in list(possibles.keys()):
            el_lst = el.split(" ")
            i, j = int(el_lst[0]), int(el_lst[-1])
            if i == N: 
                vrstice.append(possibles[el])
                keys_vrstice.append(el)
            if j == N:
                stolpci.append(possibles[el])
                keys_stolpci.append(el)
            if el in map2[N]:
                obmocja.append(possibles[el])
                keys_obmocja.append(el)
        Vrstice[N] = vrstice
        Stolpci[N] = stolpci
        Obmocja[N] = obmocja
        Keys_Vrstice[N] = keys_vrstice
        Keys_Stolpci[N] = keys_stolpci
        Keys_Obmocja[N] = keys_obmocja


    for N in range(m*n):
        for cifra in range(1, m*n+1):
            pos_obmocje_vrstica, pos_obmocje_stolpec = None, None
            count_vrstica, count_stolpec = 0, 0
            for i in range(len(Obmocja[N])):
                if cifra in Obmocja[N][i]:
                    vrstica = int(Keys_Obmocja[N][i][0])
                    if pos_obmocje_vrstica is None: 
                        pos_obmocje_vrstica = vrstica
                        count_vrstica += 1
                    elif pos_obmocje_vrstica == vrstica: 
                        count_vrstica += 1
                    else:
                        pos_obmocje_vrstica = -1
            
                if cifra in Obmocja[N][i]:
                    stolpec = int(Keys_Obmocja[N][i][-1])
                    if pos_obmocje_stolpec is None: 
                        pos_obmocje_stolpec = stolpec
                        count_stolpec += 1
                    elif pos_obmocje_stolpec == stolpec: 
                        count_stolpec = 1
                    else:
                        pos_obmocje_stolpec = -1
            if pos_obmocje_stolpec != -1 and pos_obmocje_stolpec is not None and count_stolpec >= 1: 
                for el in Keys_Stolpci[pos_obmocje_stolpec]:
                    if cifra in possibles[el] and el not in Keys_Obmocja[N]:
                        to_drop.append((el, cifra))
            if pos_obmocje_vrstica != -1 and pos_obmocje_vrstica is not None and count_vrstica >= 1: 
                for el in Keys_Vrstice[pos_obmocje_vrstica]:
                    if cifra in possibles[el] and el not in Keys_Obmocja[N]:
                        to_drop.append((el, cifra))

    for el, cifra in to_drop:
        if cifra in possibles[el]:
            possibles[el].remove(cifra)

    for el in possibles.keys():
        counter[el] = len(possibles[el])

    return counter, possibles, to_drop

def boxed_reduction(counter, possibles, m, n):

    to_drop = []
    map, map2 = gen_mapping(m, n)
    Vrstice, Stolpci, Obmocja, Keys_Vrstice, Keys_Stolpci, Keys_Obmocja = {}, {}, {}, {}, {}, {}
    for N in range(m * n):
        vrstice = []
        stolpci = []
        obmocja = []
        keys_vrstice = []
        keys_stolpci = []
        keys_obmocja = []
        for el in list(possibles.keys()):
            el_lst = el.split(" ")
            i, j = int(el_lst[0]), int(el_lst[-1])
            if i == N: 
                vrstice.append(possibles[el])
                keys_vrstice.append(el)
            if j == N:
                stolpci.append(possibles[el])
                keys_stolpci.append(el)
            if el in map2[N]:
                obmocja.append(possibles[el])
                keys_obmocja.append(el)
        Vrstice[N] = vrstice
        Stolpci[N] = stolpci
        Obmocja[N] = obmocja
        Keys_Vrstice[N] = keys_vrstice
        Keys_Stolpci[N] = keys_stolpci
        Keys_Obmocja[N] = keys_obmocja

    for N in range(m*n):
        for cifra in range(1, m*n+1): 
            pos_obmocja_stolpci, pos_obmocja_vrstice = None, None 
            for i in range(len(Stolpci[N])):
                key = Keys_Stolpci[N][i]
                obmocje = map[key]
                if pos_obmocja_stolpci is None: 
                    pos_obmocja_stolpci = obmocje 
                elif pos_obmocja_stolpci == obmocje:
                    ...
                else:
                    pos_obmocja_stolpci = -1 
            for i in range(len(Vrstice[N])):
                if cifra in Vrstice[N][i]:
                    key = Keys_Vrstice[N][i]
                    obmocje = map[key]
                    if pos_obmocja_vrstice is None: 
                        pos_obmocja_vrstice = obmocje 
                    elif pos_obmocja_vrstice == obmocje:
                        ...
                    else:
                        pos_obmocja_vrstice = -1  
            if pos_obmocja_stolpci != -1 and pos_obmocja_stolpci is not None: 
                print("V obmocju", pos_obmocja_stolpci, "se pojavi cifra", cifra, "samo v stolpcu", N)
                for el in Keys_Obmocja[pos_obmocja_stolpci]:
                    if cifra in possibles[el] and el not in Keys_Stolpci[N]:
                        to_drop.append((el, cifra))
            if pos_obmocja_vrstice != -1 and pos_obmocja_vrstice is not None: 
                print("V obmocju", pos_obmocja_vrstice, "se pojavi cifra", cifra, "samo v vrstici", N)
                for el in Keys_Obmocja[pos_obmocja_vrstice]:
                    if cifra in possibles[el] and el not in Keys_Vrstice[N]:
                        to_drop.append((el, cifra))
    print("===========")
    print(possibles)
    for el, cifra in to_drop:
        if cifra in possibles[el]:
            possibles[el].remove(cifra)
    for el in possibles.keys():
        counter[el] = len(possibles[el])
    
    return counter, possibles, to_drop

def use_logic(counter, possibles, m, n):
    to_drop = [0]
    while to_drop != []:
        counter, possibles, to_drop = pointed_pairs(counter, possibles, m, n)
        # counter, possibles, to_drop = boxed_reduction(counter, possibles, m, n)
    counter, possibles, to_drop = pointed_pairs(counter, possibles, m, n)
    # counter, possibles, to_drop = boxed_reduction(counter, possibles, m, n)
    return counter, possibles 


def brute_force_solver(game, m, n):
    try_game = copy.deepcopy(game)
    while True: 
        counter, possibles = count_input_options(try_game, m, n)
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

def naive_solver(game, m, n):
    try_game = copy.deepcopy(game)
    try_game = fill_rows_and_cols(try_game, m, n)
    while True: 
        counter, possibles = count_input_options(try_game, m, n)
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


def advanced_solver(game, m, n, minimax_moznosti = 0, stevilo_odlocitev = 0, solutions = [], is_unique = False):
    # If possible try naive solver, if it is not working go for advance 
    if is_unique:
        advanced_solver.count = 0
    game, solved = naive_solver(game, m, n)
    counter, possibles = count_input_options(game, m, n)
    counter, possibles = use_logic(counter, possibles, m, n)
    advanced_solver.count += 1
    if 0 in list(counter.values()) or (advanced_solver.count > 1000 and not is_unique):
        print("Neuspesno!")
        return None, None, minimax_moznosti, stevilo_odlocitev, True
    get_best_index = {}
    if solved:
        kvaliteta = check_sudoku(game, m, n)
        if solutions == [] and kvaliteta:
            solutions.append(game)
            return True, game, minimax_moznosti, stevilo_odlocitev, True
        elif kvaliteta:
            if game == solutions[0]:
                return True, game, minimax_moznosti, stevilo_odlocitev, True
            else:
                return False, False, minimax_moznosti, stevilo_odlocitev, False
        else:
            return None, None, minimax_moznosti, stevilo_odlocitev, True
    # Pogledam v katere indekse lahko vpisem neko stevilo moznih cifer 
    for el in counter.keys():
        count = counter[el]
        if count in list(get_best_index.keys()):
            get_best_index[count] = get_best_index[count] + [el]
        else:
            get_best_index[count] = [el]
    mini_count = min(list(get_best_index.keys()))
    try_solve = None
    if mini_count > minimax_moznosti:
        minimax_moznosti = mini_count
    for indeks in list(get_best_index[mini_count]):
        try_solve = copy.deepcopy(game)
        a, b = int(indeks[0]), int(indeks[-1])
    # for indeks in list(possibles.keys()):
        values = possibles[indeks]
        for num in values:
            a, b = int(indeks[0]), int(indeks[-1])
            if try_solve is None:
                try_solve = copy.deepcopy(game)
            try_solve[a][b] = num
            solvable, try_solve, moznosti, odlocitve, unique = advanced_solver(try_solve, m, n, minimax_moznosti, stevilo_odlocitev+1, is_unique=is_unique)
            if not unique:
                return False, None, moznosti, odlocitve, unique
            if solvable and is_unique:
                return True, try_solve, moznosti, odlocitve, unique
        # if not unique:
        #     break
        # if solutions != [] and is_unique:
        #     break
    if solutions != [] and unique:
        return True, solutions[0], moznosti, odlocitve, unique
    else:
        return False, None, moznosti, odlocitve, unique


def is_game_valid(game, m, n, i, j):
    try_game = copy.deepcopy(game)
    try_game[i][j] = None 
    advanced_solver.count = 0
    solvable, _, a, b, _ = advanced_solver(try_game, m, n, minimax_moznosti=0, stevilo_odlocitev=0, solutions=[])
    return solvable

def get_game(m, n, max_praznih = None):
    if max_praznih is None: 
        max_praznih = (m*n)**2
    grid = None
    while grid is None:
        try:
            grid = gen_grid(m, n)
        except:
            pass

    game = copy.deepcopy(grid)
    inds = get_list_of_index(m, n)
    prazne_celice = 0
    for N in range(len(inds)):
        if prazne_celice >= max_praznih:
            break
        el = inds[N]
        i, j = int(el[0]), int(el[-1])
        preizkus = is_game_valid(game, m, n, i, j)
        if preizkus:
            game[i][j] = None
            prazne_celice += 1
        else:
            ... 
    return game, grid

def count_hints(game):
    count = 0 
    for el in game:
        count += el.count(None)
    count = len(game) * len(game[0]) - count 
    return count

def game_to_string(game):
    string = ""
    for vrstica in game: 
        for znak in vrstica:
            if znak is None:
                string += "."
            else:
                string += str(znak)
    return string


def rate_game(grid, game, m, n, minimax_moznosti = 0, stevilo_odlocitev = 0): 
    game, _ = brute_force_solver(game, m, n)
    counter, possibles = count_input_options(game, m, n)
    if 0 in list(counter.values()):
        return None, minimax_moznosti, stevilo_odlocitev, False
    elif counter == {}:
        return game, minimax_moznosti, stevilo_odlocitev, True
    get_best_index = {}
    for el in counter.keys():
        count = counter[el]
        if count in list(get_best_index.keys()):
            get_best_index[count] = get_best_index[count] + [el]
        else:
            get_best_index[count] = [el]
    mini_count = min(list(get_best_index.keys()))
    try_solve = None
    if mini_count > minimax_moznosti:
        minimax_moznosti = mini_count
    try_solve = copy.deepcopy(game)
    current_odlocitve = 100
    for indeks in list(get_best_index[mini_count]):
        try_solve = copy.deepcopy(game)
        a, b = int(indeks[0]), int(indeks[-1])
        try_solve[a][b] = grid[a][b]
        try_solve, minimax_moznosti, stevilo_odlocitev_final, solved = rate_game(grid, try_solve, m, n, minimax_moznosti, stevilo_odlocitev+1)
        if solved:
            if stevilo_odlocitev_final < current_odlocitve: 
                current_odlocitve = stevilo_odlocitev_final
            return try_solve, minimax_moznosti, stevilo_odlocitev_final, True 
    return try_solve, minimax_moznosti, current_odlocitve, False

def get_rating(grid, game, m, n):
    _, minimax, globina, _ = rate_game(grid, game, m, n)
    stevilo_namigov = count_hints(game)
    stevilo_praznih = len(game) * len(game[0]) - stevilo_namigov
    if minimax < 1: 
        return "Easy", stevilo_praznih
    elif minimax == 2 and globina <= 5: 
        return "Medium", 100 * (globina) + stevilo_praznih
    elif minimax == 2 and globina <= 10: 
        return "Hard", 100 * (globina) + stevilo_praznih
    else: 
        return "Very hard", 1000 * (minimax - 2) + 100 * (globina) + stevilo_praznih