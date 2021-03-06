#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 
#  
#  

from math import ceil, dist

class Fleet():
    """
    - owner = the player who owns this fleet -> class Player
    - starting_planet = the planet the fleet departed from -> class Planet
    - destination_planet = the planet the fleet is headed to -> class Planet
    - nb_ships = the number of ships composing the fleet -> int
    - total_travel_turns = the total number of turns needed to complete the trip -> int
    - turns_before_arrival = the number of turns left to travel -> int
    - arrival_time = the exact arrival turn -> float

    Methods
    - next_turn
    """
    def __init__(self, owner, starting_planet, destination_planet, nb_ships, speed, current_turn):
        """
        speed = the distance the fleet can cover per turn -> float
        current_turn = the creation's turn of the fleet
        """
        self.owner = owner
        self.starting_planet = starting_planet
        self.destination_planet = destination_planet
        self.nb_ships = nb_ships

        travel_time = self.compute_travel_time(starting_planet, destination_planet, speed)
        self.arrival_time = current_turn + travel_time
        self.total_travel_turns = self.turns_before_arrival = ceil(travel_time)

    @staticmethod
    def compute_travel_time(planet1, planet2, travel_speed):
        """
        Given two planets and a speed, compute the number of turns it takes to travel between them
        
        travel_speed = the distance covered per turn
        """
        return dist((planet1.x, planet1.y), (planet2.x, planet2.y)) / travel_speed

    def next_turn(self):
        """
        Prepare the next turn
        """
        self.turns_before_arrival -= 1
        return