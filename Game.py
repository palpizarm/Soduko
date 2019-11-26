"""Wrapper functions for Tcl/Game.

This class manager all function to play the game
"""

import tkinter as tk
from tkinter import messagebox
import ast
import threading

import Constants as c
from LoadImages import *
from Handler import *


class Game:
    __matrix = []
    __buttons_label = ["START GAME", "UNDO", "FINISH GAME", "ERASE GAME", "TOP 10"]
    __buttons = dict().fromkeys(__buttons_label)
    __seleceted_options = ""
    __watchActivited = ""
    __time = [0]*3
    __timeEntry = []
    __buttonsOptions = []
    __number = 0
    __start = False
    __seconds = 0
    
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
        self.__timeThread = threading.Thread(target=self.startWatch)
        self.__timeThread.start()
        self.createTable()
    

    def exit(self):
        """
        Hide the frame
        """
        self.playerName.delete(0,'end')
        self.__frame.withdraw()
        self.__master.focus_force()
        self.__master.grab_set()
        self.__master.deiconify()
        self.__seconds = 0


    def getSettingGame(self):
        """
        Read the file to get the adjusment of the game
        """
        self.__start = False
        for index in range(len(self.__timeEntry)):
            self.__timeEntry[index].config(state="disabled")
            self.__timeEntry[index].delete(0,'end')
        self.playerName.config(state="normal")
        file = open("sudoku2019Setting.dat","r")
        self.__level = int(file.readline())
        self.__fillOption = int(file.readline())
        self.__watchActivited = int(file.readline())
        if self.__watchActivited == 3:
            self.__time = file.readline()
            self.__time = ast.literal_eval(self.__time)
            self.__seconds = HoursToSec(self.__time[0],self.__time[1], self.__time[2])
            for index in range(len(self.__timeEntry)):
                self.__timeEntry[index].config(state="normal")
                self.__timeEntry[index].insert(0,self.__time[index])
        file.close()
        self.cleanTable()
        self.__options_label,self.__options_bg = c.FILL_OPTION[self.__fillOption-1]
        if self.__level == 1:
            self.__difficulty.config(text = "DIFFICULTY: EASY")
        elif self.__level == 2:
            self.__difficulty.config(text = "DIFFICULTY: NORMAL")
        elif self.__level == 3:
            self.__difficulty.config(text = "DIFFICULTY: HARD")
        self.__handler.setLevel(self.__level)
        self.__handler.chooseRandomGames()
        for buttonIndex in range(len(self.__buttonsOptions)):
            if  self.__fillOption == 4:
                self.__buttonsOptions[buttonIndex].config(image = self.__options_images[buttonIndex],
                                                            width = 45, height= 45)          
            else:
                self.__buttonsOptions[buttonIndex].config(text = self.__options_label[buttonIndex],
                                                    bg = self.__options_bg[buttonIndex],
                                                    width = 5, height= 2)
        if self.__watchActivited == 1 or self.__watchActivited == 3:
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
        if self.__start:
            for i in range(9):
                if self.__buttonsOptions[i] == btn.widget:
                    self.__number = i+1
                    break
            print(self.__number)
            self.__optionSelect.place(x=c.SELECTED_X, y=c.SELECTED_Y + (45*(self.__number-1)))
        else:
            messagebox.showwarning("Log in", "Presione el boton de start pata iniciar el juego")


    def matrixOptionSelected(self, btn):
        """
        Search the option selected of the matrix
        """
        if self.__number != 0 and self.__start:
            matrixRow = 0
            matrixColumn = 0
            for i in range(9):
                for j in range(9):
                    if self.__matrix[i][j] == btn.widget:
                        matrixRow = i
                        matrixColumn = j
                        break
                if self.__matrix[i][j] == btn.widget:
                    break
            result = self.__handler.addNumberToGame(matrixRow,matrixColumn,self.__number)
            if result[0] == False:
                messagebox.showerror("Error", result[1])
            self.updateTable()
            if result[0] == True and result[1] == "Complete":
                messagebox.showinfo("WIN", "Felicidades ha completado el juego")
                self.getSettingGame()
                self.__handler.addPlayerTop10(self.__seconds)
                self.__seconds = 0
            self.__optionSelect.place_forget()
            self.__number = 0
        else:
            messagebox.showwarning("OPTION SELECTED", "Seleccione un valor primero")


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
        self.btSaveGame = tk.Button(self.__frame, text= "SAVE GAME",
                                    bg= "brown", fg= "white",
                                    width = c.BUTTON_WIDTH, font= c.FONT_BUTTON,
                                    command = self.saveGame)
        self.btSaveGame.place(x = c.BTSAVE_X, y = c.BTSAVE_Y)
        self.btLoadGame = tk.Button(self.__frame, text= "LOAD GAME",
                            bg= "brown", fg= "white",
                            width = c.BUTTON_WIDTH, font= c.FONT_BUTTON,
                            command = self.loadGame)
        self.btLoadGame.place(x = c.BTLOAD_X, y = c.BTLOAD_Y)
        self.btSolveGame = tk.Button(self.__frame, text= "SOLVE GAME",
                            bg= "brown", fg= "white",
                            width = c.BUTTON_WIDTH, font= c.FONT_BUTTON,
                            command = self.solveGame)
        self.btSolveGame.place(x = c.BTSOLVE_X, y = c.BTSOLVE_Y)


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
                    else:
                        self.__matrix[i][j].config(text="",width=c.SQUARE_WIDTH, height=c.SQUARE_HEIGHT)
        elif self.__fillOption == 3:
            for i in range(len(gameMatrix)):
                for j in range(len(gameMatrix[0])):
                    if gameMatrix[i][j] != 0:
                        self.__matrix[i][j].config(bg=self.__options_bg[gameMatrix[i][j]-1],
                                                   width=c.SQUARE_WIDTH, height=c.SQUARE_HEIGHT)
                    else:
                        self.__matrix[i][j].config(bg="white", width=c.SQUARE_WIDTH, height=c.SQUARE_HEIGHT)
        elif self.__fillOption == 4:
            for i in range(9):
                for j in range(9):
                    if gameMatrix[i][j] != 0:
                        self.__matrix[i][j].config(image=self.__options_images[gameMatrix[i][j]-1],
                                                     width=35, height=35)
                    else:
                        self.__matrix[i][j].config(image="", width=c.SQUARE_WIDTH, height=c.SQUARE_HEIGHT)


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
        if self.__start:
            messagebox.showerror("Load Game", "No se puede cargar el juego, hay un juego en proceso")
        else:
            self.cleanTable()
            file = open('sudoku2019juegoactual.dat', 'r')
            game = file.readline()
            plays = file.readline()
            self.__level = int(file.readline())
            self.__fillOption = int(file.readline())
            name = file.readline()
            self.__watchActivited = int(file.readline())
            if self.__watchActivited == 3:
                self.__seconds = int(file.readline())
            game = ast.literal_eval(game)
            plays = ast.literal_eval(plays)
            self.__handler.loadCurrentGame(game,plays,name)
            self.playerName.config(state="normal")
            self.playerName.delete(0,'end')
            self.playerName.insert(0,name)
            self.playerName.config(state="disabled")
            self.__options_label,self.__options_bg = c.FILL_OPTION[self.__fillOption-1]
            for buttonIndex in range(len(self.__buttonsOptions)):
                if  self.__fillOption == 4:
                    self.__buttonsOptions[buttonIndex].config(image = self.__options_images[buttonIndex],
                                                                width = 45, height= 45)          
                else:
                    self.__buttonsOptions[buttonIndex].config(text = self.__options_label[buttonIndex],
                                                        bg = self.__options_bg[buttonIndex],
                                                        width = 5, height= 2)
            if self.__watchActivited == 1 or self.__watchActivited == 3:
                self.__watch.place(x=c.WATCH_X,y=c.WATCH_Y)
            else:
                self.__watch.place_forget()
            self.updateTable()
            

    def saveGame(self):
        """
        Save the actual game in the file
        """
        if self.__start:
            file = open('sudoku2019juegoactual.dat', 'w+')
            game, plays = self.__handler.saveCurrentGame()
            file.write(str(game) + '\n')
            file.write(str(plays) + '\n')
            file.write(str(self.__level) + '\n')
            file.write(str(self.__fillOption) + '\n')
            file.write(self.playerName.get() + '\n')
            file.write(str(self.__watchActivited) + '\n')
            if self.__watchActivited != 2:
                file.write(str(self.__seconds) + '\n')
            file.close()
        else:
            messagebox.showwarning("Save Game", "No se pudo guardar el juego no ha iniciado")


    def solveGame(self):
        """
        Solve the current game
        """
        if self.__start:
            self.__handler.solveSudoku()
            self.updateTable()
            messagebox.showinfo("Game solve", "Presione enter para cerrar la solucion")
            self.getSettingGame()
            self.__seconds = 0
            self.__start = False
        else:
            messagebox.showinfo("Solve Game", "No hay ningun juego en proceso")


    def startGame(self):
        """
        Check and  start the game if is possible
        """
        if not self.__start:
            if len(self.playerName.get()) == 0:
                messagebox.showerror("ERROR", "Ingrese el nombre para iniciar el juego")
                return
            self.__start = True
            self.__handler.setPlayer(self.playerName.get())
            for index in range(len(self.__timeEntry)):
                    self.__timeEntry[index].config(state="disabled")
            self.playerName.config(state="disabled")


    def undo(self):
        """
        Delete the last move
        """
        if self.__start:
            self.__handler.removeLastMove()
            self.updateTable()
        else:
            messagebox.showwarning("Undo", "No se ha iniciado el juego")
    

    def finishGame(self):
        """
        Exit and delete the game and load a new game
        """
        if self.__start:
            opcion = messagebox.askyesno("Finish Game","¿Esta seguro que desea finalizar el juego?")
            if opcion:
                self.getSettingGame()
        else:
            messagebox.showwarning("Finish Game", "No se ha iniciado el juego")
    

    def erase(self):
        """
        Delete all move that the players did
        """
        if self.__start:
            opcion = messagebox.askyesno("Erase game","¿Esta seguro que desea borrar el juego?")
            if opcion:
                self.__handler.EraseGame()
        else:
            messagebox.showwarning("Erase game", "No se ha iniciado el juego")
        self.updateTable()
    

    def top10(self):
        """
        show the top10 of each levels
        """
        self.__start = False
        self.top10Frame = tk.Toplevel(self.__frame)
        self.top10Frame.protocol('WM_DELETE_WINDOW', self.exitTop10)
        self.top10Frame.focus_force()
        self.top10Frame.transient(self.__frame)
        self.top10Frame.grab_set()
        self.top10Frame.title("Top 10")
        self.top10Frame.config(bg="white")
        self.top10Frame.geometry("{}x{}+{}+{}".format(700,
                                            500,
                                            c.FRAME_X,
                                            c.FRAME_Y))
        tk.Label(self.top10Frame, text="Top 10 \n Easy Level",
                fg="black", font=c.FONT_BUTTON).place(x=50,y=0)
        tk.Label(self.top10Frame, text="Top 10 \n Normal Level",
                fg="black", font=c.FONT_BUTTON).place(x=250,y=0)
        tk.Label(self.top10Frame, text="Top 10 \n Hard Level",
                fg="black", font=c.FONT_BUTTON).place(x=500,y=0)
        easyLevel = tk.Canvas(self.top10Frame, width=260,
                            height=500, bg="white",
                            highlightbackground = "white")
        easyLevel.place(x=c.TOP10EASY_X,y=c.TOP10EASY_Y)
        normalLevel = tk.Canvas(self.top10Frame, width=260,
                            height=500, bg="white",
                            highlightbackground = "white")
        normalLevel.place(x=c.TOP10NORMAL_X,y=c.TOP10NORMAL_Y)
        hardLevel = tk.Canvas(self.top10Frame, width=260,
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


    def exitTop10(self):
        """
        Close the top10 frame
        """
        self.top10Frame.destroy()
        self.__start = True

         
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
        

    def startWatch(self):
        """
        Inicialize the watch
        """
        if self.__start and self.__watchActivited != 2:
            if self.__watchActivited == 1:
                self.__seconds += 1
            else:
                self.__seconds -= 1
                if self.__seconds == 0:
                    opcion = messagebox.askyesno("Time Out", "Tiempo expirado ¿Desea continuar con el juego?")
                    if opcion:
                        self.__seconds = HoursToSec(self.__time[0],self.__time[1],self.__time[2])
                        self.__watchActivited = 1
                    else:
                        self.getSettingGame()
            hours,min,sec = secToHours(self.__seconds)
            for index in range(len(self.__timeEntry)):
                    self.__timeEntry[index].config(state="normal")
                    self.__timeEntry[index].delete(0,'end')
            self.__timeEntry[0].insert(0,str(hours))
            self.__timeEntry[1].insert(0,str(min))
            self.__timeEntry[2].insert(0,str(sec))
            for index in range(len(self.__timeEntry)):
                    self.__timeEntry[index].config(state="disabled")
        self.__timeEntry[0].after(1000, self.startWatch)