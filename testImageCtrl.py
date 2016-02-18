import imageCtrl
from projectCtrl import getProject
from marsSchema import initDB
import imageUtil
import cropCtrl
import classCtrl
import exampleCtrl

initDB()

project = getProject('Craters')
# l,clases = classCtrl.listClassesName(project)
# print l
name ="stinkbug.png"
path = "testImages"
imageData,imageInfo = imageCtrl.getImage(name,project)
c = classCtrl.getClass("Craters")
# exampleCtrl.insertExample(c,imageInfo,"Bark.png",[0,0,10,10])
print c.id
print exampleCtrl.listExamples(c)
# exampleCtrl.saveExample(c,project,imageInfo,[0,0,10,10],imageData)
data,example = exampleCtrl.getExample(project,"Craters_3")
print data
print example.src
# print c.name
'''
name ="stinkbug.png"
path = "testImages"
imageData,imageInfo = imageCtrl.getImage(name,project)
rec = (0,0,100,100)
# crop = cropCtrl.insertCrop(name+"_crop_0",imageInfo,rec)
cropData,cropInfo = cropCtrl.saveCrop(project,imageInfo,imageData,rec)
print cropData
print cropInfo.src

'''
# image = imageCtrl.getImage("stinkbug.png",project)
# print "crop name "+crop.src
# print imageInfo.src
# print imageData


# img,name = imageUtil.loadImage('testImages/stinkbug.png')
# imageCtrl.saveImage(project,img,name,0)