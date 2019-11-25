"""Wrapper functions for Tcl/Game.

This class manager all function to play the game
"""

import tkinter as tk
from tkinter import messagebox
import ast


import Constants as c
from LoadImages import *
from Handler import *


class Game:
    __matrix = []
    __buttons_label = ["START GAME", "UNDO", "FINISH GAME", "ERASE GAME", "TOP 10"]
    __buttons = dict().fromkeys(__buttons_label)
    __seleceted_options = ""
    __watchAtivited = ""
    __time = ["0"]*3
    __timeEntry = []
    __buttonsOptions = []

    def __init__(self, pMaster, pGameFrame):
        """
        Create and configure the window
        """
        self.__master = pMaster
        self.__handler = Handler()
        self.__frame = pGameFrame
        self.__frame.title("SUDOKU GAME")
        self.__frame.geometry("{}x{}+{}+{}".format(c.GAME_WEIGTH, c.GAME_HEIGHT,
                                                    c.FRAME_X, c.FRAME_Y))
        self.__frame.resizable(width=False,height=False)
        self.__options_label = []
        self.__options_bg = []
        self.__options_images = [] 
        self.initComponents()
        self.initListeners()
        self.__frame.protocol('WM_DELETE_WINDOW', self.exit)
        self.createTable()
    

    def exit(self):
        """
        Hide the frame
        """
        self.__frame.withdraw()
        self.__master.focus_force()
        self.__master.grab_set()


    def getSettingGame(self):
        """
        Read the file to get the adjusment of the game
        """
        for index in range(len(self.__timeEntry)):
                self.__timeEntry[index].config(state="normal")
        self.playerName.config(state="normal")
        file = open("sudoku2019Setting.dat","r")
        level = int(file.readline())
        self.__fillOption = int(file.readline())
        self.__watchAtivited = int(file.readline())
        if self.__watchAtivited == 3:
            self.__time = file.readline()
            self.__time = ast.literal_eval(self.__time)
        file.close()
        self.cleanTable()
        self.__options_label,self.__options_bg = c.FILL_OPTION[self.__fillOption-1]
        if level == 1:
            self.__difficulty.config(text = "DIFFICULTY: EASY")
        elif level == 2:
            self.__difficulty.config(text = "DIFFICULTY: NORMAL")
        elif level == 3:
            self.__difficulty.config(text = "DIFFICULTY: HARD")
        self.__handler.setLevel(level)
        self.__handler.chooseRandomGames()
        for buttonIndex in range(len(self.__buttonsOptions)):
            if  self.__fillOption == 4:
                self.__buttonsOptions[buttonIndex].config(image = self.__options_images[buttonIndex],
                                                            width = 45, height= 45)          
            else:
                self.__buttonsOptions[buttonIndex].config(text = self.__options_label[buttonIndex],
                                                    bg = self.__options_bg[buttonIndex],
                                                    width = 5, height= 2)
        if self.__watchAtivited == 1 or self.__watchAtivited == 3:
            self.__watch.place(x=c.WATCH_X,y=c.WATCH_Y)
        else:
            self.__watch.place_forget()
        self.updateTable()


    def initComponents(self):
        """
        Create the label, entry and other widgets need
        """
        self.__options_images = loadImages().copy()
        tk.Label(self.__frame, text = "SUDOKU",
                fg = "white" , bg = "red", borderwidth = 2,
                relief="solid" ,highlightcolor = "black",
                font= c.FONT).pack()
        tk.Label(self.__frame, text = "PLAYER",
                fg = "black",
                font= c.FONT_BUTTON).place(x=c.PLAYER_X, y=c.PLAYER_Y)
        pilImage = Image.open("images/ball1.png")
        row = ImageTk.PhotoImage(pilImage)
        self.__optionSelect = tk.Button(self.__frame, image = row,
                                width = 50, height= 50,)
        self.playerName = tk.Entry(self.__frame,
                                    bg="white",
                                    fg="black",
                                    width=45)
        self.playerName.bind('<KeyRelease>', self.checkName)
        self.playerName.place(x=c.PLAYER_NAME_X, y=c.PLAYER_NAME_Y)
        for index in range(9):
            option = tk.Button(self.__frame, fg = "black" ,  borderwidth = 2, 
                                relief="solid" ,highlightcolor = "black",
                                width = 5, height= 2,font= c.FONT_BUTTON)
            option.bind("<Button-1>",self.selected)
            if index < 6:
                option.place(x=c.OPTION_X + index*10, y=c.OPTION_Y + (index*45))
            else:
                option.place(x=c.OPTION_X + (10-index)*10, y=c.OPTION_Y + (index*45))
            self.__buttonsOptions.append(option)
        self.__difficulty = tk.Label(self.__frame,
                        fg = "black", text="PRUEBA",
                        font= c.FONT_BUTTON)
        self.__difficulty.place(x=c.DIFFICULTY_X, y=c.DIFFICULTY_Y)
        # To show the watch in the frame if a selceted option is 1 or 3
        self.__watch = tk.Canvas(self.__frame, width=200,
                        height=100, bg="white", highlightbackground = "white")
        self.__watch.place(x=c.WATCH_X,y=c.WATCH_Y)
        for i in range(3):
            subcontainer = tk.Canvas(self.__watch, 
                                width=70, height=70,
                                bg="white", highlightbackground = "white")
            subcontainer.grid(row=1,column=i, padx=4, pady=4)
            tk.Label(master=self.__watch, text = c.WACTH_LABEL[i],
                    bg="white", fg="black",
                    font=c.FONT_CONFIGURE).grid(row=0,column=i)
            entry = tk.Entry(master=self.__watch,bg="white", 
                            fg="black", width=4,
                            font=c.FONT_CONFIGURE)
            entry.grid(row=1,column=i)
            entry.bind('<KeyRelease>', self.checkEntriesTimes)
            self.__timeEntry.append(entry)


    def selected(self, btn):
        """
        Call when the buttons options is press
        """
        index = 0
        for i in range(9):
            if self.__buttonsOptions[i] == btn.widget:
                index = i
                break
        print(index)
        self.__optionSelect.place(x=c.SELECTED_X, y=c.SELECTED_Y + (45*index))


    def matrixOptionSelected(self, btn):
        """
        Search the option selected of the matrix
        """
        matrixRow = 0
        matrixColumn = 0
        for i in range(9):
            for j in range(9):
                if self.__matrix[i][j] == btn.widget:
                    matrixRow = i
                    matrixColumn = j
                    break
        print(matrixRow)
        print(matrixColumn)


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
        self.__buttons[self.__buttons_label[0]].config(command = self.startGame)
        self.__buttons[self.__buttons_label[1]].config(command = self.undo)
        self.__buttons[self.__buttons_label[2]].config(command = self.finishGame)
        self.__buttons[self.__buttons_label[3]].config(command = self.erase)
        self.__buttons[self.__buttons_label[4]].config(command = self.top10)
        self.btSaveGame = tk.Button(self.__frame, text= "LOAD GAME",
                                    bg= "brown", fg= "white",
                                    width = c.BUTTON_WIDTH, font= c.FONT_BUTTON,
                                    command = self.saveGame)
        self.btSaveGame.place(x = c.BTSAVE_X, y = c.BTSAVE_Y)
        self.btLoadGame = tk.Button(self.__frame, text= "SAVE GAME",
                            bg= "brown", fg= "white",
                            width = c.BUTTON_WIDTH, font= c.FONT_BUTTON,
                            command = self.loadGame)
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
                square.grid(row=i, column=j, padx=1, pady=1)
                field = tk.Button(master=square,
                                bg="white", justify="center",
                                fg="black", font=c.FONT_MATRIX, 
                                width=c.SQUARE_WIDTH, height=c.SQUARE_HEIGHT)
                field.bind("<Button-1>",self.matrixOptionSelected)
                field.grid()
                filas.append(field)
            self.__matrix.append(filas)


    def updateTable(self):
        """
        look for changes in the logical matrix and update the visual matrix
        """
        gameMatrix = self.__handler.getGamePlayer()
        if self.__fillOption == 1 or self.__fillOption == 2:
            for i in range(9):
                for j in range(9):
                    if gameMatrix[i][j] != 0:
                        self.__matrix[i][j].config(text=self.__options_label[gameMatrix[i][j]-1],
                                                    width=c.SQUARE_WIDTH, height=c.SQUARE_HEIGHT)
        elif self.__fillOption == 3:
            for i in range(9):
                for j in range(9):
                    if gameMatrix[i][j] != 0:
                        self.__matrix[i][j].config(bg=self.__options_bg[gameMatrix[i][j]-1],
                                                   width=c.SQUARE_WIDTH, height=c.SQUARE_HEIGHT)
        elif self.__fillOption == 4:
            for i in range(9):
                for j in range(9):
                    if gameMatrix[i][j] != 0:
                        self.__matrix[i][j].config(image=self.__options_images[gameMatrix[i][j]-1],
                                                    width=35,height=35)


    def cleanTable(self):
        """
        Remove all elements in the table
        """
        for i in range(9):
            self.__buttonsOptions[i].config(image = '', bg = 'white', text = '')
            for j in range(9):
                self.__matrix[i][j].config(text="",bg="white", image = '',
                                            width=c.SQUARE_WIDTH, height=c.SQUARE_HEIGHT)

    

    def loadGame(self):
        """
        Load the game from the file
        """
        file = open('sudoku2019juegoactual.dat', 'r')
    

    def saveGame(self):
        """
        Save the actual game in the file
        """
        file = open('sudoku2019juegoactual.dat', 'w+')
    

    def startGame(self):
        """
        Check and  start the game if is possible
        """
        for index in range(len(self.__timeEntry)):
                self.__timeEntry[index].config(state="disabled")
        self.playerName.config(state="disabled")


    def undo(self):
        """
        Delete the last move
        """
    

    def finishGame(self):
        """
        Exit and delete the game
        """
    
    
    def erase(self):
        """
        Delete all move that the players did
        """

    
    def top10(self):
        """
        show the top10 of each levels
        """
        top10Frame = tk.Toplevel(self.__frame)
        top10Frame.focus_force()
        top10Frame.transient(self.__frame)
        top10Frame.grab_set()
        top10Frame.title("Top 10")
        top10Frame.config(bg="white")
        top10Frame.geometry("{}x{}+{}+{}".format(700,
                                            600,
                                            c.FRAME_X,
                                            c.FRAME_Y))
        tk.Label(top10Frame, text="Top 10 \n Easy Level",
                fg="black", font=c.FONT_BUTTON).place(x=50,y=0)
        tk.Label(top10Frame, text="Top 10 \n Normal Level",
                fg="black", font=c.FONT_BUTTON).place(x=250,y=0)
        tk.Label(top10Frame, text="Top 10 \n Hard Level",
                fg="black", font=c.FONT_BUTTON).place(x=500,y=0)
        easyLevel = tk.Canvas(top10Frame, width=260,
                            height=500, bg="white",
                            highlightbackground = "white")
        easyLevel.place(x=c.TOP10EASY_X,y=c.TOP10EASY_Y)
        normalLevel = tk.Canvas(top10Frame, width=260,
                            height=500, bg="white",
                            highlightbackground = "white")
        normalLevel.place(x=c.TOP10NORMAL_X,y=c.TOP10NORMAL_Y)
        hardLevel = tk.Canvas(top10Frame, width=260,
                            height=500, bg="white",
                            highlightbackground = "white")
        hardLevel.place(x=c.TOP10HARD_X,y=c.TOP10HARD_Y)
        tk.Label(easyLevel, text="Player",
        fg="black", bg = "white",
        font=c.FONT_BUTTON).grid(row=0,column= 0)
        tk.Label(easyLevel, text="Time",
        fg="black", bg = "white",
        font=c.FONT_BUTTON).grid(row=0,column= 1)
        tk.Label(normalLevel, text="Player",
        fg="black", bg = "white",
        font=c.FONT_BUTTON).grid(row=0,column= 0)
        tk.Label(normalLevel, text="Time",
        fg="black", bg = "white",
        font=c.FONT_BUTTON).grid(row=0,column= 1)
        tk.Label(hardLevel, text="Player",
        fg="black", bg = "white",
        font=c.FONT_BUTTON).grid(row=0,column= 0)
        tk.Label(hardLevel, text="Time",
        fg="black", bg = "white",
        font=c.FONT_BUTTON).grid(row=0,column= 1)
        bestPlayers = self.__handler.getBestPlayersToTop()
        playersEasy = bestPlayers[0]
        for index in range(len(playersEasy)):
            tk.Label(easyLevel, text=str(index + 1)+ '.' +playersEasy[index][0],
            fg="black", bg = "white", anchor = 'w',
            font=c.FONT_BUTTON).grid(row=index+1,column= 0)
            tk.Label(easyLevel, text=playersEasy[index][1],
            fg="black", bg = "white", 
            font=c.FONT_BUTTON).grid(row=index+1,column= 1)
        playersEasy = bestPlayers[1]
        for index in range(len(playersEasy)):
            tk.Label(normalLevel, text=str(index + 1)+ '.' +playersEasy[index][0],
            fg="black", bg = "white",
            font=c.FONT_BUTTON).grid(row=index+1,column= 0)
            tk.Label(normalLevel, text=playersEasy[index][1],
            fg="black", bg = "white",
            font=c.FONT_BUTTON).grid(row=index+1,column= 1)
        playersEasy = bestPlayers[2]
        for index in range(len(playersEasy)):
            tk.Label(hardLevel, text=str(index + 1)+ '.' +playersEasy[index][0],
            fg="black", bg = "white",
            font=c.FONT_BUTTON).grid(row=index+1,column= 0)
            tk.Label(hardLevel, text=playersEasy[index][1],
            fg="black", bg = "white",
            font=c.FONT_BUTTON).grid(row=index+1,column= 1)


    def checkEntriesTimes(self,event):
        """
        check if a entris of hours, minutes and seconds have correct format
        """
        hours = self.__timeEntry[0].get()
        minutes = self.__timeEntry[1].get()
        seconds = self.__timeEntry[2].get()
        if hours != "":
            if not hours.isdigit():
                 self.__timeEntry[0].delete(0,"end")   
            else:
                hours = int(hours)
                if hours < 0 or hours > 4:
                    self.__timeEntry[0].delete(0,"end")
                    messagebox.showerror("Hours Format", "Las horas deben estar entre 0 - 4")
        if minutes != "":
            if not minutes.isdigit():
                self.__timeEntry[1].delete(0,"end")
            else:
                minutes = int(minutes)
                if minutes < 0 or minutes > 59:
                    self.__timeEntry[1].delete(0,"end")
                    messagebox.showerror("Minutes Format", "Las minutos deben estar entre 0 - 59")
        if seconds != "":
            if not seconds.isdigit():
                self.__timeEntry[2].delete(0,"end")
            else:
                seconds = int(seconds)
                if seconds < 0 or seconds > 59:
                    self.__timeEntry[2].delete(0,"end")
                    messagebox.showerror("Seconds Format", "Los segundos deben estar entre 0 - 59")
    

    def checkName(self,event):
        """
        Check each enter in the name entry
        """
        name = self.playerName.get()
        if name.isdigit():
            self.playerName.delete(len(name)-1,"end")
        if len(name) > 30:
            self.playerName.delete(0,"end")
            messagebox.showerror("Name format", "El nombre debe ser menor a 30 caracteres")