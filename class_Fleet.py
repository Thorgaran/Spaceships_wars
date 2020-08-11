#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 
#  
#  

class Fleet():
    """
    - owner = the player who owns this fleet -> None/1/2
    - starting_planet = the planet the fleet departed from -> class Planet
    - destination_planet = the planet the fleet is headed to -> class Planet
    - nb_ships = the number of ships composing the fleet -> int
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
        self.turns_before_arrival = self.compute_travel_time(starting_planet, destination_planet, speed)

    @staticmethod
    def compute_travel_time(planet1, planet2, travel_speed):
        """
        Given two planets and a speed, compute the number of turns it takes to travel between them
        
        travel_speed = the distance covered per turn
        """
        from math import ceil, sqrt

        distance = sqrt((planet1.x - planet2.x)**2 + (planet1.y - planet2.y)**2)
        travel_time = ceil(distance / travel_speed)

        return travel_time

    def next_turn(self):
        """
        Prepare the next turn
        """
        self.turns_before_arrival -= 1
        return