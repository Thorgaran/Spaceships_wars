#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 
#  
#  

class Ship():
    """
    A ship is define by
    - a position planet/space -> class planet/0

    A ship may have
    - a destination -> class planet
    - an arrival time -> int
    """
    def __init__(self, position, destination=None, arrival_time=None):
        self.position = position
        self.destination = destination
        self.arrival_time = arrival_time
