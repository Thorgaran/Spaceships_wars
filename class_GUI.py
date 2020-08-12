import tkinter as tk
from math import dist
import pickle

from class_Fleet import *
from class_Planet import *
from class_Universe import *
from class_Player import *
from const import *

# -------------------------------------------------------------------------------------------------
def _create_circle(self, x, y, r, **kwargs):
    """
    Adds a create_circle method to the Canvas object, more convenient than the create_oval one
    """
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

# convert from Universe coordinates to Canvas coordinates
conv = lambda x: (x+1)*80

TOTAL_SHIPS_LINE_WIDTH = 16

# -------------------------------------------------------------------------------------------------
class GUI():
    """
    Graphical User Interface
    - root = the main GUI window -> class Tk
    - canvas = the canvas inside the root -> class Canvas
    - game_info = a canvas used to display more info about the current universe -> class Canvas
    - scale_ratio = the ratio used to rescale the canvas -> float

    Optional
    - timeline = a list of Universe from a game -> [class Universe]

    Methods
    - /
    """

    def __init__(self, universe_size, timeline=[]):
        """
        universe_size: the size of the universe, used to create the canvas
        """
        # create window
        self.root = tk.Tk()
        self.root.title("Spaceship_wars_GUI")
        self.root.resizable(False, False)
        screen_smaller_dim = min(self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        title_bar_height = 30
        self.root.geometry(f'{screen_smaller_dim-title_bar_height}x{screen_smaller_dim-title_bar_height}')
        
        # configure root grid to stretch
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # add timeline nav if and only if there is one
        self.timeline = timeline
        if self.timeline:
            scale = tk.Scale(self.root, orient='h',
            from_=0, to=len(self.timeline)-1, tickinterval=5, showvalue=True, command=self.turn_update)
            scale.grid(column=0, row=0, sticky='we')

        # create canvas frame
        canvas_frame = tk.Frame(self.root)
        canvas_frame.grid(column=0, row=1, pady=(0, 10), sticky='nsew')

        # configure root grid to stretch
        canvas_frame.columnconfigure(1, weight=1)

        # add game info
        self.game_info = tk.Canvas(canvas_frame, background="white", width=4*TOTAL_SHIPS_LINE_WIDTH)
        self.game_info.grid(column=0, row=0, sticky='ns')

        # add canvas
        self.canvas = tk.Canvas(canvas_frame, background="white")
        self.canvas.grid(column=1, row=0, sticky='we')
        self.root.update()
        self.canvas.config(height=self.canvas.winfo_width())

        # compute the scale ratio
        self.scale_ratio = self.canvas.winfo_width() / conv(universe_size)

    def clear_canvases(self):
        self.game_info.delete("all")
        self.canvas.delete("all")
        return

    def display_window(self):
        self.root.mainloop()
        return

    def turn_update(self, turn_s):
        self.clear_canvases()
        self.draw_universe(self.timeline[int(turn_s)])

    def draw_universe(self, universe):
        """
        Draws all the planets and fleets in a given universe
        """
        for planet in universe.planets:
            self.draw_planet(planet)

        for fleet in universe.fleets:
            self.draw_fleet(fleet)

        # rescale the Canvas
        self.canvas.scale("all", 0, 0, self.scale_ratio, self.scale_ratio)
        
        self.draw_players_total_ships(universe)
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
        compute_pos = lambda x1,x2: conv(x2) + (((conv(x1) - conv(x2))/(fleet.total_travel_turns))*fleet.turns_before_arrival)
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

    def draw_players_total_ships(self, universe):
        # get and store ship counts
        ship_counts = []
        total_ship_count = 0
        for player in universe.players:
            nb_ships_on_planets = universe.nb_ships_on_planets(player)
            nb_ships_in_fleets = universe.nb_ships_in_fleets(player)
            
            ship_counts.append((nb_ships_on_planets, nb_ships_in_fleets))
            total_ship_count += nb_ships_on_planets + nb_ships_in_fleets

        dark_colors = {}
        dark_colors["blue"] = "blue3"
        dark_colors["red"] = "red3"
        dark_colors["green2"] = "green3"
        dark_colors["gold"] = "gold3"

        line_length = lambda x: (x/total_ship_count)*self.game_info.winfo_height()

        width = TOTAL_SHIPS_LINE_WIDTH
        for i, player in enumerate(universe.players, 0):
            pos_x = width*(i+0.5) + 0.5*((width+1)%2) + 1.5
            mid_y = line_length(ship_counts[i][0])
            end_y = mid_y + line_length(ship_counts[i][1])
            
            self.game_info.create_line(pos_x, 0, pos_x, mid_y, width=width, fill=dark_colors[player.color])
            self.game_info.create_line(pos_x, mid_y, pos_x, end_y, width=width, fill=player.color)
            text = f"{ship_counts[i][0]} | {ship_counts[i][1]}"
            self.game_info.create_text(pos_x, end_y + 5, anchor='e', angle=90, text=text, fill=player.color)

# =================================================================================================
if __name__ == "__main__":
    timeline = pickle.load(open(HISTORY_FILE, 'rb'))
    gui = GUI(timeline[0].size, timeline)
    gui.draw_universe(timeline[0])
    gui.display_window()