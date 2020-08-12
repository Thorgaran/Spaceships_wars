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

    Methods
    - /
    """

    def __init__(self, ai, name, color):
        self.color = color
        self.ai = ai
        self.name = name

# =================================================================================================
if __name__ == "__main__":
    for i in range(5):
        p = Player(ai=None)
        print(p.color)