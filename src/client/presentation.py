from tkinter import *
from tkinter.font import Font
from threading import Thread
import sys


def start_game(event):
    event.widget.pack_forget()

    for x in range(0, game_rows):
        for y in range(0, game_columns):
            game_array[x][y].config(state=NORMAL, text=" ", bg="white")
    top_label.config(text="Looking for a player")

    #call client to get start game.py:
    #   get label and get is_turn value

    top_label.config(text="Game begins...")

    #wait for response


def quit_game(event):
    sys.exit()


def button_press(event):

    #send data to server

    if event.widget["state"] == NORMAL:
        event.widget.config(text=my_label, disabledforeground=my_color, bg="black", state=DISABLED)


#variables
is_turn = True

game_rows = 3
game_columns = 3

game_array = [[0 for x in range(game_rows)] for y in range(game_columns)]

my_label, my_color = "X", "red"

opponent_label, opponent_color = "O", "blue"


#main window
window = Tk()
window.geometry("452x540")

#GUI frame skeleton
top_frame = Frame(window)
top_frame.pack(fill=BOTH, side=TOP)

mid_frame = Frame(window)
mid_frame.pack(fill=BOTH)

bottom_frame = Canvas(window)
bottom_frame.pack(fill=X, side=BOTTOM)

#GUI widgets

top_label = Label(top_frame, text="The SEXY Tic Tak Toe...", bg="black", fg="white")
top_label.pack(fill=X)

my_font = Font(family="Helvetica", size=60)

grid_canvas = Canvas(mid_frame)
grid_canvas.place()

for x in range(0, game_rows):
    for y in range(0, game_columns):
        button = Button(mid_frame, width=3, height=0, state=DISABLED, font=my_font, bg="white", disabledforeground="white", text=str(x)+str(y))
        button.grid(row=x, column=y, sticky=NSEW)
        button.bind('<Button-1>', button_press)
        game_array[x][y] = button

button_start = Button(bottom_frame, text="New game.py", fg="green")
button_start.bind("<Button-1>", start_game)
button_start.pack(fill=X)

button_quit = Button(bottom_frame, text="Quit/Close", fg="red")
button_quit.bind("<Button-1>", quit_game)
button_quit.pack(fill=X)

window.mainloop()
