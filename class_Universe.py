#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 
#  
#  

from class_Planet import *
from class_MovingFleet import *

class Universe():
    """
    A Universe is defined by
    - a size for the grid (from 0 to x-1 and y-1) -> int
    - some planets -> [class Planet]
    - some moving fleets -> [class MovingFleet]
    - a time -> int

    Methods
    - big bang -> object initialization
    """
    def __init__(self, size=None, planets=None, moving_fleets=None, time=None):
        self.size = size
        self.planets = planets
        self.moving_fleets = moving_fleets
        self.time = time

    def big_bang(self, size, nb_planets, size_planet_max=3):
        """
        Function to initialize the universe : its planets and the time.
        The number ot planets can't exceed size²/2, otherwise an error is raised.

        nb_planets = nb of planets in the universe
        """
        from random import randint

        if nb_planets > size**2 / 2:
            raise ValueError("Too many planets!")

        # place the planets
        occupied_position = [(None, None)]
        self.planets = []
        for i in range(nb_planets):
            x, y = None, None
            while (x, y) in occupied_position:
                x, y = randint(0, size), randint(0, size)
            occupied_position.append((x, y))
            planet_size = randint(1, size_planet_max)
            planet = Planet(x, y, planet_size, owner=0)
            self.planets.append(planet)
        
        # time initialization
        self.time = 0
    
    def landing(self, fleet, planet):
        """
        A fleet is landing on the planet.
        """
        planet.landing_ships(fleet)
    
    def take_off(self, planet, destination, speed):
        """
        A fleet is taking off from the planet, to an other planet (the destination).
        """
        pass


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


# =================================================================================================
if __name__ == "__main__":
    universe = Universe()
    universe.big_bang(size=10, nb_planets=10)
