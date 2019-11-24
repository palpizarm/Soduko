import sys
import tkinter as tk
import webbrowser
sys.path.append("..\images")
sys.path.append("..\commons")


from Game import *
from SettingGame import *
import Constants as c
from loadImages import *

"""
Method of de main menu
"""


def menu():
    """
    create a menu of the window
    """
    toolbar_menu = tk.Menu(main)
    main.config(menu=toolbar_menu)
    toolbar_menu.add_command(label="START GAME", command=startGame)
    toolbar_menu.add_command(label="CONFIGURE", command=configure)
    toolbar_menu.add_command(label="HELP", command=help)
    toolbar_menu.add_command(label="ABUT", command= about)
    toolbar_menu.add_command(label="EXIT", command=main.destroy)


def startGame():
    """
    Call the game instance
    """
    Game(main)


def configure():
    """
    Show the options to personalize the game
    """
    settingFrame = SettingGame(main)
    del settingFrame




def about():
    """
    Show the popup window with the information of application 
    """
    aboutPanel = tk.Toplevel(main)
    aboutPanel.focus_force()
    aboutPanel.transient(main)
    aboutPanel.grab_set()
    aboutPanel.title("About")
    aboutPanel.config(bg="gray")
    aboutPanel.geometry("{}x{}+{}+{}".format(400,
                                        200,
                                        400,
                                        20))
    aboutPanel.resizable(0,0)
    tk.Label(master=aboutPanel,
            text= "SUDOKU GAME \n visit the git repository to get more information \n",
            bg =  "gray",
            fg = "white").pack()
    btAyuda = tk.Button(master=aboutPanel,
                    text="GitHub repository",
                    bg= "brown",
                    fg= "white",
                    command = openRepository).pack()

def openRepository():
    """
    Open the repository of this project
    """
    webbrowser.open_new("https://github.com/palpizarm/Soduko")


def help():
    """
    Show the window to go the user manual
    """
    helpPanel = tk.Toplevel(main)
    helpPanel.focus_force()
    helpPanel.transient(main)
    helpPanel.grab_set()
    helpPanel.title("Help")
    helpPanel.config(bg="gray")
    helpPanel.geometry("{}x{}+{}+{}".format(400,
                                        200,
                                        400,
                                        20))
    helpPanel.resizable(0,0)
    tk.Label(master=helpPanel,
            text="Press the below button to get help\n\n",
            bg = "gray",
            fg = "white").pack()
    btHelp = tk.Button(master=helpPanel,
                        text="Open User Manual",
                        bg= "brown",
                        fg= "white",
                        command = openManual).pack()


def openManual():
    """
    Open the user manual
    """
    webbrowser.open_new(r'manual _de_usuario_sudoku.pdf')


"""""""""""""""""""""""""""""
MAIN WINDOW
"""""""""""""""""""""""""""""
main = tk.Tk()

"""
Application laucher
"""
main.title("SUDOKU")
main.geometry("{}x{}+{}+{}".format(c.SUDOKU_WEIGTH, c.SUDOKU_HEIGHT,
                                    c.FRAME_X, c.FRAME_Y))
main.resizable(width=False, height=False)
#bgImage = tk.PhotoImage(file='\\images\\menubg.png')

menu()
loadImages()
main.mainloop()