#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Constants definition
#  
#  

# for the game ------------------------------------------------------------------------------------
# nb max of turns for a game -> int
COUNTER_MAX = 100
# coefficient to increase each turn the number of ships on a planet -> float
COEF_PRODUCTION = 1
# coefficient to cap the number of ships on a planet -> float
COEF_MAX_SHIP = 20

# other consts ------------------------------------------------------------------------------------
# name of the file used to store the game's history on disk -> str
HISTORY_FILE = "history_save"

# color of the player
COLOR_PLAYER_LIGHT = {
    0:"gray",
    1:"deep sky blue",
    2:"red",
    3:"green2",
    4:"gold"
}
COLOR_PLAYER_DARK = {
    0:"gray",
    1:"blue3",
    2:"red3",
    3:"green3",
    4:"gold3"
}