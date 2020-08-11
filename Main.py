#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 
#  Main Function
#  

from class_Fleet import *
from class_Planet import *
from class_Universe import *
from class_Player import *
from class_GUI import *

from json import dumps, loads

# nb max of turns
COUNTER_MAX = 10

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

# creation of the universe
universe = Universe()
universe.big_bang(size=10, nb_planets=10, size_planet_max=3, coef_production=1, coef_max_ships=10, nb_players=2)

# universe.take_off(
#     planet=universe.planets[0],
#     destination=universe.planets[8],
#     nb_ships=universe.planets[0].nb_ships,
#     speed=2)
# display_universe(universe)
# for i in range(10):
#     universe.next_turn()
#     display_universe(universe)

# beginning of the game
counter = 0
while (universe.winner is None) and (counter < COUNTER_MAX):
    counter += 1
    # serialisation of the univers
    list_planets = [
        {
            "x":p.x, "y":p.y,
            "size":p.size,
            "production_per_turn":p.production_per_turn,
            "nb_max_ships":p.nb_max_ships,
            "owner":p.owner.color,
            "nb_ships":p.nb_ships
            }
            for p in universe.planets
    ]
    list_fleets = [
        {
            "starting":f.starting_planet,
            "destination":f.destination_planet,
            "owner":f.owner.color,
            "nb_ships":f.nb_ships
        }
        for f in universe.fleets
    ]
    data = {"planets":list_planets, "fleets":list_fleets}
    data_string = dumps(data)
    # print(data_string)
    
    # get moves player 1 to n
    pass

    # play moves
    pass

# print(f"The winner is {universe.winner.color}")