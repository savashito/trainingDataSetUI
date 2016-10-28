import exampleCtrl
import projectCtrl 
import classCtrl
import imageCtrl
import cropCtrl
import imageUtil
import craterCtrl
import numpy as np
from sklearn.cross_validation import train_test_split
import mlUtil.mlUtil as mlUtil
from os import sep
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from scipy.misc import imresize
from debugUtil import debug

import pdb;
import scalarCtrl

import scipy


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
		_class = classCtrl.getClass("craters")
		size = self.sizes[sizeIndex]
		print "----------------------------------------"
		print "image serch on "+ imageInfo.src
		lCraterInfo,listCratersImg,listCraterIdentifier  =  exampleCtrl.getExamplesFromImage(project,_class,size,imageInfo)
		# print "zac zac "+str(np.array(listCratersImg).shape)
		listBackgroundInfo,listBackgroundImg,listBackIdentifier = self.getBackgroundExamples(size)
		# print "barc barc "+str(len(listBackIdentifier))
		debug("Found %d examples of craters"%len(listCraterIdentifier))
		debug("Found %d examples of background"%len(listBackIdentifier))
		# debug("Found %d examples of background"%len(listBackgroundInfo))
		# exit()
		# return
		y = mlUtil.toClassSpace(listCraterIdentifier + listBackIdentifier) #  
		x = listCratersImg + listBackgroundImg
		return y,x,lCraterInfo+listBackgroundInfo

	def getBackgroundExamples(self,size):
		classBackground = classCtrl.getClass("background")
		classDunes = classCtrl.getClass("dunes")
		classSat = classCtrl.getClass("craterSaturation")
		listBackgroundInfo1,listBackgroundImg1,listBackIdentifier  =  exampleCtrl.getExamplesFromImage(self.project,classBackground,size,self.imageInfo)
		nB = len(listBackIdentifier)
		listBackgroundInfo2,listBackgroundImg2,listBackIdentifier  =  exampleCtrl.getExamplesFromImage(self.project,classDunes,size,self.imageInfo)
		nD = len(listBackIdentifier)
		listBackgroundInfo3,listBackgroundImg3,listBackIdentifier  =  exampleCtrl.getExamplesFromImage(self.project,classSat,size,self.imageInfo)
		nS = len(listBackIdentifier)
		listBackIdentifier = np.ones(nB+nD+nS)+1
		# print listBackIdentifier
		return listBackgroundInfo1+listBackgroundInfo2+listBackgroundInfo3,listBackgroundImg1+listBackgroundImg2+listBackgroundImg3,listBackIdentifier.tolist()

	def getExamples(self,sizeIndex):
		imagesName = self.listImages()
		X_a = []
		listExamplesClass_a = []
		# print imagesName

		orImageInfo = self.imageInfo
		# pdb.set_trace()
		print "---------------------------"
		for imageName in imagesName:
			# set the correct scaler for the image
			self.setImage(imageName)
			listExamplesClass,examplesData,examplesInfo = self.getExamplesFromImage(sizeIndex)
			if(len(examplesInfo)>0):
				# print "exampleData "+str(examplesData)
				print len(examplesInfo),np.array(examplesData).shape
				# exit()
				
				X = scalarCtrl.imageTransformation(self,sizeIndex,examplesData) #flatenImagesList(examplesData)
				print "XSHape"
				print np.array(X).shape
				# X = self.normalize(sizeIndex,flatExamplesData)
				X_a.extend(X)
				listExamplesClass_a.extend(listExamplesClass)
				debug ("Running total examples %d "%len(listExamplesClass_a))
				print "----------------"
		X_a,listExamplesClass_a = np.array(X_a),np.array(listExamplesClass_a)
		# restore image
		# the user selected an image before
		if(orImageInfo!=None):
			self.setImage(orImageInfo.src)
		return X_a,listExamplesClass_a
		


	def getTrainTestSplit(self,size):
		if (self.X_train[size] == None ):
			images,target = self.getExamples(size)
			X_train, X_validation, y_train, y_validation = train_test_split(images,target,test_size=0.20, random_state=42)
			return X_train, X_validation, y_train, y_validation 


		
	def getAllWindowsFromImage(self,sizeIndex):
		size = self.sizes[sizeIndex]
		# if(self.imageData==None):
		self.loadImage()
		return scalarCtrl.getAllWindowsFromImage(size,self.imageData)
	def normalize(self,sizeIndex,examples):
		# print np.array(examples).shape
		# return self.scaler[sizeIndex].transform(examples)
		return examples # self.scaler[sizeIndex].transform(examples)




	def getCropWindow(self,sizeIndex,x,y,testCropData=None):
		#flatWindow = self.getCropWindow_raw(sizeIndex,x,y,testCropData)
		#X = self.normalize(sizeIndex,flatWindow)
		size = self.sizes[sizeIndex]
		window = scalarCtrl.getWindowFromImageTransform(size,x,y,self.cropDataGray).reshape(1, -1)
		return window #self.normalize(sizeIndex,window)
		# remember to normilize each window extracted
		
	# update the scalar for the current image transformation
	def updateScalar(self,recalc=False):

		self.scaler = imageCtrl.getScaler(self.imageInfo)
		print self.scaler
		print recalc
		# exit()
		if(self.scaler == None or recalc):
			# debug( self.imageData)
			if(self.imageData==None):
				self.loadImage(None)
			# calculate the scaler for the image
			self.scaler = scalarCtrl.calculateScalerForImage(self.sizes,self.imageDataGray)
			imageCtrl.saveScaler(self.imageInfo,self.scaler)
	def safeDeleteImage(self):
		# _class = classCtrl.getClass("craters")
		# exit()
		# examplesInfo,examplesData,listExamplesClass = self.getExamplesFromImage(0)
		# print "there are " + str (len(examplesInfo))+"examples"
		self.deleteAllExamplesFromImage()
		# delete the crops
		cropCtrl.deleteCropsFromImage(self.project,self.imageInfo)
		imageCtrl.deleteImageBySrc(self.imageInfo.src)	
		debug("Succesfully deleted "+self.imageInfo.src)	
	def getCraters(self):
		return craterCtrl.getCraters()
		
	def insertCrater(self,pds,crater,bumps):
		print "inserting crater",crater,bumps
		return craterCtrl.insertCrater(self.imageInfo,pds,crater,bumps)
	def saveCropForGPU(self,testObj=None):
		if(testObj!=None):
			self.imageDataGray = testObj
			self.cropInfo = {"src":"test.png"}
		w,h = self.imageDataGray.shape
		print w,h
		cudaCores = 1024+512
		nW = w/cudaCores
		nExtraW = nW+1
		extraW = cudaCores-(w-nW*cudaCores)
		print nW,extraW
		# return
		while(nW>0):
			
			# print self.imageDataGray[cudaCores*0:cudaCores*1,0:cudaCores]
			# print self.imageDataGray[cudaCores*1:cudaCores*2,0:cudaCores]
			img = self.imageDataGray[cudaCores*(nW-1):cudaCores*nW,0:cudaCores]
			imageUtil.saveRawFloatImage(img,"%s_%d.dat"%(self.imageInfo.src,nW),"cropsForGPU")
			# print self.imageDataGray[cudaCores*3-extraW:cudaCores*4-extraW,0:cudaCores]

			nW-=1
		if(extraW):
			img = self.imageDataGray[cudaCores*(nExtraW-1)-extraW:cudaCores*nExtraW-extraW,0:cudaCores]
			imageUtil.saveRawFloatImage(img,"%s_%d.dat"%(self.imageInfo.src,nExtraW),"cropsForGPU")
	def getGPUCrops(self):
		w,h = self.imageDataGray.shape
		print w,h
		cudaCores = 1024+512
		nW = w/cudaCores
		nH = h/cudaCores
		# nExtraW = nW+1
		# extraW = cudaCores-(w-nW*cudaCores)

		# print nW,extraW
		return range(nW+1),range(nH+1)
	def getGPUCrop(self,indexX,indexY,dtm=False):
		if(dtm):
			img = self.dtm
		else:
			img = self.imageDataGray

		imgCrop = None
		w,h = img.shape
		# print w,h
		cudaCores = 1024+512
		nW = w/cudaCores
		nH = h/cudaCores
		nExtraW = nW+1
		nExtraH = nH+1

		extraW = cudaCores-(w-nW*cudaCores)
		extraH = cudaCores-(h-nH*cudaCores)
		xStart,xEnd = 0,0
		# print nW,extraW
		if(indexX<nW):
			xStart,xEnd = cudaCores*(indexX),cudaCores*(indexX+1)
		elif(extraW):
			xStart,xEnd = cudaCores*(nExtraW-1)-extraW,cudaCores*nExtraW-extraW

		if(indexY<nH):
			yStart,yEnd = cudaCores*(indexY),cudaCores*(indexY+1)
		elif(extraH):
			yStart,yEnd = cudaCores*(nExtraH-1)-extraH,cudaCores*nExtraH-extraH
		return img[xStart:xEnd,yStart:yEnd]

	# def getGPUCrop(self,index,dtm=False):
	# 	if(dtm):
	# 		img = self.dtm
	# 	else:
	# 		img = self.imageDataGray

	# 	imgCrop = None
	# 	w,h = img.shape
	# 	# print w,h
	# 	cudaCores = 1024+512
	# 	nW = w/cudaCores
	# 	nExtraW = nW+1
	# 	extraW = cudaCores-(w-nW*cudaCores)
	# 	# print nW,extraW
	# 	if(index<nW):
	# 		imgCrop = img[cudaCores*(index):cudaCores*(index+1),0:cudaCores]
	# 		# imageUtil.saveRawFloatImage(img,"%s_%d.dat"%(self.imageInfo.src,index),"cropsForGPU")
	# 	elif(extraW):
	# 		imgCrop = img[cudaCores*(nExtraW-1)-extraW:cudaCores*nExtraW-extraW,0:cudaCores]
	# 		# imageUtil.saveRawFloatImage(img,"%s_%d.dat"%(self.imageInfo.src,nExtraW),"cropsForGPU")
	# 	return imgCrop
		# return
		# imageUtil.saveRawFloatImage(self.cropDataGray,"meow_%d.dat"%nW,"outputCrops")
		

		# print self.cropDataGray.shape

	def deleteAllExamplesFromImage(self):
		exampleCtrl.deleteAllExamplesFromImage(self.project,self.imageInfo)
	def setCropAsMainImage(self):
		# we have self.currentImage
		self.cropInfo = self.imageInfo
		self.cropData = self.imageData
		self.cropDataGray = self.imageDataGray

	##########
	def loadImage(self,name):
		src = name
		if(src==None):
			src = self.imageInfo.src
		debug("Loading image "+src)
		if(name==None):
			self.imageData,self.imageInfo = imageCtrl.getImage(src,self.project)
		else:
			self.imageData,self.imageInfo = imageUtil.loadImage(src)
		self.imageDataGray = scalarCtrl.toGrayScale(self.imageData)
		# print "imageInfo",self.imageInfo
		# exit
		return self.imageData
	def scaleImageAndDTM(self,frac = 1.0/3.0):
		self.imageDataGray = scipy.misc.imresize(self.imageDataGray, frac)
		self.dtm = scipy.misc.imresize(self.dtm, frac)*frac

	def loadDTM(self,dtmData):

		self.dtm = dtmData
	def setImage(self,imageName):
		self.imageInfo = self.imagesInfo[imageName]
		self.updateScalar(False)
	def setCropRawDataGray(self,cropDataGray):
		self.cropInfo = self.imageInfo
		self.cropData = cropDataGray
		self.cropDataGray = cropDataGray
	def setCrop(self,cropName):
		self.cropInfo = self.cropsInfo[cropName]
		self.updateScalar()
	def loadCrop(self):
		self.cropData = cropCtrl.getCrop(self.project,self.imageInfo,self.cropInfo)
		self.cropDataGray = scalarCtrl.toGrayScale(self.cropData)
		# print self.cropDataGray.dtype
		# print self.cropData.dtype
		# exit()
		return self.cropData
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
	def displayImage(self):
		fig, ax = plt.subplots()
		ax.imshow(self.cropData)
		plt.title(self.cropInfo.src)
		plt.show()
	
	def displayImage(self,crop,name,isGray=False,lbl_colorbar=['%f','%f']):
		fig, ax = plt.subplots()
		cmap='jet_r'
		if(isGray):
			cmap='Greys_r'
		cax = ax.imshow(crop,cmap=cmap)
		plt.title(name)
		plt.xlabel('[m]')
		plt.ylabel('[m]')
		addColorBar(crop,fig,cax,lbl_colorbar)

	def show(self):
		plt.show()

	def displayCrop(self,heatmap,save_name=None,title="SVM creater probability distribution",suptitle=""):
		# print "Crop is "+self.cropInfo.src
		# print self.cropData.shape
		fig, ax = plt.subplots()
		ones = np.ones( heatmap.shape)
		print heatmap.shape,ones.shape
		heatmapAlpha = np.array([1.0*ones,0*ones,0*ones,heatmap*0.4])
		heatmapAlpha = imresize(heatmapAlpha,self.cropData.shape)
		# plt.figure()
		print heatmapAlpha.shape
		ax.imshow(self.cropData,cmap='Greys_r')
		cax = ax.imshow(heatmapAlpha,cmap='afmhot_r')
		addColorBar(heatmapAlpha,fig,cax,lbl_colorbar=['%0.1f','%0.1f'])
		plt.xlabel('[m]')
		plt.ylabel('[m]')
		plt.title(title + "\n"+suptitle)
		# plt.suptitle(suptitle)
		if(save_name!=None):
			plt.savefig(save_name+".svg")
			plt.savefig(save_name+".png")


def addColorBar(crop,fig,cax,lbl_colorbar):
	if(lbl_colorbar!=None):
		m = np.min(crop)
		M = np.max(crop)
		print "range: (%f,%f)"%(m,M)
		cbar = fig.colorbar(cax, ticks=[m,M])
		a = lbl_colorbar
		cbar.ax.set_yticklabels([a[0]%m,a[1]%M ])  # vertically oriented colorbar





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