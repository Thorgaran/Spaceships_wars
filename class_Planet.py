#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 
#  
#  

class Planet():
    """
    - x, y = position on the grid (the space) -> int, int
    - size = size of the planet, which define the number of neutral ships -> int

    Optional
    - owner = player owner of the planet -> None/1/2
    - nb_ships = number of ships belonging to the owner -> int
    """
    def __init__(self, x, y, size, owner=None, nb_ships=None):
        self.x, self.y = x, y
        self.owner = owner
        if owner is None:  # neutral planet
            self.nb_ships = size
        else:
            self.nb_ships = nb_ships

    def take_off_ships(self, nb):
        """
        Remove ships from the planet
        """
        self.nb_ships -= nb
        if self.nb_ships == 0:
            self.owner = None
        elif self.nb_ships < 0:
            raise ValueError("Not enough ships for the take off !")
        return
    
    def landing_ships(self, nb, ships_owner):
        """
        Add ships to the planet, from the owner of the planet or not
        """
        if ships_owner == self.owner:
            self.nb_ships += nb
        else:  # it's an attack
            self.nb_ships -= nb
            if self.nb_ships == 0:  # not conquered
                self.owner = None
            elif self.nb_ships < 0:  # planet conquered
                self.nb_ships = -self.nb_ships
                self.owner = ships_owner
            else:
                pass  # no change...