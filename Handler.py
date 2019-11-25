
import ast

from Games import *
from Player import *
import Constants as c


class Handler:
    """
    Controller the game and logical functions
    """
    __currentGame = None
    __currentLevel = None

    def __init__(self):
        """
        Constructor of the instance
        """
        self.__games = Games()
        self.__gamesLevel = dict()
        self.__bestPlayers = dict()
        self.loadBestPlayers()
        self.saveBestPlayers()
    

    def setLevel(self, level):
        """
        To get the games of a level of the player
        """
        self.__currentLevel = level-1
        self.__gamesLevel = self.__games.getLevelGames(self.__currentLevel).copy()


    def chooseRandomGames(self):
        """
        Choose a random game from dictionary
        """
        if len(self.__gamesLevel) == 0:
            self.__gamesLevel = self.__games.getLevelGames(self.__currentLevel)
        keys = []
        for key in self.__gamesLevel.keys():
            keys.append(key)
        game = random.choice(keys)
        self.__currentGame = self.__gamesLevel.pop(game)


    def checkBestPlayers(self, player):
        """
        Check the dictionary to look if a this players is best than one in the top
        """
        

    def getBestPlayersToTop(self):
        """
        Save the best players of three levels in a list to show in a top frame
        """
        bestPlayers = []
        for key in self.__bestPlayers:
            level = []
            for player in self.__bestPlayers[key]:
                elemento = player.getName() , secToHours(player.getTime())
                level.append(elemento)
            bestPlayers.append(level)
        return bestPlayers


    def saveBestPlayers(self):
        """
        Save the best players in the file
        """
        file = open('sudoku2019top10.dat', 'w+')
        for key in self.__bestPlayers:
            file.write('[')
            for player in self.__bestPlayers[key]:
                file.write(player.saveData())
            file.write(']\n')

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
        self.__bestPlayers[0] = list()
        self.__bestPlayers[1] = list()
        self.__bestPlayers[2] = list()
        for player in easyLevel:
            self.__bestPlayers[0].append(Player(player[0],player[1]))
        for player in normalLevel:
            self.__bestPlayers[1].append(Player(player[0],player[1]))
        for player in hardLevel:
            self.__bestPlayers[2].append(Player(player[0],player[1]))



def secToHours(time):
    """
    Convert seconds in hours format
    """
    hours = time//3600
    time %= 3600
    minutes = time//60
    time %= 60
    return str(hours)+":"+str(minutes)+":"+str(time)