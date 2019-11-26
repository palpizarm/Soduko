import random
import ast

"""
This class contains the differents kind of games
There are three levels
Easy
Normal
Hard
"""


class Games:
    __easyGames = None
    __normalGames = None
    __hardGames = None
    __levels = None

    def __init__(self):
        self.__easyGames = dict()
        self.__normalGames = dict()
        self.__hardGames = dict()
        self.__levels = [self.__easyGames,self.__normalGames,self.__hardGames]
        self.loadGames()


    def addGame(self, game, type):
        """
        Add a the dictinary the new game
        Parameters
        ---------
        game: list of list with a game \n
        type: int (0: easy, 1: normal, 2: hard)
        """
        self.__levels[type][len(self.__easyGames)+1] = game
    

    def getLevelGames(self, type):
        """
        Return the game of the type of the parameter
        """
        return self.__levels[type]


    def saveGames(self):
        """
        Save the all games in a file
        """
        file = open("sudoku2019games.dat","w+")
        file.write(str(self.__levels[0]) + "\n")
        file.write(str(self.__levels[1]) + "\n")
        file.write(str(self.__levels[2]))
        file.close()


    def loadGames(self):
        """
        Load the games from the file
        """
        file = open("sudoku2019games.dat","r")
        level = file.readline()
        self.__easyGames = ast.literal_eval(level)
        level = file.readline()
        self.__normalGames = ast.literal_eval(level)
        level = file.readline()
        self.__hardGames = ast.literal_eval(level)
        self.__levels = [self.__easyGames, self.__normalGames, self.__hardGames]