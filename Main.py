#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 
#  Main Function
#  

from class_Universe import *
from class_Player import *
from game import *

from AI_dumb import *

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
# creation of the neutral player... which is not a player
player_neutral = Player(ai=None)
# creation of the players
players = [
    Player(ai=AI_dumb),
    Player(ai=AI_dumb)
]

# creation of the universe
universe = Universe()
universe.big_bang(
    size=10,
    nb_planets=10,
    size_planet_max=3,
    list_players=players,
    player_neutral=player_neutral,
    coef_production=COEF_PRODUCTION,
    coef_max_ships=COEF_MAX_SHIP
)

timeline = game(universe, nb_max_turn=COUNTER_MAX)  # play the game
final = timeline[-1]

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
if final.winner is not None:
    print(f"The winner is {final.winner.color}")
else:
    print("No winner!")

# history
pickle.dump(timeline, open(HISTORY_FILE, 'wb'))