#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 
#  
#  

# from class_Fleet import *
# from class_Planet import *
# from class_Universe import *
# from class_Player import *

# from AI_dumb import *

import os
from json import dumps, loads
from subprocess import check_output, TimeoutExpired
import pickle
import copy
from inspect import isfunction

# -------------------------------------------------------------------------------------------------
def get_ai_moves(data_string):
    """
    Calls an AI program, gives it the current turn data, and retrieve a list of moves
    """
    # create a pipe to a child process 
    data, temp = os.pipe()
    # write to STDIN as a byte object(convert string 
    # to bytes with encoding utf8) 
    os.write(temp, bytes(data_string, "utf-8"))
    os.close(temp)

    try:
        # store output of the program as a byte string in s
        ai_output = check_output("py draft/fake_AI.py", stdin=data, shell=True, timeout=1)
    except TimeoutExpired:
        return ""
    
    moves = ai_output.decode("utf-8")
    return moves

# -------------------------------------------------------------------------------------------------
def game(universe, nb_max_turn):
    """
    Play a game
    universe = initial position of the game -> class Universe
    nb_max_turn = nb max of turns for a game -> int

    Return the timeline which contain the univers, for each turn -> [class Universe]
    """
    # timeline
    timeline = [copy.deepcopy(universe)]

    # beginning of the game
    while (universe.winner is None) and (universe.turn < nb_max_turn):
        # serialisation of the univers
        # display_universe(universe)
        list_planets = [
            {
                "x":p.x, "y":p.y,
                "size":p.size,
                "production_per_turn":p.production_per_turn,
                "nb_max_ships":p.nb_max_ships,
                "owner":p.owner.number,
                "nb_ships":p.nb_ships
                }
                for p in universe.planets
        ]
        list_fleets = [
            {
                "starting_x":f.starting_planet.x,
                "starting_y":f.starting_planet.y,
                "destination_x":f.destination_planet.x,
                "destination_y":f.destination_planet.y,
                "owner":f.owner.number,
                "nb_ships":f.nb_ships
            }
            for f in universe.fleets
        ]
        data = {"planets":list_planets, "fleets":list_fleets}
        data_string = dumps(data)
        # print(data_string)

        # get moves player 1 to n
        for player in universe.players:
            if isfunction(player.ai):  # function in Python
                ai_output = player.ai(data_string, player.number)
            elif type(player.ai) is str:  # other program
                pass  # TODO
            else:
                raise ValueError("Some AI are incorrect")
            # player_moves = loads(test_AI_input)  # for test purpose
            # ai_output = get_ai_moves(data_string)
            
            # if universe.turn > 11:
            #     a=1
            #     pass

            player_moves = loads(ai_output)
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
                universe.take_off(starting_planet, destination_planet, nb_ships, speed=2)

        # next turn
        universe.next_turn()
        timeline.append(copy.deepcopy(universe))
    
    return timeline