from threadsafe_tkinter import *
import math
from threading import Thread
import random
import sys
from abc import abstractmethod
import time


def get_random_decimal(pastel_factor=0.7):
    return [(x + pastel_factor) / (1.0 + pastel_factor) for x in [random.uniform(0, 1.0) for i in [1, 2, 3]]]


def decimal_distance(c1, c2):
    return sum([abs(x[0] - x[1]) for x in zip(c1, c2)])


def generate_new_decimal(existing_colors, pastel_factor=0.5):
    max_distance = None
    best_color = None

    for i in range(0, 100):
        color = get_random_decimal(pastel_factor=pastel_factor)

        if not existing_colors:
            return color

        best_distance = min([decimal_distance(color, c) for c in existing_colors])

        if not max_distance or best_distance > max_distance:
            max_distance = best_distance
            best_color = color

    return best_color


def shapes_gen(num_shapes, min, max):
    '''
    :param num_shapes: Type: int
    :return: returns array or co-ordinates: [x1, y1, x2, y2 ...]

    Makes sure the distance between points is more than 20
    '''
    shapes = []

    for x in range(0, num_shapes):
        points = []
        point = []  # Thi is just to compare the distance of last added co-ordinates with other

        for y in range(0, 2 * x + 6):
            not_enough_distance = True

            while not_enough_distance:
                not_enough_distance = False
                # Generate random point
                rand_int = random.randint(min, max)
                points.append(rand_int)

                if y > 1 and x == 2:
                    # only append if 1 co-ordinate present in points array
                    point.append(rand_int)

                if len(point) == 2:  # when one full co-ordinate is present in point array

                    for z in range(0, len(points) - 3):
                        # measure the distance for all points
                        distance = math.sqrt(pow(points[z] - point[0], 2) + pow(points[z + 1] - point[1], 2))

                        if distance < (max - min) / 5:
                            not_enough_distance = True
                            break

                    if not_enough_distance:
                        # delete last point if distance is not enough
                        points.pop()

                        point.pop()
                    else:
                        point.clear()

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
            rgb_color.append(int(val[y] * 255))

        hex_colors.append('#%02x%02x%02x' % (rgb_color[0], rgb_color[1], rgb_color[2]))
    return hex_colors


# class TTTInterface:
#     def __init__(self, shape_generator=shapes_gen, color_generator=colors_gen, game_rows=3, game_columns=3, players=2,
#                  gui_cell_size=140):
#         '''
#         Game GUI manipulator
#         :param shape_generator: Type: function, Args: # of shapes to be generated, Returns array of co-ordinates
#         :param color_generator: Type: function, Args: # of colors to be generated, Returns array of hex colors
#         :param game_rows:       Type: int
#         :param game_columns:    Type: int
#         :param players:         Type: int, # of players in a game
#         :param gui_cell_size:   Type: int
#         '''
#         self.shape_gen = shape_generator
#         self.color_gen = color_generator
#
#         self.num_players = players
#         self.game_rows = game_rows
#         self.game_columns = game_columns
#
#         self.gui_cell_size = gui_cell_size
#
#         self.player_shapes = []
#         self.player_colors = []
#
#         self.curr_player = -1
#
#         self.tk = GameGUI(self.game_move, self.start_game, self.quit_game, self.game_rows, self.game_columns,
#                           self.gui_cell_size)
#
#     def start_game(self):
#         self.tk.show_new_game_button(False)
#
#         self.player_shapes = self.shape_gen(self.num_players, int(self.gui_cell_size / 7),
#                                             int(self.gui_cell_size * 6 / 7))
#         self.player_colors = self.color_gen(self.num_players)
#
#         self.tk.initialize()
#
#         self.tk.change_top_label("Looking for a player")
#
#         # call client to get start game:
#         #   get label and get curr_player value
#
#         self.status_change()
#
#     def quit_game(self):
#         sys.exit()
#
#     def status_change(self):
#         self.curr_player = self.curr_player + 1
#         self.tk.change_top_label("Opponents's turn...")
#         if self.curr_player == self.num_players or self.curr_player == 0:
#             self.curr_player = 0
#             self.tk.change_top_label("Your turn...")
#
#     def toggle_buttons(self):
#         if self.curr_player == 0:
#             self.tk.change_grid_state(NORMAL)
#         else:
#             self.tk.change_grid_state(DISABLED)
#
#     def game_move(self, x, y):
#
#         # send x, y to server
#         shape, color = self.player_shapes[self.curr_player], self.player_colors[self.curr_player]
#         # self.toggle_buttons()
#
#         self.status_change()
#
#         return shape, color


