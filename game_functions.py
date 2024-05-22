# game_functions contains all the functions used in generate_game and solve_game 

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

def count_input_options(game, m, n, restrictions = []): 
    N = m*n
    counter = {}
    possibles = {}
    for i in range(N):
        for j in range(N):
            if game[i][j] is None:
                counter[str(i) + " " + str(j)] = 0
                possibles[str(i) + " " + str(j)] = []
                for num in range(1, N+1):
                    if str(i) + " " + str(j) + " " + str(num) in restrictions:
                        continue
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
                if cifra in Stolpci[N][i]:
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
                for el in Keys_Obmocja[pos_obmocja_stolpci]:
                    if cifra in possibles[el] and el not in Keys_Stolpci[N]:
                        to_drop.append((el, cifra))
            if pos_obmocja_vrstice != -1 and pos_obmocja_vrstice is not None: 
                for el in Keys_Obmocja[pos_obmocja_vrstice]:
                    if cifra in possibles[el] and el not in Keys_Vrstice[N]:
                        to_drop.append((el, cifra))
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
        counter, possibles, to_drop = boxed_reduction(counter, possibles, m, n)
    counter, possibles, to_drop = pointed_pairs(counter, possibles, m, n)
    counter, possibles, to_drop = boxed_reduction(counter, possibles, m, n)
    return counter, possibles 


def naive_solver(game, m, n):
    try_game = copy.deepcopy(game)
    while True: 
        counter, possibles = count_input_options(try_game, m, n)
        if possibles == {}:
            return try_game, True 
        solved = False
        for el in counter.items():
            if el[1] == 1: 
                ind = el[0].split(" ")
                i, j = int(ind[0]), int(ind[-1])
                vrednost = possibles[el[0]]
                try_game[i][j] = vrednost[0]
                solved = True
                break 
        if not solved: 
            break
    return try_game, solved

def naive_solver_with_logic(game, m, n):
    try_game = copy.deepcopy(game)
    try_game = fill_rows_and_cols(try_game, m, n)
    while True: 
        counter, possibles = count_input_options(try_game, m, n)
        counter, possibles = use_logic(counter, possibles, m, n)
        if possibles == {}:
            return try_game, True 
        solved = False
        for el in counter.items():
            if el[1] == 1: 
                ind = el[0].split(" ")
                i = int(ind[0])
                j = int(ind[-1])
                vrednost = possibles[el[0]]
                try_game[i][j] = vrednost[0]
                solved = True
                break 
        if not solved: 
            break
    return try_game, solved

def get_best_possible_index(game, m, n, counter, possibles): 
    moznosti, indeksi = [], []
    for indeks in list(possibles.keys()):
        for cifra in possibles[indeks]:
            nov_indeks = indeks + " " + str(cifra) 
            try_game = copy.deepcopy(game)
            ind = indeks.split(" ")
            a, b = int(ind[0]), int(ind[-1])
            try_game[a][b] = cifra 
            c, p = count_input_options(try_game, m, n)
            c, p = use_logic(c, p, m, n)
            nove_moznosti = sum(list(c.values()))
            moznosti.append(nove_moznosti)
            indeksi.append(nov_indeks)
    best = np.argmin(moznosti)
    inds = indeksi[best].split(" ")
    sorted_lst = [x for _, x in sorted(zip(moznosti, indeksi))]
    return sorted_lst

