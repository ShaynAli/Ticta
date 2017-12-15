from tkinter import *
from tkinter.font import Font
from threading import Thread
import sys


class Ttt_game:
    def __init__(self, game_rows, game_columns, players):
        self.player_num = players

        self.game_rows = game_rows
        self.game_columns = game_columns

        self.curr_label, self.curr_color = " ", " "
        self.my_label, self.my_color = "X", "#3366ff"

        for p in range(1, players):
            self.opponent_label, self.opponent_color = "O", "#33cccc"

        self.is_turn = True

        self.tk = GameGUI(self)

    def start_game(self, event):
        event.widget.pack_forget()

        for x in range(0, self.game_rows):
            for y in range(0, self.game_columns):
                self.tk.game_array[x][y].config(state=NORMAL, text=str(x)+str(y), fg="white")
        self.tk.top_label.config(text="Looking for a player")

        # call client to get start game:
        #   get label and get is_turn value

        self.status_change()

    def quit_game(self, event):
        sys.exit()

    def status_change(self):
        if self.is_turn:
            self.curr_color = self.my_color
            self.curr_label = self.my_label
            self.tk.top_label.config(text="Your move...", fg=self.curr_color)
            self.is_turn = False
        else:
            # get user input
            self.curr_color = self.opponent_color
            self.curr_label = self.opponent_label
            self.tk.top_label.config(text="Opponent's move...", fg=self.curr_color)
            self.is_turn = True

    def toggle_buttons(self):
        if self.is_turn:
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
            event.widget.config(text=self.curr_label, disabledforeground=self.curr_color, state=DISABLED)

        # self.toggle_buttons()
        self.status_change()


class GameGUI:
    def __init__(self, main):
        self.game = main
        self.window = Tk()
        self.top_label = Label(self.window, text="The SEXY Tic Tak Toe...", bg="#ff5050", fg="white", font=28)

        self.my_font = Font(family="Helvetica", size=60)

        self.grid_canvas = Frame(self.window)

        self.button_start = Button(self.window, text="New game", fg="green")
        self.button_quit = Button(self.window, text="Quit/Close", fg="red")

        self.game_array = [[0 for x in range(self.game.game_rows)] for y in range(self.game.game_columns)]

    def build_game(self):
        self.window.geometry("495x540")
        self.window.update()
        self.window.minsize(int(self.window.winfo_width()*self.game.game_columns/3), int(self.window.winfo_height()*self.game.game_rows/3))

        self.window.config(background="#ff5050")

        self.top_label.place(relx=0.5, rely=0.05, anchor=CENTER)
        self.grid_canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

        for x in range(0, self.game.game_rows):
            for y in range(0, self.game.game_columns):
                self.button = Button(self.grid_canvas, width=3, height=0, state=DISABLED, font=self.my_font, bg="white")
                self.button.grid(row=x, column=y)
                self.button.bind('<Button-1>', self.game.button_press)
                self.game_array[x][y] = self.button

        self.button_start.bind("<Button-1>", self.game.start_game)
        self.button_start.place(relx=0.5, rely=0.92, anchor=CENTER)

        self.button_quit.bind("<Button-1>", self.game.quit_game)
        self.button_quit.place(relx=0.5, rely=0.97, anchor=CENTER)

        self.window.mainloop()


# variables
game_row = 3
game_column = 3
players = 2

game = Ttt_game(game_row, game_column, players)
game.tk.build_game()
