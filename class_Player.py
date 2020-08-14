#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 
#  
#  

class Player():
    """
    Player of the game.
    - color = color of the player on the screen -> str
    - ai = artificial intelligence of the player -> function
    - name = name of the ai -> str
    - number = a unique id for the player -> int 

    Methods
    - /
    """
    _counter = 0
    def __init__(self, ai, name, color):
        self.color = color
        self.ai = ai
        self.name = name
        self.number = Player._counter
        Player._counter += 1

# =================================================================================================
if __name__ == "__main__":
    for i in range(5):
        p = Player(ai=None, name="bill", color="black")
        print(p.color)