# Prva verzija advanced_solverja, kjer gremo od najbolj verjetne celice proti najmanj verjetni
def advanced_solver(game, m, n, minimax_moznosti = 0, stevilo_odlocitev = 0, solutions = [], is_unique = False, prejsnji = None, naive_logic = True, restrictions = []):
    # If possible try naive solver, if it is not working go for advance 
    if prejsnji is None:
        advanced_solver.count = 0
    if naive_logic:
        game, solved = naive_solver_with_logic(game, m, n)
    else:
        game, solved = naive_solver(game, m, n)
    counter, possibles = count_input_options(game, m, n)
    counter, possibles = use_logic(counter, possibles, m, n)
    advanced_solver.count += 1
    if solved:
        kvaliteta = check_sudoku(game, m, n)
        if solutions == [] and kvaliteta:
            solutions.append(game)
            print("Najdena je rešitev!!!")
            return True, game, minimax_moznosti, stevilo_odlocitev, True, advanced_solver.count
        elif kvaliteta:
            if game == solutions[0]:
                return True, game, minimax_moznosti, stevilo_odlocitev, True, advanced_solver.count
            else:
                return False, False, minimax_moznosti, stevilo_odlocitev, False, advanced_solver.count
        else:
            return None, None, minimax_moznosti, stevilo_odlocitev, True, advanced_solver.count
    if is_unique and advanced_solver.count > 200 == 0:
        print("Po", advanced_solver.count, "klicih funkcije, nimamo se resitve")
    if 0 in list(counter.values()) or (advanced_solver.count > 1000 and not is_unique):
        return None, None, minimax_moznosti, stevilo_odlocitev, True, advanced_solver.count
    get_best_index = {}
    # Pogledam v katere indekse lahko vpisem neko stevilo moznih cifer 
    for el in counter.keys():
        count = counter[el]
        if count in list(get_best_index.keys()):
            get_best_index[count] = get_best_index[count] + [el]
        else:
            get_best_index[count] = [el]
    sorted_lst = get_best_possible_index(game, m, n, counter, possibles)
    for indeks in sorted_lst:
        try_solve = copy.deepcopy(game)
        inds = indeks.split(" ")
        a, b, cifra = int(inds[0]), int(inds[1]), int(inds[2])
        try_solve[a][b] = cifra
        solvable, try_solve, moznosti, odlocitve, unique, _ = advanced_solver(try_solve, m, n, minimax_moznosti, stevilo_odlocitev+1, solutions=[], is_unique=is_unique, prejsnji = (a, b))
        if advanced_solver.count > 100 and stevilo_odlocitev != 0:
            print("Alarm?")
            return None, None, None, None, None, None
        elif advanced_solver.count > 100 and stevilo_odlocitev == 0:
            print("Gremo na naslednji indeks!")
        elif not unique:
            return False, None, moznosti, odlocitve, unique, advanced_solver.count
        elif solvable and is_unique:
            return True, try_solve, moznosti, odlocitve, unique, advanced_solver.count
    if solutions != [] and unique:
        return True, solutions[0], moznosti, odlocitve, unique, advanced_solver.count
    else:
        return False, None, moznosti, odlocitve, unique, advanced_solver.count

def advanced_solver_without_logic(game, m, n, minimax_moznosti = 0, stevilo_odlocitev = 0, solutions = [], is_unique = False, prejsnji = None):
    # If possible try naive solver, if it is not working go for advance 
    if prejsnji is None:
        advanced_solver_without_logic.count = 0
    game, solved = naive_solver(game, m, n)
    counter, possibles = count_input_options(game, m, n)
    advanced_solver_without_logic.count += 1
    if is_unique and advanced_solver_without_logic.count % 200 == 0:
        print("Po", advanced_solver_without_logic.count, "klicih funkcije, nimamo se resitve")
    if 0 in list(counter.values()) or (advanced_solver_without_logic.count > 1000 and not is_unique):
        return None, None, minimax_moznosti, stevilo_odlocitev, True, advanced_solver_without_logic.count
    get_best_index = {}
    if solved:
        kvaliteta = check_sudoku(game, m, n)
        if solutions == [] and kvaliteta:
            solutions.append(game)
            return True, game, minimax_moznosti, stevilo_odlocitev, True, advanced_solver_without_logic.count
        elif kvaliteta:
            if game == solutions[0]:
                return True, game, minimax_moznosti, stevilo_odlocitev, True, advanced_solver_without_logic.count
            else:
                return False, False, minimax_moznosti, stevilo_odlocitev, False, advanced_solver_without_logic.count
        else:
            return None, None, minimax_moznosti, stevilo_odlocitev, True
    sorted_lst = get_best_possible_index(game, m, n, counter, possibles)
    for indeks in sorted_lst:
        print(stevilo_odlocitev, indeks)
        try_solve = copy.deepcopy(game)
        inds = indeks.split(" ")
        a, b, cifra = int(inds[0]), int(inds[1]), int(inds[2])
        try_solve[a][b] = cifra
        solvable, try_solve, moznosti, odlocitve, unique, _ = advanced_solver_without_logic(try_solve, m, n, minimax_moznosti, stevilo_odlocitev+1, is_unique=is_unique, prejsnji = (a, b))
        if not unique:
            return False, None, moznosti, odlocitve, unique, advanced_solver_without_logic.count
        if solvable and is_unique:
            return True, try_solve, moznosti, odlocitve, unique, advanced_solver_without_logic.count
    if solutions != [] and unique:
        return True, solutions[0], moznosti, odlocitve, unique, advanced_solver_without_logic.count
    else:
        return False, None, moznosti, odlocitve, unique, advanced_solver_without_logic.count


