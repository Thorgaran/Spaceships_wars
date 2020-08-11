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

from AI_dumb import *

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
while (universe.winner is None) and (universe.turn < COUNTER_MAX):
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
    for player in universe.players:
        pass  # TODO
        player_moves = AI_dumb(data_string, player.color)
        # player_moves = loads(test_AI_input)  # for test purpose
        
        if type(player_moves) != list:  # moves are not corrects => next player
            continue

        # play moves
        for move in player_moves:
            # retrieve planets, if they exist
            try:
                starting_planet_pos = move["starting_planet"]
                destination_planet_pos = move["destination_planet"]
            except KeyError:
                continue
            
            try:
                s_planet_pos_x = int(starting_planet_pos["x"])
                s_planet_pos_y = int(starting_planet_pos["y"])
                d_planet_pos_x = int(destination_planet_pos["x"])
                d_planet_pos_y = int(destination_planet_pos["y"])
            except (ValueError, KeyError):
                continue

            starting_planet = destination_planet = None
            for planet in universe.planets:
                if (s_planet_pos_x == planet.x) and (s_planet_pos_y == planet.y):
                    starting_planet = planet
                if (d_planet_pos_x == planet.x) and (d_planet_pos_y == planet.y):
                    destination_planet = planet
            
            if starting_planet is None or destination_planet is None:
                continue
            elif starting_planet is destination_planet:
                continue
            else:
                # check that the starting planet owner is the move emitter
                if starting_planet.owner is not player:
                    continue

                # retrieve the number of ships
                nb_ships = move["nb_ships"]
                if nb_ships > starting_planet.nb_ships:
                    continue

            # the move is only emitted if it's valid
            fleet = Fleet(starting_planet.owner, starting_planet, destination_planet, nb_ships, speed=2)

    # next turn
    universe.next_turn()


# universe.take_off(
#     planet=universe.planets[0],
#     destination=universe.planets[8],
#     nb_ships=universe.planets[0].nb_ships,
#     speed=2)
# display_universe(universe)
# for i in range(10):
#     universe.next_turn()
#     display_universe(universe)

print(f"End at turn {universe.turn}")
if universe.winner is not None:
    print(f"The winner is {universe.winner.color}")
else:
    print("No winner!")