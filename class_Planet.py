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
    - player_neutral = the neutral player, if the planet has no more ship -> class Player

    Optional
    - owner = player owner of the planet -> class Player
    - nb_ships = number of ships belonging to the owner -> int

    Methods
    - take_off_ships
    - landing_ships
    - next_turn
    """
    def __init__(self, x, y, size, production_per_turn, nb_max_ships, player_neutral, owner=None, nb_ships=0):
        self.x, self.y = x, y
        self.owner = player_neutral if owner is None else owner
        self.player_neutral = player_neutral
        self.size = size
        self.production_per_turn = production_per_turn
        self.nb_max_ships = nb_max_ships
        self.nb_ships = nb_ships

    def take_off_ships(self, nb):
        """
        Remove ships from the planet
        """
        self.nb_ships -= nb
        if self.nb_ships < 0:
            raise ValueError("Not enough ships for the take off !")
        if self.nb_ships < 1:
            self.owner = self.player_neutral
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
        if self.owner is not self.player_neutral:
            self.nb_ships += self.production_per_turn
        if self.nb_ships > self.nb_max_ships:
            self.nb_ships = int(self.nb_max_ships)
        return