def random_solver(game, m, n, with_logic = True, limit = None):

    # Najprej z logiko resimo kolikor je le mogoce
    hints_before = 0
    hints_now = count_hints(game)
    while hints_before != hints_now: 
        if with_logic:
            game, solved = naive_solver_with_logic(game, m, n)
        else:
            game, solved = naive_solver(game, m, n)
        hints_before = hints_now 
        hints_now = count_hints(game)

    def random_backtracker(game, m, n, with_logic, solutions = [], is_unique = False):
        # If possible try naive solver, if it is not working go for advance 
        if with_logic:
            game, solved = naive_solver_with_logic(game, m, n)
            counter, possibles = count_input_options(game, m, n)
            counter, possibles = use_logic(counter, possibles, m, n)
        else:
            game, solved = naive_solver(game, m, n)
            counter, possibles = count_input_options(game, m, n)
        random_backtracker.count += 1
        if 0 in list(counter.values()):
            return None, None, None
        if solved:
            kvaliteta = check_sudoku(game, m, n)
            if solutions == [] and kvaliteta:
                solutions.append(game)
                return True, game, True
            elif kvaliteta:
                if game == solutions[0]:
                    return True, game, True
                else:
                    return False, False, False
            else:
                return None, None, True
        # Pogledam v katere indekse lahko vpisem neko stevilo moznih cifer 
        rand_indeks = random.choice(list(possibles.keys()))
        rand_value = random.choice(possibles[rand_indeks])
        try_solve = copy.deepcopy(game)
        rand_ind = rand_indeks.split(" ")
        a, b = int(rand_ind[0]), int(rand_ind[-1])
        try_solve[a][b] = rand_value
        solvable, try_solve, unique = random_backtracker(try_solve, m, n, is_unique=is_unique, with_logic=with_logic)

        if not unique:
            return False, None, unique
        if solvable and is_unique:
            return True, try_solve, unique
        if solutions != [] and unique:
            return True, solutions[0], unique
        else:
            return False, None, unique

    if solved: 
        return game, 0, 0
    else:
        resitev = None
        count_solving = 0
        if limit is None: 
            limit = sys.maxsize
        while resitev is None and count_solving < limit:
            count_solving += 1
            random_backtracker.count = 0
            _, resitev, _ = random_backtracker(game, m, n, with_logic, solutions=[], is_unique=True)
        
        return resitev, count_solving, random_backtracker.count


def is_game_valid(game, m, n, i, j):
    try_game = copy.deepcopy(game)
    try_game[i][j] = None 
    resitev = []
    unique = True
    for i in range(10):
        solution, count_solving, _ = random_solver(try_game, m, n, with_logic=True)
        if resitev == []:
            resitev = solution
        if resitev != solution and resitev != []:
            unique = False 
            break
    return unique, count_solving

def get_game(m, n, max_praznih = None):
    if max_praznih is None: 
        max_praznih = (m*n)**2
    grid = None
    while grid is None:
        try:
            grid = gen_grid(m, n)
        except:
            pass
    print(grid)
    game = copy.deepcopy(grid)
    inds = get_list_of_index(m, n)
    prazne_celice = 0
    for N in range(len(inds)):
        if prazne_celice >= max_praznih:
            break
        el = inds[N]
        i, j = int(el[0]), int(el[-1])
        preizkus, count_solving = is_game_valid(game, m, n, i, j)
        if preizkus:
            game[i][j] = None
            prazne_celice += 1
        else:
            ... 
    if count_solving == 0: 
        unique = True 
    else: 
        unique = False
    return game, grid, unique

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


def rate_game(grid, game, m, n): 
    Depths = [] 
    while len(Depths) != 10: 
        solution, _, globina = random_solver(game, m, n, with_logic = False)
        if solution != grid:
            print("Izgubili smo enoličnost!!!")
            return None
        Depths.append(globina)
    return np.round(sum(Depths) / len(Depths), 1)
    
def plot_game(game):
    print(tabulate(game, tablefmt="rounded_grid"))


def game_to_string(game): 
    string = "" 
    for el in game: 
        for znak in el: 
            if znak is None: 
                string += "."
            else:
                string += str(znak)
    return string 

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
