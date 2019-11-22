"""Wrapper functions for Tcl/Game.

This class manager all function to play the game
"""

import tkinter as tk
import sys
sys.path.append('../commons')

import Constants as c


class Game:
    __matrix = []
    __buttons_label = ["START GAME", "UNDO", "FINISH GAME", "ERASE GAME", "TOP 10"]
    __options_label = [""]*9
    __options_bg = c.MATRIX_COLORES
    __buttons = dict().fromkeys(__buttons_label)
    __seleceted_options = None
    def __init__(self, pMaster):
        """
        Create and configure the window
        """
        self.__master = pMaster
        self.__frame = tk.Tk()
        self.__frame.title("SUDOKU GAME")
        self.__frame.geometry("{}x{}+{}+{}".format(c.GAME_WEIGTH, c.GAME_HEIGHT,
                                                    c.FRAME_X, c.FRAME_Y))
        self.__frame.resizable(width=False,height=False)

        self.initComponents()
        self.initListeners()
        self.createTable()

        self.__frame.mainloop()
    

    def initComponents(self):
        """
        Create the label, entry and other widgets need
        """
        tk.Label(self.__frame, text = "SUDOKU",
                fg = "white" , bg = "red", borderwidth = 2,
                relief="solid" ,highlightcolor = "black",
                font= c.FONT).pack()
        tk.Label(self.__frame, text = "PLAYER",
                fg = "black",
                font= c.FONT_BUTTON).place(x=c.PLAYER_X, y=c.PLAYER_Y)
        self.difficulty = tk.Label(self.__frame, text = "DIFFICULTY: ",
                fg = "black",
                font= c.FONT_BUTTON)
        self.difficulty.place(x=c.DIFFICULTY_X, y=c.DIFFICULTY_Y)
        self.playerName = tk.Entry(self.__frame,
                                    bg="white",
                                    fg="black",
                                    width=45)
        self.playerName.place(x=c.PLAYER_NAME_X, y=c.PLAYER_NAME_Y)
        for index in range(len(self.__options_label)):
            option = tk.Button(self.__frame, text = self.__options_label[index],
                                fg = "white" , bg = self.__options_bg[index], borderwidth = 2,
                                relief="solid" ,highlightcolor = "black",
                                width = 5, height= 2, font= c.FONT_BUTTON,
                                command = "")
            if index < 6:
                option.place(x=c.OPTION_X + index*10, y=c.OPTION_Y + (index*45))
            else:
                option.place(x=c.OPTION_X + (10-index)*10, y=c.OPTION_Y + (index*45))
        
        
    def selected(self):
        """
        Call when the buttons options is press
        """
        self.__seleceted_options


    def initListeners(self):
        """
        Create the buttons and other listeners like keyboard entries
        """
        for index in range(len(self.__buttons_label)):
            button = tk.Button(self.__frame, 
                            text= self.__buttons_label[index],
                            bg= "brown", fg= "white",
                            width = c.BUTTON_WIDTH, font= c.FONT_BUTTON)
            button.place(x = c.BUTTON_X + index * 120, y = c.BUTTON_Y)
        self.__buttons[self.__buttons_label[index]] = button
        self.btSaveGame = tk.Button(self.__frame, text= "LOAD GAME",
                                    bg= "brown", fg= "white",
                                    width = c.BUTTON_WIDTH, font= c.FONT_BUTTON)
        self.btSaveGame.place(x = c.BTSAVE_X, y = c.BTSAVE_Y)
        self.btLoadGame = tk.Button(self.__frame, text= "SAVE GAME",
                            bg= "brown", fg= "white",
                            width = c.BUTTON_WIDTH, font= c.FONT_BUTTON)
        self.btLoadGame.place(x = c.BTLOAD_X, y = c.BTLOAD_Y)



    def createTable(self):
        """
        Create the visual matrix 9x9
        """
        container = tk.PanedWindow(self.__frame,bg="black")
        container.place(x=c.CONTAINER_X,y=c.CONTAINER_Y)
        for i in range(9):
            filas = []
            for j in range(9):
                square = tk.PanedWindow(container)
                square.grid(row=i, column=j, padx=1, pady=3)
                if j % 3 == 0:
                    square.grid(row=i, column=j, padx=3, pady=1)
                if i % 3 == 0:
                    square.grid(row=i, column=j, padx=1, pady=3)
                field = tk.Label(master=square, text="",
                                bg="white", justify="center",
                                fg="black", font=c.FONT_MATRIX, 
                                width=c.SQUARE_WIDTH, height=c.SQUARE_HEIGHT)
                field.grid()
                filas.append(field)
            self.__matrix.append(filas)


    def updateTable(self):
        """
        look for changes in the logical matrix and update the visual matrix
        """