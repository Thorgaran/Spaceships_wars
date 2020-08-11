#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 
#  
#  

class Planet():
    """
    - x, y = position on the grid (the space) -> int, int
    - size = size of the planet, which define the initial number of neutral ships -> int
    - production_per_turn = ship increase per turn -> float
    - nb_max_ships = max ships on the planet -> float

    Optional
    - owner = player owner of the planet -> None/1/2
    - nb_ships = number of ships belonging to the owner -> int

    Methods
    - take_off_ships
    - landing_ships
    - next_turn
    """
    def __init__(self, x, y, size, production_per_turn, nb_max_ships, owner=None, nb_ships=None):
        self.x, self.y = x, y
        self.owner = owner
        self.size = size
        self.production_per_turn = production_per_turn
        self.nb_max_ships = nb_max_ships
        if owner is None:  # neutral planet
            self.nb_ships = size
        else:
            self.nb_ships = nb_ships

    def take_off_ships(self, nb):
        """
        Remove ships from the planet
        """
        self.nb_ships -= nb
        if self.nb_ships < 0:
            raise ValueError("Not enough ships for the take off !")
        if self.nb_ships < 1:
            self.owner = None
            self.nb_ships = 0
        return
    
    def landing_ships(self, fleet):
        """
        Add ships from a fleet to the planet, from the owner of the planet or not
        """
        if fleet.owner == self.owner:
            self.nb_ships += fleet.nb_ships
        else:  # it's an attack
            self.nb_ships -= fleet.nb_ships
            if self.nb_ships > -1 and self.nb_ships < 1:  # fleets annihilation
                self.owner = None
                self.nb_ships = 0
            if self.nb_ships <= -1:  # planet conquered
                self.nb_ships = int(-self.nb_ships) + 1
                self.owner = fleet.owner
        return

    def next_turn(self):
        """
        Prepare the next turn
        """
        if self.owner is not None:
            self.nb_ships += self.production_per_turn
        if self.nb_ships > self.nb_max_ships:
            self.nb_ships = int(self.nb_max_ships)
        return
