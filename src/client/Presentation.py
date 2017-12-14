from tkinter import *

import sys


def start_game(event):
    for x in range(0, game_rows):
        for y in range(0, game_columns):
            game_array[x][y].config(state=NORMAL, text=" ", bg="white")
    label.config(text="Looking for a player")

    #call client to get start game:
    #   get label and get is_turn value

    label.config(text="Game begun")



def quit_game(event):
    sys.exit()


def button_press(event):
    if event.widget["state"] == NORMAL:
        event.widget.config(text=myLabel, fg="white", bg="black", state=DISABLED)


is_turn = True

game_rows = 3
game_columns = 3

game_array = [[0 for x in range(game_rows)] for y in range(game_columns)]

myLabel = "X"

opponentLabel = "O"

#main window
window = Tk()
window.geometry("380x420")

#Strat frame skeleton
startFrame = Frame(window)
startFrame.pack(fill=BOTH)

topFrame = Frame(startFrame)
topFrame.pack(fill=BOTH)

middleFrame = Canvas(startFrame, height=327, bg="black")
middleFrame.pack(fill=BOTH)

bottomFrame = Canvas(window)
bottomFrame.pack(fill=X, side=BOTTOM)

#start page widgets
label = Label(topFrame, text="The SEXY Tic Tak Toe...", bg="black", fg="white")
label.pack(fill=X)

for x in range(0, game_rows):
    for y in range(0, game_columns):
        button = Button(middleFrame, width=17, height=7, state=DISABLED)
        button.grid(row=x, column=y)
        button.bind('<Button-1>', button_press)
        game_array[x][y] = button

buttonStart = Button(bottomFrame, text="New game", fg="green")
buttonStart.bind("<Button-1>", start_game)
buttonStart.pack(fill=X)

buttonQuit = Button(bottomFrame, text="Quit", fg="red")
buttonQuit.bind("<Button-1>", quit_game)
buttonQuit.pack(fill=X)

window.mainloop()
