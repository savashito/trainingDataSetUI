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
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from scipy.misc import imresize
from debugUtil import debug

import scalarCtrl



class MLProject:
	def __init__(self,projName):
		# retrieve project
		self.project = projectCtrl.getProject(projName)
		self.imagesInfo,self.cropsInfo = None,None
		self.imageInfo,self.cropInfo = None,None
		self.imageData,self.cropData = None,None
		# self.currentImage = None
		self.sizes = classCtrl.getExampleSizes(None)
		noneSizeArray = [None,None,None,None]
		self.scaler = noneSizeArray
		projectCtrl.updateOutputImageFolder(self.project)
		self.X_train, self.X_validation, self.y_train, self.y_validation = noneSizeArray,noneSizeArray,noneSizeArray,noneSizeArray

	def getExamplesFromImage(self,sizeIndex):
		imageInfo = self.imageInfo
		project = self.project
		l,classes = classCtrl.listClassesName(project)
		classBackground = classCtrl.getClass("background")
		_class = classCtrl.getClass("craters")
		size = self.sizes[sizeIndex]
		lCraterInfo,listCratersImg,listCraterIdentifier  =  exampleCtrl.getExamplesFromImage(project,_class,size,imageInfo)
		listBackgroundInfo,listBackgroundImg,listBackIdentifier  =  exampleCtrl.getExamplesFromImage(project,classBackground,size,imageInfo)
		debug("Found %d examples of craters"%len(listCraterIdentifier))
		debug("Found %d examples of background"%len(listBackIdentifier))
		y = mlUtil.toClassSpace(listCraterIdentifier + listBackIdentifier) #  
		x = listCratersImg + listBackgroundImg
		return y,x,lCraterInfo+listBackgroundInfo



	def getExamples(self,sizeIndex):
		imagesName = self.listImages()
		X_a = []
		listExamplesClass_a = []
		print imagesName
		print "---------------------------"
		for imageName in imagesName:
			# set the correct scaler for the image
			self.setImage(imageName)
			listExamplesClass,examplesData,examplesInfo = self.getExamplesFromImage(sizeIndex)
			flatExamplesData = scalarCtrl.flatenImagesList(examplesData)
			X = self.normalize(sizeIndex,flatExamplesData)
			X_a.extend(X)
			listExamplesClass_a.extend(listExamplesClass)
			debug ("Running total examples %d "%len(listExamplesClass_a))
			print "----------------"
		X_a,listExamplesClass_a = np.array(X_a),np.array(listExamplesClass_a)
		return X_a,listExamplesClass_a
		


	def getTrainTestSplit(self,size):
		if (self.X_train[size] == None ):
			images,target = self.getExamples(size)
			X_train, X_validation, y_train, y_validation = train_test_split(images,target,test_size=0.20, random_state=42)
			return X_train, X_validation, y_train, y_validation 


		
	
	def normalize(self,sizeIndex,examples):
		return self.scaler[sizeIndex].transform(examples)




	def getCropWindow(self,sizeIndex,x,y,testCropData=None):
		#flatWindow = self.getCropWindow_raw(sizeIndex,x,y,testCropData)
		#X = self.normalize(sizeIndex,flatWindow)
		size = self.sizes[sizeIndex]
		window = scalarCtrl.getWindowFromImage(size,x,y,self.cropData)
		return self.normilize(sizeIndex,window)
		# remember to normilize each window extracted
		
	# update the scalar for the current image transformation
	def updateScalar(self):
		self.scaler = imageCtrl.getScaler(self.imageInfo)
		if(self.scaler == None):
			# calculate the scaler for the image
			self.scaler = scalarCtrl.calculateScalerForImage(self.sizes,self.imageData)
			imageCtrl.saveScaler(self.imageInfo,self.scaler)


	def setCropAsMainImage(self):
		# we have self.currentImage
		self.cropInfo = self.imageInfo
		self.cropData = self.imageData
	##########
	def loadImage(self):
		debug("Loading image "+self.imageInfo.src)
		self.imageData,self.imageInfo = imageCtrl.getImage(self.imageInfo.src,self.project)
	def setImage(self,imageName):
		self.imageInfo = self.imagesInfo[imageName]
		self.updateScalar()
	def setCrop(self,cropName):
		self.cropInfo = self.cropsInfo[cropName]
		self.updateScalar()
	def loadCrop(self):
		self.cropData = cropCtrl.getCrop(self.project,self.imageInfo,self.cropInfo)
	#############
	def listImages(self):
		imagesName, self.imagesInfo = imageCtrl.retrieveImages(self.project)
		return imagesName
	def listCrops(self):
		cropsNames, self.cropsInfo = cropCtrl.retrieveCrops(self.project,self.imageInfo)
		return cropsNames
	def getWindowSizes(self):
		return self.sizes
	def getWindowSize(self,size):
		return self.sizes[size],self.sizes[size]
	def getCropShape(self):
		return self.cropData.shape
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









			# print X_train.shape
			# print y_train.shape
			# self.X_train[size] = X_train
			# self.y_train[size] = y_train
			#, (X_validation), (y_train), (y_validation)
			# print self.X_train[size].shape,self.y_train[size].shape
		# return self.X_train[size], self.X_validation[size], self.y_train[size], self.y_validation[size]





		# Normalize example!
		# scaler = StandardScaler()
		# X = scaler.fit_transform(listExamplesImages)
		# self.scaler[sizeIndex] = scaler
		# print listExamplesClass_a.shape
		# print X_a.shape
		# print " Te amo <3 "
		# print "-----------------------------"
		# exit()





		# name = imageName.split(sep)
		# name = name[len(name)-1]
		# print name
		# self.imageInfo = self.currentImage

		# 
		# print "Image loaded: "+self.imageInfo.src
		# print "Image loaded: "+str(self.imageData.shape)

		# print self.imageData.shape
		# exit()


	# def getCrop(self):
	# 	return self.cropData[:,:,0]


