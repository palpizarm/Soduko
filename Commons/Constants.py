"""
Contains all constants 
"""

import tkinter

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

DIFFICULTY_X = CONTAINER_X
DIFFICULTY_Y = BUTTON_Y+175

BTSAVE_X = GAME_WEIGTH*0.5 + 120
BTSAVE_Y = BUTTON_Y + 100

BTLOAD_X = GAME_WEIGTH*0.5
BTLOAD_Y = BUTTON_Y + 100

OPTION_X = GAME_WEIGTH*0.8
OPTION_Y = CONTAINER_Y

FONT = ("Helvetica", 24, "bold")
FONT_MATRIX = ("Helvetica", 10)
FONT_BUTTON = ("Helvetica", 12, "bold")
FONT_CONFIGURE = ("Helvetica", 12)

WACTH_LABEL = ("Hours", "Minutes", "Seconds")

MATRIX_NUMBERS = [1,2,3,4,5,6,7,8,9]
MATRIX_LETTERS = ["A","B","C","D","E","F","G","H", "I"]
MATRIX_COLORES = ["#1676b0", "#a9b4bb", "#e1b403", "#8cf45d", "#6f3636", "#e11414", "#efff13", "#9609ec","#000000"]
MATRIX_POOL_BALLS = ["pool_ball1", "pool_ball2", "pool_ball3","pool_ball4", "pool_ball5", "pool_ball6","pool_ball7", "pool_ball8", "pool_ball9"]