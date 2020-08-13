#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 
#  
#  

from class_Planet import *
from class_Fleet import *
from class_Player import *

from random import randint, seed, shuffle
seed("tartiflett")

class Universe():
    """
    Definition of the universe
    - size = size for the square grid (from 0 to size-1) -> int
    - planets = some planets -> set(class Planet)
    - fleets = some fleets -> set(class Fleet)
    - players = list of the players -> [class Player]
    - player_neutral = neutral player present at the beginning of the game -> class Player
    - nb_players = number of players -> int
    - turn = turn number (init = 0) -> int
    - winner = the winner of the game -> None/class Player (property read only)

    Methods
    - big bang = initialization -> /
    - next_turn = incrementation of the turn -> /
    - landing = a fleet is landing on the planet -> /
    - take_off = a fleet is taking off from the planet -> /
    - nb_ships = number of ships owned by a player -> int
    - nb_ships_in_fleets = number of ships owned by a player, in fleets -> int
    - nb_ships_on_planets = number of ships owned by a player, on planets -> int
    - change_players = reattribute the starting planets, using new_list -> /
    """
    def __init__(self, size=None, planets=None, fleets=None, players=None, player_neutral=None, turn=None):
        self.size = size
        self.planets = planets
        self.fleets = fleets
        self.players = players
        self.player_neutral = player_neutral
        self.turn = turn
        self.nb_players = 0 if players is None else len(players)

    def big_bang(self, size, nb_planets, list_players, player_neutral, coef_production, coef_max_ships, size_planet_max=3):
        """
        Function to initialize the universe : its planets and the time.
        The number ot planets can't exceed size²/2, otherwise an error is raised.

        nb_planets = nb of planets in the universe. Must be 5, at least -> int
        size_planet_max = size max of the planet -> int
        list_players = players of the game -> [class Player]

        coef_production = coefficient to increase each turn the number of ships on a planet -> float
        coef_max_ships = coefficient to cap the number of ships on a planet -> float
        """
        if nb_planets > size**2 / 2:
            raise ValueError("Too many planets!")
        if nb_planets < 5:
            raise ValueError("Not enough planets!")

        # players, creation of their starting planets
        self.nb_players = len(list_players)
        self.players = list_players
        self.player_neutral = player_neutral
        self.planets = set()
        occupied_positions = [(0, 0), (size-1, size-1), (0, size-1), (size-1, 0)]  # starting planets
        for i, player in enumerate(list_players):
            planet = Planet(
                *occupied_positions[i],
                size=1,
                player_neutral=player_neutral,
                owner=player,
                nb_ships=1,
                production_per_turn=1*coef_production,
                nb_max_ships=1*coef_max_ships)
            self.planets.add(planet)

       # place the neutral planets and the neutral player
        for i in range(nb_planets-self.nb_players):
            x, y = occupied_positions[0]
            while (x, y) in occupied_positions:
                x, y = randint(0, size-1), randint(0, size-1)
            occupied_positions.append((x, y))
            planet_size = randint(1, size_planet_max)
            planet = Planet(
                x, y,
                size=planet_size,
                player_neutral=self.player_neutral,
                owner=self.player_neutral,
                nb_ships=planet_size,
                production_per_turn=planet_size*coef_production,
                nb_max_ships=planet_size*coef_max_ships)
            self.planets.add(planet)
        
        # fleets initialization
        self.fleets = set()

        # size initialization
        self.size = size

        # turn initialization
        self.turn = 0
        return

    def next_turn(self):
        """
        Prepare the next turn : next turn for each planet and each fleet which is arrived must land
        To determine the landing order of the fleets, the rules are
        1/ the arrival_time parameter determine which land first
        2/ if multiple fleets have the exact same arrival_time parameter, they fight each other in random order
           and the survivor can land
        
        note : the arrival time float is round with 8 decimals (round_factor)
        """
        round_factor = 8

        self.turn += 1
        
        for planet in self.planets:
            planet.next_turn()

        landing_fleet = {}  # will contain {(destination_planet0, arrival_time_0):[fleet_0, fleet_3], (destination_planet1, arrival_time_2):[fleet_1], ...}
        for fleet in self.fleets:
            fleet.next_turn()
            if fleet.turns_before_arrival == 0:
                f_tupple = (fleet.destination_planet, round(fleet.arrival_time, round_factor))
                other = landing_fleet.get(f_tupple, [])
                other.append(fleet)
                landing_fleet[f_tupple] = other

        # shuffle fleets which arrive at the exact same time on the same planet
        for fleets in landing_fleet.values():
            shuffle(fleets)
        # fight between fleets which arrive at the exact same time on the same planet
        landing = []
        for fleets_in_competition in landing_fleet.values():
            self.fleets = self.fleets.difference(fleets_in_competition)  # landing fleets don't exist anymore
            while len(fleets_in_competition) > 1:  # more than one fleet remains => they must fight before landing
                fl0 = fleets_in_competition[0]
                fl1 = fleets_in_competition[1]
                nb = fl0.nb_ships - fl1.nb_ships
                if nb == 0:  # anhilation
                    fleets_in_competition = fleets_in_competition[2:]
                elif nb > 0:  # fl1 has lost
                    fl0.nb_ships = nb
                    del fleets_in_competition[1]
                else:  # fl0 has lost
                    fl1.nb_ships = -nb
                    del fleets_in_competition[0]
            # the remaining fleet can land... if one remains
            if fleets_in_competition:
                self.landing(fleets_in_competition[0])

        return
    
    def landing(self, fleet):
        """
        A fleet is landing on the planet.
        """
        fleet.destination_planet.landing_ships(fleet)
        return
    
    def take_off(self, planet, destination, nb_ships, speed):
        """
        A fleet is taking off from the planet, to another planet (the destination).
        """
        fleet = Fleet(planet.owner, planet, destination, nb_ships, speed, current_turn=self.turn)
        planet.take_off_ships(nb_ships)
        self.fleets.add(fleet)
        return

    def nb_ships(self, player):
        """
        Return the number of ships belonging to the player.
        Ships may be on a planet or in a fleet, travelling to an other planet
        """
        return self.nb_ships_in_fleets(player) + self.nb_ships_on_planets(player)

    def nb_ships_in_fleets(self, player):
        """
        Return the number of ships belonging to the player, in fleets.
        """
        nb = 0
        for f in self.fleets:
            if f.owner is player:
                nb += f.nb_ships
        return nb

    def nb_ships_on_planets(self, player):
        """
        Return the number of ships belonging to the player, on planets.
        """
        nb = 0
        for p in self.planets:
            if p.owner is player:
                nb += p.nb_ships
        return nb

    @property
    def winner(self):
        """
        Return the winner of the game, None if the game is not finished, the neutral player if there are no more ships in game
        """
        
        list_nb_ships = []
        for player in self.players:
            nb = self.nb_ships(player)
            list_nb_ships.append(nb)

        # case draw : no more ship on the map
        if max(list_nb_ships) == 0:
            return self.player_neutral

        # case game not finished : more than one player have ships on the map
        if len([e for e in list_nb_ships if e != 0])  > 1:
            return None

        # case winner : only one player has ship on the map
        for i, nb in enumerate(list_nb_ships):
            if nb > 0:
                return self.players[i]

    def change_players(self, new_list):
        """
        This function reattribute the starting planets, using new_list
        The player new_list[0] will be on the planet of the actual first player, and so on

        new_list = list of players -> [class Players]
        """
        old_list = self.players
        array = list(zip(old_list, new_list))
        dico = {old:new for (old, new) in array}
        for planet in self.planets:
            if planet.owner in dico.keys():
                planet.owner = dico[planet.owner]
        self.players = new_list
        return

# =================================================================================================
if __name__ == "__main__":
    universe = Universe()
    # universe.big_bang(size=10, nb_planets=10)