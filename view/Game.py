"""Wrapper functions for Tcl/Game.

This class manager all function to play the game
"""

import tkinter as tk
import sys
sys.path.append('../commons')


import Constants as c

class Game:


    def __init__(self, pMaster):
        """
        Create and configure the window
        """
        self.__master = pMaster
        self.__frame = tk.Tk()
        self.__frame.title("SUDOKU GAME")
        self.__frame.geometry("{}x{}+{}+{}".format(c.GAME_WEIGTH, c.GAME_HEIGHT,
                                                    c.FRAME_X, c.FRAME_Y))

        self.initComponents()
        self.initListeners()
        self.__frame.mainloop()
    

    def initComponents(self):
        """
        Create the label, entry and other widgets need
        """
        tk.Label(self.__frame, text = "SUDOKU",
                fg = "white" , bg = "red", borderwidth = 2,
                relief="solid" ,highlightcolor = "black",
                font= c.FONT).pack()


    def initListeners(self):
        """
        Create the buttons and other listeners like keyboard entries
        """


    def createTable(self):
        """
        Create the matrix 9x9
        """
    

    def updateTable(self):
        """
        look for changes in the logical matrix and update the visual matrix
        """