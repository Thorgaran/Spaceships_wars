#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 
#  
#  

class Planet():
    """
    - x, y = position on the grid (the space) -> int, int
    - size = size of the planet, minimum 1 -> int
    - owner = player owner of the planet -> None/1/2
    - nb_ships = number of ships belonging to the owner -> int
    """
    def __init__(self, x, y, size, owner, nb_ships):
        self.x, self.y = x, y
        self.size = size
        self.owner = owner
        self.nb_ships = nb_ships
    
    def landing(self, fleet):
        """
        A fleet is landing on the planet.
        """
        pass
    
    def take_off(self):
        """
        A fleet is taking off from the planet.
        """
        pass