#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 
#  Main Function
#  

from class_Fleet import *
from class_Planet import *
from class_Universe import *

# creation of the universe
universe = Universe()
universe.big_bang(size=10, nb_planets=20, size_planet_max=10)

# setup for the players
