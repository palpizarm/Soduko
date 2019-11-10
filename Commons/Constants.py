"""
Contains all constants 
"""

import tkinter

window = tkinter.Tk()
print(window.winfo_screenwidth())
print(window.winfo_screenheight())
print(window.winfo_screenwidth()*0.5)

SUDUKU_WEIGTH = int((window.winfo_screenwidth()*(0.5)))
SUDOKU_HEIGHT = int((window.winfo_screenheight()*(0.5)))
FRAME_X = int(window.winfo_screenheight()*0.5)-50
FRAME_Y = 10

GAME_WEIGTH = int((window.winfo_screenwidth()*(0.5)))
GAME_HEIGHT = int((window.winfo_screenheight()*(0.95)))



window.withdraw()
window.destroy()

FONT = ("Helvetica", 24, "bold")