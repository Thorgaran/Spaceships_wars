#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 
#  
#  

from class_Planet import *
from class_Ship import *

class Univers():
    """
    A Univers is define by
    - a size for the grid (from 0 to x-1 and y-1) -> int
    - some planets -> [class Planet]
    - some ships -> [class Ship]
    - a time -> int

    Methods
    - a destination -> class planet
    - an arrival time -> int
    """
    def __init__(self, size=None, planets=None, ships=None, time=None):
        self.size = size
        self.planets = planets
        self.ships = ships
        self.time = time

    def big_bang(self, size, nb_planets, size_planet_max=3):
        """
        Function to initialize the univers : its planets and the time.
        The number ot planet can't exceed size²/2, otherwise an error is raised.

        nb_planets = nb of planets in the univers
        """
        from random import randint

        if nb_planets > size**2 / 2:
            raise ValueError("Too many planets !")

        # place the planets
        occupied_position = [(None, None)]
        self.planets = []
        for i in range(nb_planets):
            x, y = None, None
            while (x, y) in occupied_position:
                x, y = randint(0, size), randint(0, size)
            size = randint(1, size_planet_max)
            planet = Planet(x, y, size, player=0)
            self.planets.append(planet)
        
        # time initialization
        self.time = 0

# =================================================================================================
if __name__ == "__main__":
    univers = Univers()
    univers.big_bang(size=10, nb_planets=10)