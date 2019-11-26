import sys


class Player:
    __name = ""
    __time = ""

    def __init__(self, pName):
        self.__name = pName


    def __init__(self, pName, pTime):
        self.__name = pName
        self.__time = pTime
    

    def getName(self):
        return self.__name


    def getTime(self):
        return self.__time

    
    def setTime(self, pTime):
        self.__time = pTime
    

    def saveData(self):
        """
        Give the format of the data
        """
        return '(\'' + str(self.__name) + '\',' + str(self.__time) + '),'