class TTTGUI:

    def __init__(self, size=3):
        '''
        GUI builder for tic tac toe
        :param rows:                Type: int
        :param columns:             Type: int
        :param cell_size:           Type: int
        '''

        self.rows = size
        self.columns = size
        self.cell_size = int(240 * 3 / size)

        self.window_size = str(self.cell_size * 4)

        self.window = Tk()
        self.top_label = Label(self.window, text='The SEXY Tic Tak Toe...', bg='#ffcccc', font=28)
        self.message = Label(self.window, text='Message', bg='#ffcccc', font=28)

        self.grid_frame = Frame(self.window)

        self.button_start = Button(self.window, text='New game', fg='green')
        self.button_disconnect = Button(self.window, text='Disconnect', fg='red')
        self.button_quit = Button(self.window, text='Quit/Close', fg='red')

        self.game_array = [[0 for x in range(self.rows)] for y in range(self.columns)]
        self.button_array = [[0 for x in range(self.rows)] for y in range(self.columns)]

        # non GUI variables

        self.players = {}

        self.run = True

        self.build_gui()

    def build_gui(self):
        self.window.geometry(self.window_size + 'x' + self.window_size)
        self.window.update()
        self.window.minsize(int(self.window.winfo_width() * self.columns / 3),
                            int(self.window.winfo_height() * self.rows / 3))

        self.window.config(background='#ffcccc')

        self.top_label.place(relx=0.5, rely=0.03, anchor=CENTER)
        self.message.place(relx=0.5, rely=0.07, anchor=CENTER)

        self.grid_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        for x in range(0, self.rows):
            for y in range(0, self.columns):
                canvas = Canvas(self.grid_frame, width=self.cell_size, height=self.cell_size, bg='white', highlightcolor='#'+str(x)+str(y)+'0')
                canvas.grid(row=x, column=y)
                canvas.bind('<Button-1>', self.__move)
                self.game_array[x][y] = canvas

                # button = Button(self.game_array[x][y], width=int(self.cell_size / 7), height=int(self.cell_size / 15),
                #                 text=str(x) + str(y), fg='white', disabledforeground='white', bg='white')
                # button.bind('<Button-1>', self.__move)
                # self.button_array[x][y] = button

        self.button_start.bind('<Button-1>', self.initialize)
        self.button_start.place(relx=0.5, rely=0.92, anchor=CENTER)

        self.button_disconnect.bind('<Button-1>', self.__disconnect)

        self.button_quit.bind('<Button-1>', self.__quit)
        self.button_quit.place(relx=0.5, rely=0.97, anchor=CENTER)

    def start(self):
        while self.run:
            self.update()

    def update(self):
        self.window.update()

    def initialize(self, event):
        for x in range(0, self.rows):
            for y in range(0, self.columns):
                self.game_array[x][y].delete('all')
        self.new_game()

    # def change_gui(self):

    @abstractmethod
    def new_game(self):
        pass

    def __disconnect(self, event):
        self.disconnect()

    @abstractmethod
    def disconnect(self):
        pass

    def __quit(self, event):
        self.run = False
        self.quit()

    @abstractmethod
    def quit(self):
        pass

    def __move(self, event):
        x = (event.widget['highlightcolor'])[1]
        y = (event.widget['highlightcolor'])[2]

        self.move(x, y)

    @abstractmethod
    def move(self, row, col):
        pass

    def set_players(self, players):
        shapes = shapes_gen(len(players), int(self.cell_size / 7), int(self.cell_size * 6 / 7))
        colors = colors_gen(len(players))
        for i in range(0, len(players)):
            dic = {'Shape': shapes[i], 'Color': colors[i]}
            self.players[(players[i])] = dic

    # def disable_grid_state(self):
    #     for x in range(0, self.rows):
    #         for y in range(0, self.columns):
    #             self.button_array[x][y].config(state=DISABLED)
    #
    # def enable_grid_state(self):
    #     for x in range(0, self.rows):
    #         for y in range(0, self.columns):
    #             self.button_array[x][y].config(state=NORMAL)

    def set_board(self, row, col, player):
        #self.button_array[row][col].pack_forget()
        self.game_array[row][col].create_polygon(self.players[player]['Shape'], fill=self.players[player]['Color'])

    def clear_board(self, row, col):
        self.game_array[row][col].delete('all')

    def set_title(self, text):
        self.top_label.config(text=text)

    def set_message(self, text):
        self.message.config(text=text)

    # def draw(self, row, col, player):
    #     if event.widget['state'] == NORMAL:
    #         x = int(event.widget['text'][0])
    #         y = int(event.widget['text'][1])
    #
    #         event.widget.pack_forget()
    #         self.game_array[row][col].create_polygon(co_ordinates, fill=color)

    def show_new_game_button(self):
        self.button_disconnect.place_forget()
        self.button_start.place(relx=0.5, rely=0.92, anchor=CENTER)

    def show_disconnect_button(self):
        self.button_start.place_forget()
        self.button_disconnect.place(relx=0.5, rely=0.92, anchor=CENTER)


# def test(game):
#     game.set_message('ksdjnfsdm,f')
#
# def gui(func):
#     t = T2(func)
#     t.get_gui()


# class Test(TTTGUI):
#
#     def new_game(self):
#         print('playing')
#
#     def move(self, row, col):
#         print(row, col)
#
#     def quit(self):
#         pass
#
#     def disconnect(self):
#         pass

# class T2:
#     def __init__(self, func):
#         self.gui = Test()
#         self.func = func
#         self.gui.run()
#
#     def get_gui(self):
#         self.func(self.gui)

# def func():
#     pass
#
# # game = Test()
# # gui_thread = Thread(target=game_2.new_game)
# # gui_thread.start()
# # print('Other cmd')
# # gui_thread_2 = Thread(target=game_2.move())
# # gui_thread_2.start()
#
# # th = Thread(target=game.start)
# # th.start()
# # game.start()
#
# g = None
#
# def run_g(g):
#     g = TTTGUI()
#     g.start()
#
# run_g(g)
#
# print('Running')
# print(str(g))


