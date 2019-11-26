from PIL import Image, ImageTk
import ast
import numpy as np

from Games import *
from Player import *
import Constants as c


class Handler:
    """
    Controller the game and logical functions
    """
    __currentGame = None
    __currentLevel = None
    __gamePlayer = None
    __playerPlays = []
    __player = None

    def __init__(self):
        """
        Constructor of the instance
        """
        self.__games = Games()
        self.__gamesLevel = dict()
        self.__bestPlayers = dict()
        self.loadBestPlayers()
    

    def setLevel(self, level):
        """
        To get the games of a level of the player
        """
        self.__currentLevel = level-1
        self.__gamesLevel = self.__games.getLevelGames(self.__currentLevel).copy()


    def getGamePlayer(self):
        """
        Return the current game of the player
        """
        return self.__gamePlayer


    def chooseRandomGames(self):
        """
        Choose a random game from dictionary
        """
        self.__gamePlayer = []
        if len(self.__gamesLevel) == 0:
            self.__gamesLevel = self.__games.getLevelGames(self.__currentLevel)
        keys = []
        for key in self.__gamesLevel.keys():
            keys.append(key)
        game = random.choice(keys)
        self.__currentGame = self.__gamesLevel.pop(game)
        for row in self.__currentGame:
            self.__gamePlayer.append(row.copy())

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
            bestPlayers.append(level.copy())
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


    def addNumberToGame(self, pRow, pColumn, pNumber):
        """
        Check if is posible insert a number this row and column
        and insert the element
        """
        submatrix_row = (pRow//3)*3
        submatrix_column = (pColumn//3)*3
        row = submatrix_row
        column = submatrix_column
        if self.__currentGame[pRow][pColumn] != 0:
            return False, "No se puede remplazar el elemento(elemento fijo)"
        # Check if there is this number in the row and column 
        # and the sub-matrix 3x3
        for index in range(9):
            # check row and column
            if self.__gamePlayer[index][pColumn] == pNumber:
                return False, "El elemento se encuentra en la fila"
            if self.__gamePlayer[pRow][index] == pNumber:
                return False, "El elemento se encuentra en la columna"
            # check in the sub-matrix
            if column == submatrix_column+3:
                column = submatrix_column
                row += 1
            if self.__gamePlayer[row][column] == pNumber:
                return False,"El elemento ya se encuentra en la submatriz"
            column+=1
        self.__gamePlayer[pRow][pColumn] = pNumber
        if self.gameComplete():
            return True,"Complete"
        self.__playerPlays.append((pRow, pColumn))
        return True,""


    def addPlayerTop10(self, time):
        """
        Check the list of a player to look if better than the last one
        """
        self.__player.setTime(time)
        playersLevel = self.__bestPlayers[self.__currentLevel]
        for index in range(len(playersLevel)):
            if playersLevel[index].getTime() > time:
                playersLevel.insert(index, self.__player)
                break
        if len(playersLevel) > 10:
            playersLevel.pop(-1)
        self.saveBestPlayers()


    def removeLastMove(self):
        """
        Undo the last move
        """
        if len(self.__playerPlays) != 0:
            row,column = self.__playerPlays.pop(-1)
            self.__gamePlayer[row][column] = 0


    def setPlayer(self, pName):
        """
        Set the actual player
        """
        self.__player = Player(pName,0)


    def EraseGame(self):
        """
        Delete the player plays of the gamePlayer
        """
        self.__playerPlays = []
        self.__gamePlayer = self.__currentGame.copy()


    def gameComplete(self):
        """
        check gamePlayer to look if a complete
        """
        for row in range(9):
            for column in range(9):
                if self.__gamePlayer[row][column] == 0:
                    return False
        return True


    def solveSudoku(self):
        """
        Solve the current game
        """
        m = self.__gamePlayer
        if isinstance(m, list):
            m = np.array(m)
        elif isinstance(m, str):
            m = np.loadtxt(m, dtype=np.int, delimiter=",")
        rg = np.arange(m.shape[0]+1)
        while True:
            mt = m.copy()
            while True:
                d = []
                d_len = []
                for i in range(m.shape[0]):
                    for j in range(m.shape[1]):
                        if mt[i, j] == 0:
                            possibles = np.setdiff1d(rg, np.union1d(np.union1d(mt[i, :], mt[:, j]), mt[3*(i//3):3*(i//3+1), 3*(j//3):3*(j//3+1)]))
                            d.append([i, j, possibles])
                            d_len.append(len(possibles))
                if len(d) == 0:
                    break
                idx = np.argmin(d_len)
                i, j, p = d[idx]
                if len(p) > 0:
                    num = np.random.choice(p)
                else:
                    break
                mt[i, j] = num
                if len(d) == 0:
                    break
            if np.all(mt != 0):
                break
        print(mt)
        self.__gamePlayer = mt


    def saveCurrentGame(self):
        """
        return the current game
        """
        game = self.__gamePlayer.copy()
        plays = self.__playerPlays.copy()
        return game,plays


    def loadCurrentGame(self, game, plays, player):
        self.__gamePlayer = game.copy()
        self.__playerPlays.copy()
        self.__player = (player,0)


def secToHours(time):
    """
    Convert seconds in hours format
    """
    hours = time//3600
    time %= 3600
    minutes = time//60
    time %= 60
    return hours,minutes,time


def HoursToSec(hours, min, sec):
    """
    Convert in the hours, min and sec in seconds
    """
    seconds = hours*3600
    seconds += min*60
    seconds += sec
    return seconds