# def toGrayScale(image):
# 	return image[:,0]

# def flatenImagesList(listImages):
# 	flatenList = []
# 	for image in listImages:
# 		s = len(image)
# 		flatImage = image.reshape(s*s,3)
# 		flatenImage = toGrayScale(flatImage)
# 		flatenList.append(flatenImage)
# 	return flatenList

# def extractLinearArray(cropData,x,y,size):
# 	return cropData[x:x+size,y]



	# def selectImage(self,image):

	# def generateHeatMapFromImage(self,image,clf):






	# def getDataNormalizer(self):
	# 	return self.scaler
	# def setDataNormalizer(self,scaler):
	# 	self.scaler = scaler





























































#####################################################
	# def getExamplesFromCrop(self,sizeIndex):
	# 	_class = classCtrl.getClass("craters")
	# 	size = self.sizes[sizeIndex]
	# 	l,listExamples,listClassIdentifier = exampleCtrl.getExampleSizeCrop(self.project,_class,size,self.cropInfo)

	# def getExamples_raw(self,sizeIndex):
	# 	# retrieve class from the project
	# 	project = self.project
	# 	l,classes = classCtrl.listClassesName(project)
	# 	print "clases are "+str(l)
	# 	# retrieve background object and craters
	# 	# for className in l:
	# 	classBackground = classCtrl.getClass("background")
	# 	_class = classCtrl.getClass("craters")
	# 	# self.sizes = classCtrl.getExampleSizes(_class)
	# 	# retrieve examples for that specific size 
	# 	size = self.sizes[sizeIndex]
	# 	lCraterInfo,listCratersImg,listCraterIdentifier  =  exampleCtrl.getExampleSize(project,_class,size)
	# 	listBackgroundInfo,listBackgroundImg,listBackIdentifier  =  exampleCtrl.getExampleSize(project,classBackground,size)
		
	# 	y = mlUtil.toClassSpace(listCraterIdentifier + listBackIdentifier)
	# 	x = listCratersImg + listBackgroundImg
	# 	# print y
	# 	# exit()
		
	# 	return y,x,lCraterInfo+listBackgroundInfo


	# def rotateExamplesCrater(self):
	# 	sizes = classCtrl.getExampleSizes(None)
	# 	for sizeIndex in range(len(sizes)):
	# 		examplesClass,examplesData,examplesInfo = self.getExamples_raw(sizeIndex)
	# 		for i in range(len(examplesInfo)):
	# 			exampleData = examplesData[i]
	# 			exampleInfo = examplesInfo[i]
	# 			exampleClass = examplesClass[i]
	# 			img90 = imageUtil.rotateImage(np.array(exampleData),90.0)
	# 			img180 = imageUtil.rotateImage(np.array(exampleData),180.0)
	# 			img270 = imageUtil.rotateImage(np.array(exampleData),270.0)
	# 			exampleCtrl.saveExampleTransformed(exampleInfo,img90,self.project)
	# 			exampleCtrl.saveExampleTransformed(exampleInfo,img180,self.project)
	# 			exampleCtrl.saveExampleTransformed(exampleInfo,img270,self.project)
	# 		# print examplesInfo
	# return X
	# def getRotatedExamples(self,sizeIndex):
	# 	listExamples,examplesImg,examplesInfo = self.getExamples_raw(sizeIndex)

	# 	# print examplesImg[0].shape
	# 	rotatedListExamples, rotatedImg = [],[]
	# 	# plt.show()
	# 	for i in range(len(examplesImg)):
	# 		img = examplesImg[i]
	# 		img90 = imageUtil.rotateImage(np.array(examplesImg[i]),90.0)
	# 		img180 = imageUtil.rotateImage(np.array(examplesImg[i]),180.0)
	# 		img270 = imageUtil.rotateImage(np.array(examplesImg[i]),270.0)
	# 		rotatedImg.append(img)
	# 		rotatedImg.append(img90)
	# 		rotatedImg.append(img180)
	# 		rotatedImg.append(img270)
	# 		rotatedListExamples.append(listExamples[i])
	# 		rotatedListExamples.append(listExamples[i])
	# 		rotatedListExamples.append(listExamples[i])
	# 		rotatedListExamples.append(listExamples[i])
	# 	listExamplesImages = flatenImagesList(rotatedImg)

	# 	# normalize the images
	# 	X = self.normalize(sizeIndex,listExamplesImages)
	# 	# scaler = StandardScaler()
	# 	# X = scaler.fit_transform(listExamplesImages)
	# 	# self.scaler[sizeIndex] = scaler

	# return X,rotatedListExamples