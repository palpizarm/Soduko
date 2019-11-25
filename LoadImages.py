from PIL import Image, ImageTk
import Constants as c

def loadImages():
    """
    Load the images of the 4th option of fill in the array
    """
    images = []
    pilImg1 = Image.open("images/ball1.png")
    pilImg2 = Image.open("images/ball2.png")
    pilImg3 = Image.open("images/ball3.png")
    pilImg4 = Image.open("images/ball4.png")
    pilImg5 = Image.open("images/ball5.png")
    pilImg6 = Image.open("images/ball6.png")
    pilImg7 = Image.open("images/ball7.png")
    pilImg8 = Image.open("images/ball8.png")
    pilImg9 = Image.open("images/ball9.png")
    images.append(ImageTk.PhotoImage(pilImg1))
    images.append(ImageTk.PhotoImage(pilImg2))
    images.append(ImageTk.PhotoImage(pilImg3))
    images.append(ImageTk.PhotoImage(pilImg4))
    images.append(ImageTk.PhotoImage(pilImg5))
    images.append(ImageTk.PhotoImage(pilImg6))
    images.append(ImageTk.PhotoImage(pilImg7))
    images.append(ImageTk.PhotoImage(pilImg8))
    images.append(ImageTk.PhotoImage(pilImg9))
    c.MATRIX_POOL_BALLS = images
    return images
