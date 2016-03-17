import exampleCtrl
import projectCtrl 
import classCtrl
import imageCtrl
import cropCtrl
import numpy as np

def toGrayScale(image):
	return image[:,0]

def flatenImagesList(listImages):
	flatenList = []
	for image in listImages:
		s = len(image)
		flatImage = image.reshape(s*s,3)
		flatenImage = toGrayScale(flatImage)
		flatenList.append(flatenImage)
	return flatenList

def extractLinearArray(cropData,x,y,size):
	return cropData[x:x+size,y]

import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from scipy.misc import imresize
class MLProject:
	def __init__(self,projName):
		# retrieve project
		self.project = projectCtrl.getProject(projName)
		self.images,self.crops = None,None
		self.currentImage = None
		self.sizes = classCtrl.getExampleSizes(None)
		self.scaler = [None,None,None,None]
	def getExamples(self,sizeIndex):
		# retrieve class from the project
		project = self.project
		l,classes = classCtrl.listClassesName(project)
		print "clases are "+str(l)
		# retrieve background object and craters
		# for className in l:
		classBackground = classCtrl.getClass("background")
		_class = classCtrl.getClass("craters")
		# self.sizes = classCtrl.getExampleSizes(_class)
		# retrieve examples for that specific size 
		size = self.sizes[sizeIndex]
		lCraterInfo,listCratersImg,listCraterIdentifier  =  exampleCtrl.getExampleSize(project,_class,size)
		listBackgroundInfo,listBackgroundImg,listBackIdentifier  =  exampleCtrl.getExampleSize(project,classBackground,size)

		listExamples = listCraterIdentifier + listBackIdentifier
		listExamplesImages = flatenImagesList(listCratersImg + listBackgroundImg)
		
		scaler = StandardScaler()
		X = scaler.fit_transform(listExamplesImages)
		self.scaler[sizeIndex] = scaler
		return X,listExamples
		
	def listImages(self):
		imagesName, self.images = imageCtrl.retrieveImages(self.project)
		return imagesName
	def setImage(self,imageName):
		self.currentImage = self.images[imageName]
	def listCrops(self):
		cropsNames, self.crops = cropCtrl.retrieveCrops(self.project,self.currentImage)
		return cropsNames
	def setCrop(self,cropName):
		self.cropInfo = self.crops[cropName]
		self.cropData = cropCtrl.getCrop(self.project,self.currentImage,self.cropInfo)
	def getCropShape(self):
		return self.cropData.shape
	def getCropWindow(self,size,x,y,testCropData=None):
		sizeIndex = size
		size = self.sizes[size]
		cropData = testCropData if testCropData!=None else self.cropData
		outWindow = []
		for i in range(size):
			outWindow.extend(extractLinearArray(cropData,x,y+i,size))
		# scaler = StandardScaler()
		flatWindow = np.float64(toGrayScale( np.array(outWindow)).reshape(1, -1))
		X = self.scaler[sizeIndex].transform(flatWindow)
		return X
	def getWindowSize(self,size):
		return self.sizes[size],self.sizes[size]
	def getCrop(self):
		return self.cropData[:,:,0]
	def displayCrop(self,heatmap):
		# print "Crop is "+self.cropInfo.src
		# print self.cropData.shape
		fig, ax = plt.subplots()
		ones = np.ones( heatmap.shape)
		print heatmap.shape,ones.shape
		heatmapAlpha = np.array([1.0*ones,0*ones,0*ones,heatmap*0.4])
		heatmapAlpha = imresize(heatmapAlpha,self.cropData.shape)
		# plt.figure()
		print heatmapAlpha.shape
		ax.imshow(self.cropData)
		ax.imshow(heatmapAlpha)
		plt.title(self.cropInfo.src)
		plt.show()

	# def selectImage(self,image):

	# def generateHeatMapFromImage(self,image,clf):
