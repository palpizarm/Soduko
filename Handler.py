"""
Controller the game and logical functions
"""
import ast

from Games import *
from Player import *
import Constants as c


class Handler:
    """

    """

    def __init__(self):
        """
        Constructor of the instance
        """
        self.__games = Games()
        self.__bestPlayers = dict()
    

    def checkBestPlayers(self, player):
        """
        Check the dictionary to look if a this players is best than one in the top
        """
        

    def saveBestPlayers(self):
        """
        Save the best players in the file
        """
        file = open('sudoku2019top10.dat', 'r')


    def loadBestPlayers(self):
        """
        Load the games from file
        """
        file = open('sudoku2019top10.dat', 'r')
        easyLevel = file.readline()
        normalLevel = file.readline()
        hardLevel = file.readline()
        easyLevel = ast.literal_eval(easyLevel)
        normalLevel = ast.literal_eval(normalLevel)
        hardLevel = ast.literal_eval(hardLevel)
        self.__bestPlayers[0] = easyLevel
        self.__bestPlayers[1] = normalLevel
        self.__bestPlayers[2] = hardLevel
