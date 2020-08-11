import tkinter as tk
from math import dist

from class_Fleet import *
from class_Planet import *
from class_Universe import *

# convert from Universe coordinates to Canvas coordinates
conv = lambda x: (x+1)*80

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

def draw_planet(canvas, planet):
    colors = ['gray', 'blue', 'red']
    canvas.create_circle(conv(planet.x), conv(planet.y), (planet.production_per_turn+3)*4, fill=colors[planet.owner])
    canvas.create_text(conv(planet.x), conv(planet.y), text=str(planet.nb_ships), fill='white')

def draw_fleet(canvas, fleet):
    colors = ['gray', 'blue', 'red']

    # draw the trajectory
    canvas.create_line(conv(fleet.starting_planet.x), conv(fleet.starting_planet.y),
        conv(fleet.destination_planet.x), conv(fleet.destination_planet.y),
        fill=colors[fleet.owner])
    
    # draw the fleet itself
    compute_pos = lambda x1,x2: conv(x2) + (((conv(x1) - conv(x2))/(fleet.total_travel_turns+1))*fleet.turns_before_arrival)
    fleet_pos_x = compute_pos(fleet.starting_planet.x, fleet.destination_planet.x)
    fleet_pos_y = compute_pos(fleet.starting_planet.y, fleet.destination_planet.y)
    
    canvas.create_circle(fleet_pos_x, fleet_pos_y, 5, fill=colors[fleet.owner])
    
    distance_left = dist((fleet_pos_x, fleet_pos_y), (conv(fleet.destination_planet.x), conv(fleet.destination_planet.y)))
    ratio = 20/distance_left
    canvas.create_line(fleet_pos_x, fleet_pos_y,
        fleet_pos_x + ((conv(fleet.destination_planet.x) - fleet_pos_x) * ratio),
        fleet_pos_y + ((conv(fleet.destination_planet.y) - fleet_pos_y) * ratio),
        arrow='last', width=4, fill=colors[fleet.owner])
    
    # draw the number of ships
    canvas.create_text(fleet_pos_x, fleet_pos_y-20, text=str(fleet.nb_ships), fill=colors[fleet.owner])

root = tk.Tk()

canvas = tk.Canvas(root, height=conv(10) , width=conv(10), background="white")

planet1 = Planet(x=1, y=2, size=10, production_per_turn=2, nb_max_ships=20, owner=1, nb_ships=6)
draw_planet(canvas, planet1)

planet2 = Planet(x=9, y=9, size=10, production_per_turn=1, nb_max_ships=20, owner=2, nb_ships=6)
draw_planet(canvas, planet2)

planet3 = Planet(x=3, y=5, size=10, production_per_turn=3, nb_max_ships=20, owner=0, nb_ships=15)
draw_planet(canvas, planet3)

planet4 = Planet(x=3, y=4, size=10, production_per_turn=3, nb_max_ships=20, owner=1, nb_ships=15)
draw_planet(canvas, planet4)

fleet1 = Fleet(planet4.owner, planet4, planet2, 10, 2)
draw_fleet(canvas, fleet1)

fleet2 = Fleet(planet2.owner, planet2, planet1, 7, 2)
fleet2.turns_before_arrival -= 5
draw_fleet(canvas, fleet2)

canvas.grid()
root.mainloop()