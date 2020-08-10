#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 
#  
#  

class MovingFleet():
    """
    - self.owner = the player who owns this fleet -> int
    - self.starting_planet = the planet the fleet departed from -> class Planet
    - sef.destination_planet = the planet the fleet is headed to -> class Planet
    - self.nb_of_ships = the number of ships composing the fleet -> int
    - self.turns_before_arrival = the number of turns left to travel -> int
    """
    def __init__(self, owner, starting_planet, destination_planet, nb_of_ships, turns_before_arrival):
        self.owner = owner
        self.starting_planet = starting_planet
        self.destination_planet = destination_planet
        self.nb_of_ships = nb_of_ships
        self.turns_before_arrival = turns_before_arrival
