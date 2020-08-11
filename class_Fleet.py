#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 
#  
#  

from math import ceil, dist

class Fleet():
    """
    - owner = the player who owns this fleet -> None/1/2
    - starting_planet = the planet the fleet departed from -> class Planet
    - destination_planet = the planet the fleet is headed to -> class Planet
    - nb_ships = the number of ships composing the fleet -> int
    - total_travel_turns = the total number of turns needed to complete the trip -> int
    - turns_before_arrival = the number of turns left to travel -> int

    Methods
    - next_turn
    """
    def __init__(self, owner, starting_planet, destination_planet, nb_ships, speed):
        """
        speed = the distance the fleet can cover per turn -> float
        """
        self.owner = owner
        self.starting_planet = starting_planet
        self.destination_planet = destination_planet
        self.nb_ships = nb_ships
        self.total_travel_turns = self.turns_before_arrival = self.compute_travel_time(starting_planet, destination_planet, speed)

    @staticmethod
    def compute_travel_time(planet1, planet2, travel_speed):
        """
        Given two planets and a speed, compute the number of turns it takes to travel between them
        
        travel_speed = the distance covered per turn
        """
        travel_time = ceil(dist((planet1.x, planet1.y), (planet2.x, planet2.y)) / travel_speed)

        return travel_time

    def next_turn(self):
        """
        Prepare the next turn
        """
        self.turns_before_arrival -= 1
        return