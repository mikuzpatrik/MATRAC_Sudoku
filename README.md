Projekt pri predmetu Matematika z računalnikom na magisterskem študiju FMF. 

Naloga je izdelati program za reševanje in generiranje sudokujev. 

Reporzitorij vsebuje skripte game_functions.py, generate_csv.py, analyse_results.csv in sudoku_demo.py. V skripti game_functions se nahajo pomožne funkcije, ki se uporabljajo v preostalih dveh skriptah. Skripta generate_csv.py generira 4 csv-je z rezultati testiranja, ki se nahajo v mapi files. 

Prvi csv se imenuje testing_set_results.csv in vsebuje čas reševanja posamezne igre pri različnih random.seed.
Csv random_with_without_logic.csv je primerjava med dvema solverjema in sicer random z in random brez logike v ozadju. 
Hardest_sudoku_testing.csv so rezultati testiranja solverja na domnevno najtežjemu sudokuju na svetu. 
New_games.csv vsebuje novo generirane igre, s pomočjo generatorja iger. 

Za testiranje, kot sem ga izvedel, je potrebno prenesti zip datoteko s spletne strani https://www.kaggle.com/datasets/radcliffe/3-million-sudoku-puzzles-with-rating, saj je sam file prevelik, da bi ga naložil na git. 

Tretja skripta, predstavlja analizo rezultatov. 

Skripta sudoku_demo.py predstavlja primer reseavnja za dotični sudoku, ki ga uporabnik sam vnese.
