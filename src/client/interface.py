from tkinter import *
from tkinter.font import Font
import math
from src.client.client import Client
import string
from threading import Thread
import random
import sys


def get_random_decimal(pastel_factor=0.7):
    return [(x+pastel_factor)/(1.0+pastel_factor) for x in [random.uniform(0, 1.0) for i in [1, 2, 3]]]


def decimal_distance(c1,c2):
    return sum([abs(x[0]-x[1]) for x in zip(c1, c2)])


def generate_new_decimal(existing_colors, pastel_factor=0.5):
    max_distance = None
    best_color = None

    for i in range(0,100):
        color = get_random_decimal(pastel_factor=pastel_factor)

        if not existing_colors:
            return color

        best_distance = min([decimal_distance(color, c) for c in existing_colors])

        if not max_distance or best_distance > max_distance:
            max_distance = best_distance
            best_color = color

    return best_color


def shapes_gen(num_shapes):
    '''
    :param num_shapes: Type: int
    :return: returns array or co-ordinates: [x1, y1, x2, y2 ...]

    Makes sure the distance between points is more than 20
    '''
    shapes = []

    for x in range(0, num_shapes):
        points = []
        point = [] # Thi is just to compare the distance of last added co-ordinates with other

        for y in range(0, 2*x + 6):
            enough_distance = False

            while not enough_distance:

                # Generate random point
                rand_int = random.randint(20, 120)
                points.append(rand_int)

                if y > 1:
                    # only append if 1 co-ordinate present in points array
                    point.append(rand_int)

                if len(point) == 2: # when one full co-ordinate is present in point array

                    for z in range(0, len(points) - 3):
                        # measure the distance for all points
                        distance = math.sqrt(pow(points[z] - point[0], 2) + pow(points[z+1] - point[1], 2))

                        if distance > 20:
                            enough_distance = True

                    if not enough_distance:
                        # delete last co-ordinate if distance is not enough
                        points.pop()
                        points.pop()
                    point.clear()
                else:
                    break

        shapes.append(points)
    return shapes


def colors_gen(num_colors):
    decimals = []
    hex_colors = []

    for x in range(0, num_colors):
        rgb_color = []
        val = generate_new_decimal(decimals)
        decimals.append(val)

        for y in range(0, 3):
            rgb_color.append(int(val[y]*255))

        hex_colors.append('#%02x%02x%02x' % (rgb_color[0], rgb_color[1], rgb_color[2]))
    return hex_colors


class TttGame:
    def __init__(self, shape_generator, color_generator, game_rows=3, game_columns=3, players=2, gui_cell_size=140):
        '''
        Game GUI manipulator
        :param shape_generator: Type: function, Args: # of shapes to be generated, Returns array of co-ordinates
        :param color_generator: Type: function, Args: # of colors to be generated, Returns array of hex colors
        :param game_rows:       Type: int
        :param game_columns:    Type: int
        :param players:         Type: int, # of players in a game
        :param gui_cell_size:   Type: int
        '''
        self.shape_gen = shape_generator
        self.color_gen = color_generator

        self.num_players = players
        self.game_rows = game_rows
        self.game_columns = game_columns

        self.gui_cell_size = gui_cell_size

        self.player_shapes = []
        self.player_colors = []

        self.curr_player = -1

        self.tk = GameGUI(self.game_move, self.start_game, self.quit_game, self.game_rows, self.game_columns, self.gui_cell_size)

    def start_game(self, event):
        self.tk.show_new_game_button(False)

        self.player_shapes = self.shape_gen(self.num_players)
        self.player_colors = self.color_gen(self.num_players)

        self.tk.initialize()

        self.tk.change_top_label("Looking for a player")

        # call client to get start game:
        #   get label and get curr_player value

        self.status_change()

    def quit_game(self, event):
        sys.exit()

    def status_change(self):
        self.curr_player = self.curr_player + 1
        self.tk.change_top_label("Opponents's turn...")
        if self.curr_player == self.num_players or self.curr_player == 0:
            self.curr_player = 0
            self.tk.change_top_label("Your turn...")

    def toggle_buttons(self):
        if self.curr_player == 0:
            self.tk.change_grid_state(NORMAL)
        else:
            self.tk.change_grid_state(DISABLED)

    def game_move(self, event):

        if self.tk.draw(event.widget, self.player_shapes[self.curr_player], self.player_colors[self.curr_player]):
            # send data to server

            # self.toggle_buttons()

            self.status_change()


