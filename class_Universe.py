#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 
#  
#  

from class_Planet import *
from class_Fleet import *

class Universe():
    """
    A Universe is defined by
    - a size for the grid (from 0 to x-1 and y-1) -> int
    - some planets -> [class Planet]
    - some fleets -> [class Fleet]
    - a time -> int

    Methods
    - big bang -> object initialization
    """
    def __init__(self, size=None, planets=None, fleets=None, time=None):
        self.size = size
        self.planets = planets
        self.fleets = fleets
        self.time = time

    def big_bang(self, size, nb_planets, size_planet_max=3, coef_production=1, coef_max_ships=10):
        """
        Function to initialize the universe : its planets and the time.
        The number ot planets can't exceed size²/2, otherwise an error is raised.

        size = size of the univers -> int
        nb_planets = nb of planets in the universe. Must be 3, at least -> int
        size_planet_max = size max of the planet -> int
        coef_production = coefficient to increase each turn the number of ships on a planet -> float
        coef_max_ships = coefficient to cap the number of ships on a planet -> float
        """
        from random import randint

        if nb_planets > size**2 / 2:
            raise ValueError("Too many planets!")
        if nb_planets < 3:
            raise ValueError("Not enough planets!")

        # place the neutral planets
        occupied_position = [(0, 0), (size, size)]
        self.planets = []
        for i in range(nb_planets-2):
            x, y = 0, 0
            while (x, y) in occupied_position:
                x, y = randint(0, size), randint(0, size)
            occupied_position.append((x, y))
            planet_size = randint(1, size_planet_max)
            planet = Planet(x, y, size=planet_size, production_per_turn=planet_size/coef_production, nb_max_ships=planet_size*coef_max_ships)
            self.planets.append(planet)

        # and the planets for the players
        planet = Planet(0, 0, size=1, owner=1, nb_ships=1, production_per_turn=planet_size/coef_production, nb_max_ships=1*coef_max_ships)
        self.planets.append(planet)
        planet = Planet(size, size, size=1, owner=2, nb_ships=1, production_per_turn=planet_size/coef_production, nb_max_ships=1*coef_max_ships)
        self.planets.append(planet)
        
        # time initialization
        self.time = 0

    def next_turn(self):
        """
        Prepare the next turn
        """
        for fleet in self.fleets:
            fleet.next_turn()
            if fleet.turns_before_arrival == 0:
                self.landing(fleet, fleet.destination_planet)
        
        for planet in self.planets:
            if planet.owner is not None:
                planet.nb_ships += 1
    
    def landing(self, fleet, planet):
        """
        A fleet is landing on the planet.
        """
        planet.landing_ships(fleet)
        self.fleets.remove(fleet)
    
    def take_off(self, planet, destination, speed):
        """
        A fleet is taking off from the planet, to an other planet (the destination).
        """
        pass


# =================================================================================================
if __name__ == "__main__":
    universe = Universe()
    universe.big_bang(size=10, nb_planets=10)
    universe.fleets = []
    universe.fleets.append(Fleet(1, universe.planets[0], universe.planets[1], 5, 2))
    universe.planets[1].nb_ships = 0
    for i in range(10):
        universe.next_turn()