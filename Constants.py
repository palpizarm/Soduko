"""
Contains all constants 
"""
import tkinter
from LoadImages import *


window = tkinter.Tk()

SUDOKU_WEIGTH = int((window.winfo_screenwidth()*(0.5)))
SUDOKU_HEIGHT = int((window.winfo_screenheight()*(0.5)))
FRAME_X = int(window.winfo_screenheight()*0.5)-50
FRAME_Y = 0

CONFIGURE_WEIGTH = int(SUDOKU_WEIGTH * 0.8)
CONFIGURE_HEIGHT = int((window.winfo_screenheight()*(0.8)))

GAME_WEIGTH = int((window.winfo_screenwidth()*(0.5)))
GAME_HEIGHT = int((window.winfo_screenheight()*(0.90)))

window.withdraw()
window.destroy()

CONTAINER_X = GAME_WEIGTH*0.05
CONTAINER_Y = GAME_HEIGHT*0.10
SQUARE_WIDTH = 4
SQUARE_HEIGHT = 2

BUTTON_X = CONTAINER_X
BUTTON_Y =  GAME_HEIGHT - 200
BUTTON_WIDTH = 10

PLAYER_X = CONTAINER_X
PLAYER_Y = BUTTON_Y+50

PLAYER_NAME_X = CONTAINER_X + 100
PLAYER_NAME_Y = BUTTON_Y+52

DIFFICULTY_X = GAME_WEIGTH*0.5
DIFFICULTY_Y = BUTTON_Y+150

BTSAVE_X = GAME_WEIGTH*0.5+ 120
BTSAVE_Y = BUTTON_Y + 100

BTLOAD_X = GAME_WEIGTH*0.5
BTLOAD_Y = BUTTON_Y + 100

OPTION_X = GAME_WEIGTH*0.8
OPTION_Y = CONTAINER_Y

WATCH_X = 20
WATCH_Y = GAME_HEIGHT - 120

FONT = ("Helvetica", 24, "bold")
FONT_MATRIX = ("Helvetica", 10)
FONT_BUTTON = ("Helvetica", 12, "bold")
FONT_CONFIGURE = ("Helvetica", 12)

WACTH_LABEL = ("Hours", "Minutes", "Seconds")

MATRIX_NUMBERS = ["1","2","3","4","5","6","7","8","9"]
MATRIX_LETTERS = ["A","B","C","D","E","F","G","H", "I"]
MATRIX_COLORES = ["#1676b0", "#a9b4bb", "#e1b403", "#8cf45d", "#6f3636", "#e11414", "#efff13", "#9609ec","#000000"]
MATRIX_POOL_BALLS = []

FILL_OPTION1 = [MATRIX_NUMBERS,["white"]*9,[""]*9]
FILL_OPTION2 = [MATRIX_LETTERS,["white"]*9,[""]*9]
FILL_OPTION3 = [[""]*9,MATRIX_COLORES,[""]*9]
FILL_OPTION4 = [[""]*9,["white"]*9,MATRIX_POOL_BALLS]

FILL_OPTION = [FILL_OPTION1,FILL_OPTION2,FILL_OPTION3,FILL_OPTION4]