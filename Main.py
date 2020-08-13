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

from AI_dumb import *

from itertools import permutations
from math import factorial
from random import random
from copy import deepcopy

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

# number of games = number of univers
number_of_univers = 1

# if flag_fair is True, each univers will be played with players in each starting position
# Warning : this option multiply the number of game (= number_of_univers) depending of the number of player
#           2 players => x2 ; 3 players => x6 ; 4 players => x24
flag_fair = False

# -------------------------------------------------------------------------------------------------
# creation of the neutral player... which is not a player
player_neutral = Player(ai=None, name="neutral", color=COLOR_PLAYER_LIGHT[0])
# creation of the players
players = [
    # Player(ai=AI_dumb, name="AI_1", color=COLOR_PLAYER_LIGHT[1]),
    # Player(ai=AI_dumb, name="AI_2", color=COLOR_PLAYER_LIGHT[2]),
    Player(ai=AI_dumb, name="AI_3", color=COLOR_PLAYER_LIGHT[3]),
    Player(ai=AI_dumb, name="AI_4", color=COLOR_PLAYER_LIGHT[4])
]

results_glob = {}

for game_number in range(number_of_univers):
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
            players0 = deepcopy(players)
            flag_first = False
            print(f"=== Universe number {game_number} ===")
        else:
            # the universe is already created
            # the position of the players need to be changed
            universe = deepcopy(universe0)
            universe.change_players(list_players)

        timeline = game(universe, nb_max_turn=COUNTER_MAX)  # play the game
        final = timeline[-1]

        result = {"turn":universe.turn}
        if final.winner is not None:
            print(f" The winner is {final.winner.name} (color = {final.winner.color}) at turn number {universe.turn}")
            result["winner"] = final.winner.name
        else:
            print(f" No winner at turn number {universe.turn}!")
            result["winner"] = "No winner!"

        results_glob[(game_number, permutation_counter)] = result
        permutation_counter += 1

        if not flag_fair:  # no need to play on the same universe
            break

# history
if number_of_univers == 1 and not flag_fair:  # i.e. only one simulation
    pickle.dump(timeline, open(HISTORY_FILE, 'wb'))