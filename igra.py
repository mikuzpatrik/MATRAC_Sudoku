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

def fill_rows_and_cols(game):
    # check for rows 
    count, possibles = count_input_options(game)
    for n in range(len(game)):
        values = []
        keys = []
        for el in list(possibles.keys()):
            i, j = int(el[0]), int(el[-1])
            if i == n: 
                values.append(possibles[el])
                keys.append(el)
        opcije = prestej_pojavitve(values)
        for el in opcije:
            stevilo, indeks = el
            i, j = int(keys[indeks][0]), int(keys[indeks][-1])
            game[i][j] = stevilo

    # check for cols
    for n in range(len(game[0])):
        values = []
        keys = []
        for el in list(possibles.keys()):
            i, j = int(el[0]), int(el[-1])
            if j == n: 
                values.append(possibles[el])
                keys.append(el)
        opcije = prestej_pojavitve(values)
        for el in opcije:
            stevilo, indeks = el
            i, j = int(keys[indeks][0]), int(keys[indeks][-1])
            game[i][j] = stevilo

    # check for cells 
    _, map2 = gen_mapping(len(game))
    for n in range(len(game)):
        inds = map2[n+1]
        values = []
        keys = []
        for el in list(possibles.keys()):
            if el in inds:
                values.append(possibles[el])
                keys.append(el)
        opcije = prestej_pojavitve(values)
        for el in opcije:
            stevilo, indeks = el
            i, j = int(keys[indeks][0]), int(keys[indeks][-1])
            game[i][j] = stevilo
        
    return game

def naive_solver(game):
    try_game = copy.deepcopy(game)
    try_game = fill_rows_and_cols(game)
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


def advanced_solver(game, minimax_moznosti = 0, stevilo_odlocitev = 0, solutions = [], is_unique = False):
    # If possible try naive solver, if it is not working go for advance 
    advanced_solver.count += 1
    game, solved = naive_solver(game)
    counter, possibles = count_input_options(game)
    if 0 in list(counter.values()) or advanced_solver.count > 1000:
        print("Slepa ulica, nadaljuj")
        return None, None, minimax_moznosti, stevilo_odlocitev, True
    get_best_index = {}
    if solved:
        if solutions == []:
            print("Prva rešitev")
            solutions.append(game)
            return True, game, minimax_moznosti, stevilo_odlocitev, True
        else:
            print("Že imamo rešitev")
            if game == solutions[0]:
                print("Gre za isto rešitev")
                return True, game, minimax_moznosti, stevilo_odlocitev, True
            else:
                print("Sudoku ni enolično rešljiv!")
                return False, False, minimax_moznosti, stevilo_odlocitev, False
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
            solvable, try_solve, moznosti, odlocitve, unique = advanced_solver(try_solve, minimax_moznosti, stevilo_odlocitev+1, is_unique=is_unique)
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

def is_game_valid(game, i, j):
    try_game = copy.deepcopy(game)
    try_game[i][j] = None 
    advanced_solver.count = 0
    solvable, _, a, b, _ = advanced_solver(try_game, minimax_moznosti=0, stevilo_odlocitev=0, solutions=[])
    print(advanced_solver.count)
    print(solvable)
    return solvable

def get_game(grid_size, max_praznih = np.max):
    grid = None
    while grid is None:
        try:
            grid = gen_grid(grid_size)
        except:
            pass

    game = copy.deepcopy(grid)
    inds = get_list_of_index(grid_size)
    prazne_celice = 0
    for n in range(len(inds)):
        if prazne_celice >= max_praznih:
            break
        print(n, "/ 81") 
        el = inds[n]
        i = int(el[0])
        j = int(el[-1])
        preizkus = is_game_valid(game, i, j)
        if preizkus:
            game[i][j] = None
            prazne_celice += 1
        else:
            ... 
    return game

def count_hints(game):
    count = 0 
    for el in game:
        count += el.count(None)
    count = len(game) * len(game[0]) - count 
    return count

def plot_game(game):
    # print(tabulate(grid, tablefmt="rounded_grid"))
    print(tabulate(game, tablefmt="rounded_grid"))


# string = "..2.3...8.....8....31.2.....6..5.27..1.....5.2.4.6..31....8.6.5.......13..531.4.."
# string = ".......1.4.........2...........5.4.7..8...3....1.9....3..4..2...5.1........8.6..."
# string = ".......1......2..3...4............5..4.16.......71......5....2......8..4..3.91...."
# lst = [[".",".",".",".",".",".",".","1","."],[".",".",".",".",".","2",".",".","3"],[".",".",".","4",".",".",".",".","."],[".",".",".",".",".",".","5",".","."],["4",".","1","6",".",".",".",".","."],[".",".","7","1",".",".",".",".","."],[".","5",".",".",".",".","2",".","."],[".",".",".",".","8",".",".","4","."],[".","3",".","9","1",".",".",".","."]]
# string = "" 
# for vrstica in lst:
#     substring = "" 
#     for el in vrstica:
#         substring += el
#     string += substring
# game = []
# for i in range(9):
#     el = string[9*i:9*(i+1)]
#     vrstica = []
#     for znak in el:
#         if znak == ".":
#             vrstica.append(None)
#         else:
#             vrstica.append(int(znak))
#     game.append(vrstica)

# print("Stevilo namigov:", count_hints(game))
# plot_game(game)


# counter, possibles = count_input_options(game)

# print("Stevilo namigov:", count_hints(game))
# plot_game(game)

# hints_before = 0
# hints_now = count_hints(game)
# while hints_before != hints_now: 
#     game, solvable = naive_solver(game)
#     hints_before = hints_now 
#     hints_now = count_hints(game)
#     print(hints_now)

# solvable, solution, a, b, u = advanced_solver(game, solutions=[], is_unique = True)

# print("Imamo resitev?", solvable)

random.seed(0)

game = get_game(9, 81)
plot_game(game)
print("Stevilo namigov:", count_hints(game))

sys.exit()

solution, solvable = naive_solver(game)

print(solution, solvable)

solvable, solution, a, b, u = advanced_solver(game, solutions=[])

print(solution, solvable, a, b, u)

sys.exit()

def save_game(game):
    pd.DataFrame(game).to_csv('game.csv', index=False)
    

def read_game():
    game = pd.read_csv('game.csv')
    return game


def prepare_and_classify_game(N, number_of_games):
    i = 0
    while i < number_of_games:
        game = get_game(9, 35)
        print("Stevilo namigov:", count_hints(game))
        plot_game(game)
        i += 1
    # Klasifikacija igre 
    # If je igra resljiva samo z enostavnimi namigi --> Lahka 
    # Elif je igra resljiva z opcijami, ki jih je manj kot 3x in ima več kot tretjino namigov --> Srednja 
    # Else Tezka

random.seed(0)

prepare_and_classify_game(9, 10)