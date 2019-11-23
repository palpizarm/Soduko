from PIL import Image, ImageTk
import Constants as c

def loadImages():
    """
    Load the images of the 4th option of fill in the array
    """
    for index in range(9):
        img = Image.open("../view/images/ball"+str(index + 1)+".png")
        pyimg = ImageTk.PhotoImage(img)
        c.MATRIX_POOL_BALLS.append(pyimg)
