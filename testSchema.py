import marsSchema
import imageCtrl
from Tkinter import Tk
from tkFileDialog import askopenfilename

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename(message="Load an image",initialdir="/Users/rodrigosavage/Documents/software/python/dbTutorial/marsML") # show an "Open" dialog box and return the path to the selected file
path,name = filename.split(":")



# marsSchema.init()

# project = projectCtrl.create("Mars craters")
# images = imageCtrl.createTestImages(project)
# imageCtrl.insertImages(images)
# imageCtrl.retrieveImages()