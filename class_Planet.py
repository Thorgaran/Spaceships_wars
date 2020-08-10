#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 
#  
#  

class Planet():
    """
    A planet is define by
    - a position (x, y) -> (int, int)
    - a size, minimum 1 -> int
    - an owner neutral/player 1/player 2 -> 0/1/2
    """
    def __init__(self, x, y, size, player):
        self.x, self.y = x, y
        self.size = size
        self.player = player