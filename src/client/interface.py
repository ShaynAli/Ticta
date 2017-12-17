from tkinter import *
from tkinter.font import Font
import string
from threading import Thread
import random
import sys


def get_random_color(pastel_factor=0.5):
    return [(x+pastel_factor)/(1.0+pastel_factor) for x in [random.uniform(0, 1.0) for i in [1, 2, 3]]]


def color_distance(c1,c2):
    return sum([abs(x[0]-x[1]) for x in zip(c1, c2)])


def generate_new_color(existing_colors, pastel_factor=0.5):
    max_distance = None
    best_color = None
    for i in range(0,100):
        color = get_random_color(pastel_factor=pastel_factor)
        if not existing_colors:
            return color
        best_distance = min([color_distance(color, c) for c in existing_colors])
        if not max_distance or best_distance > max_distance:
            max_distance = best_distance
            best_color = color
    return best_color


def shapes_gen(num_shapes):
    shapes = []

    for x in range(0, num_shapes):
        points = []

        for y in range(0, 2*x + 6):
            rand_int = random.randint(20, 120)
            points.append(rand_int)
        shapes.append(points)
    return shapes


def colors_gen(num_colors):
    colors = []
    hex_colors = []
    for x in range(0, num_colors):
        color = generate_new_color(colors)
        colors.append(color)
        for y in range(0, 3):
            color[y] = (color[y]*255)
        hex_colors.append('#%02x%02x%02x' % (int(color[0]), int(color[1]), int(color[2])))
    return hex_colors


class TttGame:
    def __init__(self, game_rows = 3, game_columns = 3, player = 2, colors=["red", "green", "blue", "orange", "purple", "pink", "yellow", "indigo", "violet"]):
        self.num_players = player

        self.game_rows = game_rows
        self.game_columns = game_columns

        self.player_shapes = []
        self.player_colors = colors

        self.curr_player = -1

        self.tk = GameGUI(self)

    def start_game(self, event):
        event.widget.pack_forget()

        self.player_shapes = shapes_gen(self.num_players)
        self.player_colors = colors_gen(self.num_players)

        for x in range(0, self.game_rows):
            for y in range(0, self.game_columns):
                self.tk.game_array[x][y].delete("all")
                self.tk.game_array[x][y].config(state=NORMAL)
        self.tk.top_label.config(text="Looking for a player")

        # call client to get start game:
        #   get label and get curr_player value

        self.status_change()

    def quit_game(self, event):
        sys.exit()

    def status_change(self):
        self.curr_player = self.curr_player + 1
        self.tk.top_label.config(text="Opponents's turn...")
        if self.curr_player == self.num_players or self.curr_player == 0:
            self.curr_player = 0
            self.tk.top_label.config(text="Your turn...")

    def toggle_buttons(self):
        if self.curr_player == 0:
            for x in range(0, self.game_rows):
                for y in range(0, self.game_columns):
                    if self.game_array[x][y]["text"].length == 2:
                        self.tk.game_array[x][y].config(state=NORMAL)
        else:
            for x in range(0, self.game_rows):
                for y in range(0, self.game_columns):
                    self.tk.game_array[x][y].config(state=DISABLED)

    def button_press(self, event):
        # send data to server

        if event.widget["state"] == NORMAL:
            print(int(event.widget["width"])-140 + int(event.widget["height"])-140)

            event.widget.config(state=DISABLED)
            event.widget.create_polygon(self.player_shapes[self.curr_player], fill=self.player_colors[self.curr_player])

            # self.toggle_buttons()

            self.status_change()


class GameGUI:
    def __init__(self, main):
        self.game = main
        self.window = Tk()
        self.top_label = Label(self.window, text="The SEXY Tic Tak Toe...", bg="#ffcccc", font=28)

        self.my_font = Font(family="Helvetica", size=60)

        self.grid_frame = Frame(self.window)

        self.button_start = Button(self.window, text="New game", fg="green")
        self.button_quit = Button(self.window, text="Quit/Close", fg="red")

        self.game_array = [[0 for x in range(self.game.game_rows)] for y in range(self.game.game_columns)]

    def build_game(self):
        self.window.geometry("495x540")
        self.window.update()
        self.window.minsize(int(self.window.winfo_width()*self.game.game_columns/3), int(self.window.winfo_height()*self.game.game_rows/3))

        self.window.config(background="#ffcccc")

        self.top_label.place(relx=0.5, rely=0.05, anchor=CENTER)
        self.grid_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        for x in range(0, self.game.game_rows):
            for y in range(0, self.game.game_columns):
                canvas = Canvas(self.grid_frame, width=140+x, height=140+y, state=DISABLED, bg="white")
                canvas.grid(row=x, column=y)
                canvas.bind('<Button-1>', self.game.button_press)
                self.game_array[x][y] = canvas

        self.button_start.bind("<Button-1>", self.game.start_game)
        self.button_start.place(relx=0.5, rely=0.92, anchor=CENTER)

        self.button_quit.bind("<Button-1>", self.game.quit_game)
        self.button_quit.place(relx=0.5, rely=0.97, anchor=CENTER)

        self.window.mainloop()


# variables
game = TttGame()
game.tk.build_game()
