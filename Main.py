#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 
#  Main Function
#  

from class_Universe import *
from class_Player import *
from class_GUI import *
from game import *
from const import *

from AI import *

from itertools import permutations
from math import factorial
from random import random
from copy import deepcopy
from statistics import mean, median

# -------------------------------------------------------------------------------------------------
def display_universe(universe):
    gui = GUI(universe.size)
    gui.draw_universe(universe)
    gui.display_window()

    """
    occupied_positions = [(planet.x, planet.y) for planet in universe.planets]
    
    # display universe grid
    print("# " * (universe.size + 2))
    for y in range(universe.size):
        line = "# "
        for x in range(universe.size):
            if (x, y) in occupied_positions:
                line += "o "
            else:
                line += "  "
        line += "# "
        print(line)
    print("# " * (universe.size + 2))

    # display planet info
    for planet in universe.planets:
        print(f"({planet.x}, {planet.y}): player {planet.owner.color}, {planet.nb_ships} ships")

    # display fleet info
    for fleet in universe.fleets:
        print(f"({fleet.starting_planet.x}, {fleet.starting_planet.y}) -> ({fleet.destination_planet.x}, {fleet.destination_planet.y}): player {fleet.owner.color}, {fleet.nb_ships} ships, {fleet.turns_before_arrival} turns left")
    """

# -------------------------------------------------------------------------------------------------
def print_results(results, number_universe, flag_fair, players, neutral_player, max_turn):
    """
    Print results with some statistical informations

    results = ... -> {(universe0, perm0):{"turn":int, "winner":None/int}, ...}
    number_universe = number of universe played -> int
    flag_fair = allow multiple play in the same universe -> bool
    players = list of players -> [class Player]
    neutral_player = ... -> class Player
    max_turn = the number max of turn to finish a game -> int
    """
    nb_games = len(results)

    # print parameters
    print("=== Parameters ===")
    print(f"Number of players : {len(players)}")
    for p in players:
        print(f" - player {p.name}")
    print(f'Number of different universes : {number_universe}')
    print(f'Number of games played : {nb_games}')
    print(f'Number of games played per universe : {int(nb_games/number_universe)} ({"" if flag_fair else "no "}fair game : permutation players {"" if flag_fair else "not "}enabled)')
    print(f'Game unfinished if this number of turn is reached : {max_turn}')

    # preparation
    result_player = {}  # {class Player:int, ..., None:int}
    list_turn = []
    nb_unfinished_games = 0
    for r in results.values():
        if r["winner"] is not None:  # the game has a winner
            list_turn.append(r["turn"])
        else:
                nb_unfinished_games += 1
        nb = result_player.get(r["winner"], 0)
        nb += 1
        result_player[r["winner"]] = nb

    # print results
    print()
    print("=== Results ===")
    if nb_unfinished_games == nb_games:
        print("All games are unfinished")
        return
    print("End of games at turn (finished game only)")
    print(f" - mean : {round(mean(list_turn), 1)}")
    print(f" - median : {median(list_turn)}")
    print("Percent of victory (number of victory)")
    for p in players:
        nb_victory = result_player.get(p.number, 0)
        percent = round(nb_victory / nb_games * 100, 1)
        print(f" - player {p.name} : {percent}% ({nb_victory})")
    nb_victory = result_player.get(neutral_player.number, 0)
    percent = round(result_player.get(neutral_player.number, 0) / nb_games * 100, 1)
    print(f"(- draw : {percent}%  ({nb_victory}) )")
    print(f"(- unfinished : {round(nb_unfinished_games/nb_games*100, 1)}% ({nb_unfinished_games}) )")
    return


# -------------------------------------------------------------------------------------------------
# number of games = number of univers
number_of_univers = 50

# if flag_fair is True, each univers will be played with players in each starting position
# Warning : this option multiply the number of game (= number_of_univers) depending of the number of player
#           2 players => x2 ; 3 players => x6 ; 4 players => x24
flag_fair = True

# creation of the neutral player... which is not a player
player_neutral = Player(ai=None, name="neutral", color=COLOR_PLAYER_LIGHT[0])
# creation of the players
players = [
    # Player(ai=AI_dumb, name="AI_1", color=COLOR_PLAYER_LIGHT[1]),
    # Player(ai=AI_dumb, name="AI_2", color=COLOR_PLAYER_LIGHT[2]),
    Player(ai=AI_0, name="AI_0", color=COLOR_PLAYER_LIGHT[3]),
    Player(ai=AI_1, name="AI_1", color=COLOR_PLAYER_LIGHT[4])
]

results_glob = {}  # {(universe0, perm0):{"turn":int, "winner":None/int}, ...}
parameters = {
    "number_universe":number_of_univers,
    "flag_fair":flag_fair,
    "players":players,
    "neutral_player":player_neutral,
    "max_turn":COUNTER_MAX
}

for universe_number in range(number_of_univers):
    flag_first = True
    permutation_counter = 1
    for list_players in permutations(players):  # iteration on the position of the players
        if flag_first:
            # creation of the universe
            universe = Universe()
            universe.big_bang(
                size=10,
                nb_planets=5,
                size_planet_max=3,
                list_players=list_players,
                player_neutral=player_neutral,
                coef_production=COEF_PRODUCTION,
                coef_max_ships=COEF_MAX_SHIP
            )
            universe0 = deepcopy(universe)  # if we need to reuse it
            flag_first = False
            # print(f"=== Universe number {universe_number} ===")
        else:
            # the universe is already created
            # the position of the players need to be changed
            universe = deepcopy(universe0)
            universe.change_players(list_players)

        timeline = game(universe, nb_max_turn=COUNTER_MAX)  # play the game
        final = timeline[-1]

        result = {"turn":universe.turn}
        if final.winner is not None:
            # print(f" The winner is {final.winner.name} (color = {final.winner.color}) at turn number {universe.turn}")
            result["winner"] = final.winner.number
        else:  # game unfinished
            # print(f" No winner at turn number {universe.turn}!")
            result["winner"] = None

        results_glob[(universe_number, permutation_counter)] = result
        permutation_counter += 1

        if not flag_fair:  # no need to play on the same universe
            break

# history
if number_of_univers == 1 and not flag_fair:  # i.e. only one simulation
    pickle.dump(timeline, open(HISTORY_FILE, 'wb'))

# print results
print_results(results_glob, **parameters)