class GameGUI:
    def __init__(self, game_grid_click, button_start_click, button_quit_click, rows=3, columns=3, cell_size=240):
        '''
        GUI builder for tic tac toe
        :param game_grid_click:     Type: event function. Execution: user clicks on game grid.
        :param button_start_click:  Type: event function. Execution: user press new game button.
        :param button_quit_click:   Type: event function. Execution: user press quit button.
        :param rows:                Type: int
        :param columns:             Type: int
        :param cell_size:           Type: int
        '''
        self.game_grid_click = game_grid_click
        self.button_start_click = button_start_click
        self.button_quit_click = button_quit_click

        self.rows = rows
        self.columns = columns
        self.cell_size = cell_size

        self.window_size = str(cell_size*4)

        self.window = Tk()
        self.top_label = Label(self.window, text="The SEXY Tic Tak Toe...", bg="#ffcccc", font=28)

        self.my_font = Font(family="Helvetica", size=60)

        self.grid_frame = Frame(self.window)

        self.button_start = Button(self.window, text="New game", fg="green")
        self.button_quit = Button(self.window, text="Quit/Close", fg="red")

        self.game_array = [[0 for x in range(self.rows)] for y in range(self.columns)]
        self.button_array = [[0 for x in range(self.rows)] for y in range(self.columns)]

    def build_gui(self):
        self.window.geometry(self.window_size+'x'+self.window_size)
        self.window.update()
        self.window.minsize(int(self.window.winfo_width()*self.columns/3), int(self.window.winfo_height()*self.rows/3))

        self.window.config(background="#ffcccc")

        self.top_label.place(relx=0.5, rely=0.05, anchor=CENTER)
        self.grid_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        for x in range(0, self.rows):
            for y in range(0, self.columns):
                canvas = Canvas(self.grid_frame, width=self.cell_size, height=self.cell_size, bg="white")
                canvas.grid(row=x, column=y)
                self.game_array[x][y] = canvas

                button = Button(self.game_array[x][y], width=int(self.cell_size/7), height=int(self.cell_size/15), text=str(x) + str(y), fg="white", disabledforeground="white", bg="white")
                button.bind('<Button-1>', self.game_grid_click)
                self.button_array[x][y] = button

        self.button_start.bind("<Button-1>", self.button_start_click)
        self.button_start.place(relx=0.5, rely=0.92, anchor=CENTER)

        self.button_quit.bind("<Button-1>", self.button_quit_click)
        self.button_quit.place(relx=0.5, rely=0.97, anchor=CENTER)

        self.window.mainloop()

    def initialize(self):
        for x in range(0, self.rows):
            for y in range(0, self.columns):
                self.game_array[x][y].delete("all")

                self.button_array[x][y].pack()
        self.window.mainloop()

    def change_grid_state(self, state):
        for x in range(0, self.rows):
                for y in range(0, self.columns):
                    self.button_array[x][y].config(state=state)

    def change_top_label(self, text):
        self.top_label.config(text=text)

    def draw(self, widget, co_ordinates, color):
        if widget["state"] == NORMAL:
            x = int(widget["text"][0])
            y = int(widget["text"][1])

            widget.pack_forget()
            self.game_array[x][y].create_polygon(co_ordinates, fill=color)

            return True
        return False

    def show_new_game_button(self, show):
        if show:
            self.button_start.place(relx=0.5, rely=0.92, anchor=CENTER)
        else:
            self.button_start.place_forget()


# variables
game = TttGame(shapes_gen, colors_gen)
game.tk.build_gui()

