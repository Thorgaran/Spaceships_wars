#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 
#  
#  

class Player():
    """
    Player of the game.
    The player number 0 is the neutral one : color "gray"
    - color = color of the player on the screen -> str
    - ai = artificial intelligence of the player -> function

    Methods
    - /
    """
    _color_list = ["gray", "blue", "red", "green", "yellow"]
    _counter = 0

    def __init__(self, ai=None):
        # print(f"{Player._counter=}")
        if Player._counter >= len(Player._color_list):
            raise IndexError("Too many players!")
        self.color = self._color_list[Player._counter]
        Player._counter += 1

# =================================================================================================
if __name__ == "__main__":
    for i in range(5):
        p = Player()
        print(p.color)