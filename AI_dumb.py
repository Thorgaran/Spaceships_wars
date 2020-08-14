#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 
#  Dumb AI
#  

from json import dumps, loads
from class_Planet import *

import random

# -------------------------------------------------------------------------------------------------
def move_creation(planet_f, planet_t, nb_ship):
    """
    Translation of the move in a dictionnary
    - planet_f = departure planet -> class Planet
    - planet_t = arrival planet -> class Planet
    - nb_ship = number of ship -> int
    """
    move = {
        "starting_planet": {
            "x":planet_f.x,
            "y":planet_f.y
        },
        "destination_planet": {
            "x":planet_t.x,
            "y":planet_t.y
        },
        "nb_ships": nb_ship
    }
    return(move)

# -------------------------------------------------------------------------------------------------
def AI_dumb(state, number_AI):
    """
    Take the state of the universe and return some random moves...
    number_AI is the number of the player in the universe.
    """
    universe = loads(state)
    # print(universe)
    list_planets = universe["planets"]
    list_fleets = universe["fleets"]

    # Planets
    planets = []
    for p in list_planets:
        planet = Planet(
            x=p["x"],
            y=p["y"],
            owner=p["owner"],  # warning : it's a number and not a player
            player_neutral=None,
            size=p["size"],
            production_per_turn=p["production_per_turn"],
            nb_max_ships=p["nb_max_ships"],
            nb_ships=p["nb_ships"]
        )
        planets.append(planet)

    # Fleets
    # ... do nothing with this information

    move = []
    # Strategy
    my_planets = [p for p in planets if p.owner == number_AI]
    for p in my_planets:
        nb_ships = p.nb_ships
        list_possible_dest = []
        for dest in planets:
            # print(f"{dest.owner=}")
            if (dest.nb_ships < nb_ships-1) and (dest.owner != number_AI):
                # the planet can be colonized!
                list_possible_dest.append(dest)
        if list_possible_dest:
            final_dest = random.choice(list_possible_dest)
            my_move = move_creation(p, final_dest, nb_ships-1)
            move.append(my_move)
    move_s = dumps(move)
    # print(move_s)
    return(move_s)

# test_AI_input = """[
#     {
#         "starting_planet": {
#         "x": 3,
#         "y": 7
#         },
#         "destination_planet": {
#         "x": 4,
#         "y": 1
#         },
#         "nb_ships": 12
#     },
#     {
#         "starting_planet": {
#         "x": 3,
#         "y": 7
#         },
#         "destination_planet": {
#         "x": 2,
#         "y": 2
#         },
#         "nb_ships": 3
#     }
# ]
# """

# =================================================================================================
if __name__ == "__main__":
    state = """{"planets": [{"x": 0, "y": 0, "size": 1, "production_per_turn": 1, "nb_max_ships": 10, "owner": "blue", "nb_ships": 1}, {"x": 9, "y": 9, "size": 1, "production_per_turn": 1, "nb_max_ships": 10, "owner": "red", "nb_ships": 1}, {"x": 7, "y": 6, "size": 1, "production_per_turn": 1, "nb_max_ships": 10, "owner": "gray", "nb_ships": 10}, {"x": 5, "y": 4, "size": 2, "production_per_turn": 2, "nb_max_ships": 20, "owner": "gray", "nb_ships": 10}, {"x": 8, "y": 3, "size": 3, "production_per_turn": 3, "nb_max_ships": 30, "owner": "gray", "nb_ships": 10}, {"x": 4, "y": 6, "size": 1, "production_per_turn": 1, "nb_max_ships": 10, "owner": "gray", "nb_ships": 10}, {"x": 7, "y": 2, "size": 3, "production_per_turn": 3, "nb_max_ships": 30, "owner": "gray", "nb_ships": 10}, {"x": 6, "y": 7, "size": 1, "production_per_turn": 1, "nb_max_ships": 10, "owner": "gray", "nb_ships": 10}, {"x": 6, "y": 3, "size": 3, "production_per_turn": 3, "nb_max_ships": 30, "owner": "gray", "nb_ships": 10}, {"x": 3, "y": 7, "size": 2, "production_per_turn": 2, "nb_max_ships": 20, "owner": "gray", "nb_ships": 10}], "fleets": []}"""
    AI_dumb(state, color_AI="blue")