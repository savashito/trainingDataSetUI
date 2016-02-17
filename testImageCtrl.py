import imageCtrl
from projectCtrl import getProject
from marsSchema import initDB
import imageUtil
import cropCtrl

initDB()

project = getProject('Craters')
name ="stinkbug.png"
path = "testImages"
imageData,imageInfo = imageCtrl.getImage(name,project)
rec = (0,0,100,100)
# crop = cropCtrl.insertCrop(name+"_crop_0",imageInfo,rec)
cropData,cropInfo = cropCtrl.saveCrop(project,imageInfo,imageData,rec)
print cropData
print cropInfo.src
# image = imageCtrl.getImage("stinkbug.png",project)
# print "crop name "+crop.src
# print imageInfo.src
# print imageData


# img,name = imageUtil.loadImage('testImages/stinkbug.png')
# imageCtrl.saveImage(project,img,name,0)