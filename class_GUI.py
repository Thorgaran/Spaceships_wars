import tkinter as tk
from math import dist

from class_Fleet import *
from class_Planet import *
from class_Universe import *
from class_Player import *

# -------------------------------------------------------------------------------------------------
def _create_circle(self, x, y, r, **kwargs):
    """
    Adds a create_circle method to the Canvas object, more convenient than the create_oval one
    """
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

# convert from Universe coordinates to Canvas coordinates
conv = lambda x: (x+1)*80

# -------------------------------------------------------------------------------------------------
class GUI():
    """
    Graphical User Interface
    - root = the main GUI window -> class Tk
    - canvas = the canvas inside the root -> class Canvas

    Methods
    - /
    """

    def __init__(self, universe_size):
        """
        universe_size: the size of the universe, used to create the canvas
        """
        self.root = tk.Tk()
        self.root.title("Spaceship_wars_GUI")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, height=conv(universe_size), width=conv(universe_size), background="white")
        self.canvas.grid()

    def clear_canvas(self):
        self.canvas.delete("all")
        return

    def display_window(self):
        self.root.mainloop()
        return

    def draw_universe(self, universe):
        """
        Draws all the planets and fleets in a given universe
        """
        for planet in universe.planets:
            self.draw_planet(planet)

        for fleet in universe.fleets:
            self.draw_fleet(fleet)
        return

    def draw_planet(self, planet):
        """
        Draws a planet of variable size, number of ships and owner
        """
        self.canvas.create_circle(conv(planet.x), conv(planet.y), (planet.production_per_turn+3)*4, fill=planet.owner.color)
        self.canvas.create_text(conv(planet.x), conv(planet.y), text=str(planet.nb_ships), fill='white')
        return

    def draw_fleet(self, fleet):
        """
        Draws a fleet with a trajectory and a number of ships
        """
        # draw the trajectory
        self.canvas.create_line(conv(fleet.starting_planet.x), conv(fleet.starting_planet.y),
            conv(fleet.destination_planet.x), conv(fleet.destination_planet.y),
            fill=fleet.owner.color)
        
        # draw the fleet itself
        compute_pos = lambda x1,x2: conv(x2) + (((conv(x1) - conv(x2))/(fleet.total_travel_turns+1))*fleet.turns_before_arrival)
        fleet_pos_x = compute_pos(fleet.starting_planet.x, fleet.destination_planet.x)
        fleet_pos_y = compute_pos(fleet.starting_planet.y, fleet.destination_planet.y)
        
        self.canvas.create_circle(fleet_pos_x, fleet_pos_y, 5, fill=fleet.owner.color)
        
        distance_left = dist((fleet_pos_x, fleet_pos_y), (conv(fleet.destination_planet.x), conv(fleet.destination_planet.y)))
        ratio = 20/distance_left
        self.canvas.create_line(fleet_pos_x, fleet_pos_y,
            fleet_pos_x + ((conv(fleet.destination_planet.x) - fleet_pos_x) * ratio),
            fleet_pos_y + ((conv(fleet.destination_planet.y) - fleet_pos_y) * ratio),
            arrow='last', width=4, fill=fleet.owner.color)
        
        # draw the number of ships
        self.canvas.create_text(fleet_pos_x, fleet_pos_y-20, text=str(fleet.nb_ships), fill=fleet.owner.color)
        return

"""
player_neutral = Player()
player1 = Player()
player2 = Player()

planet1 = Planet(x=1, y=2, size=10, production_per_turn=2, nb_max_ships=20, player_neutral=player_neutral, owner=player1, nb_ships=6)
draw_planet(canvas, planet1)

planet2 = Planet(x=9, y=9, size=10, production_per_turn=1, nb_max_ships=20, player_neutral=player_neutral, owner=player2, nb_ships=6)
draw_planet(canvas, planet2)

planet3 = Planet(x=3, y=5, size=10, production_per_turn=3, nb_max_ships=20, player_neutral=player_neutral, owner=player_neutral, nb_ships=15)
draw_planet(canvas, planet3)

planet4 = Planet(x=3, y=4, size=10, production_per_turn=3, nb_max_ships=20, player_neutral=player_neutral, owner=player1, nb_ships=15)
draw_planet(canvas, planet4)

fleet1 = Fleet(planet4.owner, planet4, planet2, 10, 2)
draw_fleet(canvas, fleet1)

fleet2 = Fleet(planet2.owner, planet2, planet1, 7, 2)
fleet2.turns_before_arrival -= 5
draw_fleet(canvas, fleet2)
"""