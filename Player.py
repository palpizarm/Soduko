import sys


class Player:
    __name = ""
    __time = ""

    def __init__(self, pName):
        self.__name = pName

    def getName(self):
        return self.__name__

    def getTime(self):
        return self.__time

    def setTime(self, pTime):
        self.__time = pTime