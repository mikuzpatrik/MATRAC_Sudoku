import datetime
import game_functions as gf
import random 

string = "..3......8.946.7.22...186.......6.7...8...4...7.8.......294...55.6.328.7......2.."

game = gf.read_sudoku(string, 3, 3)

print("Resujemo igro:")
gf.plot_game(game)
print("Stevilo namigov:", gf.count_hints(game))

random.seed(1)
start = datetime.datetime.now()
game, stevilo_ponovitev, globina_drevesa = gf.random_solver(game, 3, 3, with_logic = True)
end = datetime.datetime.now()

print("Bravo, sudoku je uspešno rešen!")
print("Potrebovali smo", (end - start).total_seconds(), "sekund")
print("Random solver je našel rešitev v poskusu številka", stevilo_ponovitev)
print("Globina drevesa je bila", globina_drevesa)
print("Resitev:")
gf.plot_game(game)