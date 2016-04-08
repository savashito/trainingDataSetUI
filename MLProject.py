import exampleCtrl
import projectCtrl 
import classCtrl
import imageCtrl
import cropCtrl
import imageUtil
import numpy as np
from sklearn.cross_validation import train_test_split
import mlUtil.mlUtil as mlUtil
from os import sep
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
		projectCtrl.updateOutputImageFolder(self.project)
		self.X_train, self.X_validation, self.y_train, self.y_validation = None,None,None,None

	def getExamples_raw(self,sizeIndex):
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
		
		y = mlUtil.toClassSpace(listCraterIdentifier + listBackIdentifier)
		x = listCratersImg + listBackgroundImg
		# print y
		# exit()
		
		return y,x,lCraterInfo+listBackgroundInfo
	def getExamplesFromCrop(self,sizeIndex):
		_class = classCtrl.getClass("craters")
		size = self.sizes[sizeIndex]
		l,listExamples,listClassIdentifier = exampleCtrl.getExampleSizeCrop(self.project,_class,size,self.cropInfo)
		print len(l)
		exit()
	def rotateExamplesCrater(self):
		sizes = classCtrl.getExampleSizes(None)
		for sizeIndex in range(len(sizes)):
			examplesClass,examplesData,examplesInfo = self.getExamples_raw(sizeIndex)
			for i in range(len(examplesInfo)):
				exampleData = examplesData[i]
				exampleInfo = examplesInfo[i]
				exampleClass = examplesClass[i]
				img90 = imageUtil.rotateImage(np.array(exampleData),90.0)
				img180 = imageUtil.rotateImage(np.array(exampleData),180.0)
				img270 = imageUtil.rotateImage(np.array(exampleData),270.0)
				exampleCtrl.saveExampleTransformed(exampleInfo,img90,self.project)
				exampleCtrl.saveExampleTransformed(exampleInfo,img180,self.project)
				exampleCtrl.saveExampleTransformed(exampleInfo,img270,self.project)
			# print examplesInfo

	def getExamples(self,sizeIndex):
		listExamples,examplesImg,examplesInfo = self.getExamples_raw(sizeIndex)
		
		listExamplesImages = flatenImagesList(examplesImg)
		
		# Normalize example!
		scaler = StandardScaler()
		X = scaler.fit_transform(listExamplesImages)
		self.scaler[sizeIndex] = scaler
		return X,listExamples

	def getTrainTestSplit(self,size):
		if (self.X_train == None ):
			images,target = self.getExamples(size)
			self.X_train, self.X_validation, self.y_train, self.y_validation = train_test_split(images,target,test_size=0.20, random_state=42)


		return self.X_train, self.X_validation, self.y_train, self.y_validation

	def getDataNormalizer(self):
		return self.scaler
	def setDataNormalizer(self,scaler):
		self.scaler = scaler

	# adds 3 rotated examples per sample (0,90,180,270)
	def getRotatedExamples(self,sizeIndex):
		listExamples,examplesImg,examplesInfo = self.getExamples_raw(sizeIndex)

		# print examplesImg[0].shape
		rotatedListExamples, rotatedImg = [],[]
		# plt.show()
		for i in range(len(examplesImg)):
			img = examplesImg[i]
			img90 = imageUtil.rotateImage(np.array(examplesImg[i]),90.0)
			img180 = imageUtil.rotateImage(np.array(examplesImg[i]),180.0)
			img270 = imageUtil.rotateImage(np.array(examplesImg[i]),270.0)
			rotatedImg.append(img)
			rotatedImg.append(img90)
			rotatedImg.append(img180)
			rotatedImg.append(img270)
			rotatedListExamples.append(listExamples[i])
			rotatedListExamples.append(listExamples[i])
			rotatedListExamples.append(listExamples[i])
			rotatedListExamples.append(listExamples[i])
		# rotatedImg = np.array(rotatedImg)
		# print "wof "+str(rotatedImg.shape)
		print rotatedImg[0].shape
		listExamplesImages = flatenImagesList(rotatedImg)
		# normalize the images
		# print "wof "+str(listExamplesImages.shape)
		scaler = StandardScaler()
		# print "wofs"
		X = scaler.fit_transform(listExamplesImages)
		# print "wof"
		self.scaler[sizeIndex] = scaler
		# print "wof"

		return X,rotatedListExamples

		# imgRot = examplesImg[0] # imageUtilfg.rotateImageg(examplesImg[0],45)

		# fig, ax = plt.subplots()
		# ax.imshow( examplesImg[0])
		# fig, ax = plt.subplots()
		# ax.imshow( img90)
		# fig, ax = plt.subplots()
		# ax.imshow( img180)
		# fig, ax = plt.subplots()
		# ax.imshow( img270)
		# plt.show()

		# exit()
	def listImages(self):
		imagesName, self.images = imageCtrl.retrieveImages(self.project)
		return imagesName
	def setImage(self,imageName):
		# print imageName
		self.currentImage = self.images[imageName]
		name = imageName.split(sep)
		name = name[len(name)-1]
		print name
		# exit()
		# self.imageInfo = self.currentImage
		self.imageData,self.imageInfo = imageCtrl.getImage(name,self.project)

		# print self.imageData.shape
		# exit()
	def listCrops(self):
		cropsNames, self.crops = cropCtrl.retrieveCrops(self.project,self.currentImage)
		return cropsNames
	def setCropAsMainImage(self):
		# we have self.currentImage
		self.cropInfo = self.imageInfo
		self.cropData = self.imageData
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
		# scale the value!
		X = self.scaler[sizeIndex].transform(flatWindow)
		return X
	def getWindowSizes(self):
		return self.sizes
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

	# def selectImage(self,image):

	# def generateHeatMapFromImage(self,image,clf):
