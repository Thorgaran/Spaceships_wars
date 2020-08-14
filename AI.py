#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 
# AI
# The AI take the state of the universe and return some fleet's moves
#
# The state of the universe is a JSON string, which structure is :
# {"planets": [
#   {
#      "x": int,
#      "y": int,
#      "size": int,
#      "production_per_turn": float,
#      "nb_max_ships": int,
#      "owner": int, <= this is the identification number of the player (player.number)
#      "nb_ships": int
#   },
#   ...
# ],
# "fleets": [
#   {
#       "starting_x": int,
#       "starting_y": int,
#       "destination_x": int,
#       "destination_y": int,
#       "owner": int, <= this is the identification number of the player (player.number)
#       "nb_ships": int
#   },
# ...
# ],
# "parameters":
#   {
#       "nb_max_turn": int,
#       "speed": float,
#       "player_nb": int,
#       "turn": int
#   }
# }


from json import dumps, loads
from class_Planet import *
from class_Fleet import *

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
def read_state_universe(universe):
    """
    Read the universe, after the loads instruction
    """
    list_planets = universe["planets"]
    list_fleets = universe["fleets"]

    # parameters
    parameters = universe["parameters"]
    turn = parameters["turn"]
    speed = parameters["speed"]

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
    fleets = []
    for f in list_fleets:
        # search for the starting planet
        f_x, f_y = f["starting_x"], f["starting_y"]
        f_planet_from = None
        for p in planets:
            if (p.x, p.y) == (f_x, f_y):
                f_planet_from = p
        if f_planet_from is None:  # problem
            return (None, None, None)
        # search for the destination planet
        f_x, f_y = f["destination_x"], f["destination_y"]
        f_planet_to = None
        for p in planets:
            if (p.x, p.y) == (f_x, f_y):
                f_planet_to = p
        if f_planet_to is None:  # problem
            return (None, None, None)

        fleet = Fleet(
            owner=f["owner"],  # warning : it's a number and not a player
            starting_planet=f_planet_from,
            destination_planet=f_planet_to,
            nb_ships=f["nb_ships"],
            speed=speed,
            current_turn=turn
        )
        fleets.append(fleet)
    return (parameters, planets, fleets)

# -------------------------------------------------------------------------------------------------
def AI_0(state):
    """
    Strategy : do nothing...
    """ 
    return dumps([])

# -------------------------------------------------------------------------------------------------
def AI_1(state):
    """
    Strategy :
    - for each of its planets p0, search an other planet
      * belonging to an other planet p, or neutral
      * with p0.nb_ship - 1 > p.nb_ship
    - if so, a fleet with (p0.nb_ship - 1) ships is send from p0 to p
    """
    universe = loads(state)
    parameters, planets, fleets = read_state_universe(universe)
    if parameters is None:  # there is a problem => no move
        return dumps([])

    number_AI = parameters["player_nb"]

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

# -------------------------------------------------------------------------------------------------
def AI_2(state):
    """
    Strategy :
    - for each of its planets p0, search an other planet
      * belonging to an other planet p, or neutral
      * with p0.nb_ship - 1 > p.nb_ship
      * with no fleet already in a journey to this planet <= difference with AI_1
    - if so, a fleet with (p0.nb_ship - 1) ships is send from p0 to p
    """
    universe = loads(state)
    parameters, planets, fleets = read_state_universe(universe)
    if parameters is None:  # there is a problem => no move
        return dumps([])

    turn = parameters["turn"]
    speed = parameters["speed"]
    number_AI = parameters["player_nb"]
    nb_max_turn = parameters["nb_max_turn"]

    move = []
    # Strategy
    my_planets = [p for p in planets if p.owner == number_AI]
    my_fleet_destination = set(f.destination_planet for f in fleets if f.owner == number_AI)
    for p in my_planets:
        nb_ships = p.nb_ships
        list_possible_dest = []
        for dest in planets:
            # print(f"{dest.owner=}")
            if (dest.nb_ships < nb_ships-1) and (dest.owner != number_AI) and (dest not in my_fleet_destination):  # <= difference with AI_1
                # the planet can be colonized!
                list_possible_dest.append(dest)
        if list_possible_dest:
            final_dest = random.choice(list_possible_dest)
            my_move = move_creation(p, final_dest, nb_ships-1)
            move.append(my_move)
    move_s = dumps(move)
    # print(move_s)
    return(move_s)

# =================================================================================================
if __name__ == "__main__":
    state = """{"planets": [{"x": 0, "y": 0, "size": 1, "production_per_turn": 1, "nb_max_ships": 10, "owner": "blue", "nb_ships": 1}, {"x": 9, "y": 9, "size": 1, "production_per_turn": 1, "nb_max_ships": 10, "owner": "red", "nb_ships": 1}, {"x": 7, "y": 6, "size": 1, "production_per_turn": 1, "nb_max_ships": 10, "owner": "gray", "nb_ships": 10}, {"x": 5, "y": 4, "size": 2, "production_per_turn": 2, "nb_max_ships": 20, "owner": "gray", "nb_ships": 10}, {"x": 8, "y": 3, "size": 3, "production_per_turn": 3, "nb_max_ships": 30, "owner": "gray", "nb_ships": 10}, {"x": 4, "y": 6, "size": 1, "production_per_turn": 1, "nb_max_ships": 10, "owner": "gray", "nb_ships": 10}, {"x": 7, "y": 2, "size": 3, "production_per_turn": 3, "nb_max_ships": 30, "owner": "gray", "nb_ships": 10}, {"x": 6, "y": 7, "size": 1, "production_per_turn": 1, "nb_max_ships": 10, "owner": "gray", "nb_ships": 10}, {"x": 6, "y": 3, "size": 3, "production_per_turn": 3, "nb_max_ships": 30, "owner": "gray", "nb_ships": 10}, {"x": 3, "y": 7, "size": 2, "production_per_turn": 2, "nb_max_ships": 20, "owner": "gray", "nb_ships": 10}], "fleets": []}"""
    # AI_dumb(state, number_AI="blue")

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