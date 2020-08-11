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
COUNTER_MAX = 1000

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

test_AI_input = """[
    {
        "starting_planet": {
        "x": 3,
        "y": 7
        },
        "destination_planet": {
        "x": 4,
        "y": 1
        },
        "nb_ships": 12
    },
    {
        "starting_planet": {
        "x": 3,
        "y": 7
        },
        "destination_planet": {
        "x": 2,
        "y": 2
        },
        "nb_ships": 3
    }
]
"""

# beginning of the game
counter = 0
while (universe.winner is None) and (counter < COUNTER_MAX):
    counter += 1
    # serialisation of the univers
    pass
    for player in universe.players:
        # get moves player 1 to n
        pass
        
        # play moves
        player_moves = loads(test_AI_input)
        valid_move = True
        for move in player_moves:
            # retrieve planets, if they exist
            starting_planet_pos = move["starting_planet"]
            destination_planet_pos = move["destination_planet"]
            
            starting_planet = destination_planet = None
            for planet in universe.planets:
                if (starting_planet_pos["x"] == planet.x) and (starting_planet_pos["y"] == planet.y):
                    starting_planet = planet
                if (destination_planet_pos["x"] == planet.x) and (destination_planet_pos["y"] == planet.y):
                    destination_planet = planet
            
            if starting_planet is None or destination_planet is None:
                valid_move = False
            elif starting_planet is destination_planet:
                valid_move = False
            else:
                # check that the starting planet owner is the move emitter
                if starting_planet.owner != player:
                    valid_move = False

            # retrieve the number of ships
            nb_ships = move["nb_ships"]
            if nb_ships > starting_planet.nb_ships:
                valid_move = False

            if valid_move:  # the move is only emitted if it's valid
                fleet = Fleet(starting_planet.owner, starting_planet, destination_planet, nb_ships, speed=2)
            else:
                pass
    pass

universe.take_off(
    planet=universe.planets[0],
    destination=universe.planets[8],
    nb_ships=universe.planets[0].nb_ships,
    speed=2)
display_universe(universe)
for i in range(10):
    universe.next_turn()
    display_universe(universe)

print(f"The winner is {universe.winner.color}")