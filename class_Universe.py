#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 
#  
#  

from class_Planet import *
from class_Fleet import *
from class_Player import *

from random import randint, seed
seed("chaussettes")

class Universe():
    """
    Definition of the universe
    - size = size for the square grid (from 0 to size-1) -> int
    - planets = some planets -> [class Planet]
    - fleets = some fleets -> [class Fleet]
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
    - nb_ships = number of ships own by a player -> int

    Each turn is saved in a self._history object with a dictionary for the players and a dictionary for each turn (0, 1...)
        {
            "players":self.players,
            0:{
                "planets":self.planets,
                "fleets":self.fleets
            },
            1:{...},
            ...
        }
    """
    def __init__(self, size=None, planets=None, fleets=None, players=None, player_neutral=None, turn=None):
        self.size = size
        self.planets = planets
        self.fleets = fleets
        self.players = players
        self.player_neutral = player_neutral
        self.turn = turn
        self.nb_players = 0 if players is None else len(players)

    def big_bang(self, size, nb_planets, size_planet_max=3, coef_production=1, coef_max_ships=10, nb_players=2):
        """
        Function to initialize the universe : its planets and the time.
        The number ot planets can't exceed size²/2, otherwise an error is raised.

        nb_planets = nb of planets in the universe. Must be 5, at least -> int
        size_planet_max = size max of the planet -> int
        coef_production = coefficient to increase each turn the number of ships on a planet -> float
        coef_max_ships = coefficient to cap the number of ships on a planet -> float
        """
        if nb_planets > size**2 / 2:
            raise ValueError("Too many planets!")
        if nb_planets < 5:
            raise ValueError("Not enough planets!")

        # creation of the neutral player... which is not a player
        self.player_neutral = Player()

        # creation of the players, and their starting planets
        self.nb_players = nb_players
        self.players = []
        self.planets = []
        occupied_positions = [(0, 0), (size-1, size-1), (0, size-1), (size-1, 0)]  # starting planets
        for i in range(nb_players):
            player = Player()
            self.players.append(player)
            planet = Planet(
                *occupied_positions[i],
                size=1,
                player_neutral=self.player_neutral,
                owner=player,
                nb_ships=1,
                production_per_turn=1*coef_production,
                nb_max_ships=1*coef_max_ships)
            self.planets.append(planet)

       # place the neutral planets and the neutral player
        for i in range(nb_planets-nb_players):
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
            self.planets.append(planet)
        
        # fleets initialization
        self.fleets = []

        # size initialization
        self.size = size

        # turn initialization
        self.turn = 0

        # history initialization
        self._history = {
            "players":self.players,
            self.turn:{
                "planets":self.planets,
                "fleets":self.fleets
            }
        }
        return

    def next_turn(self):
        """
        Prepare the next turn
        """
        self.turn += 1
        
        for planet in self.planets:
            planet.next_turn()

        fleets_to_remove = []
        for fleet in self.fleets:
            fleet.next_turn()
            if fleet.turns_before_arrival == 0:
                self.landing(fleet, fleet.destination_planet)
                fleets_to_remove.append(fleet)
        self.fleets = [f for f in self.fleets if f not in fleets_to_remove]

        # history
        self._history[self.turn] = {
            "planets":self.planets,
            "fleets":self.fleets
        }
        return
    
    def landing(self, fleet, planet):
        """
        A fleet is landing on the planet.
        """
        planet.landing_ships(fleet)
        return
    
    def take_off(self, planet, destination, nb_ships, speed):
        """
        A fleet is taking off from the planet, to another planet (the destination).
        """
        fleet = Fleet(planet.owner, planet, destination, nb_ships, speed)
        planet.take_off_ships(nb_ships)
        self.fleets.append(fleet)
        return

    def nb_ships(self, player):
        """
        Return the number of ships belonging to the player.
        Ships may be on a planet or in a fleet, travelling to an other planet
        """
        nb = 0
        for p in self.planets:
            if p.owner is player:
                nb += p.nb_ships
        for f in self.fleets:
            if f.owner is player:
                nb += f.nb_ships
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

# =================================================================================================
if __name__ == "__main__":
    universe = Universe()
    universe.big_bang(size=10, nb_planets=10)