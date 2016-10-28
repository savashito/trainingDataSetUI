import numpy as np
from debugUtil import debug
from mlUtil.hogTransform import hog
# import pdb;

from sklearn.preprocessing import StandardScaler
import cv2

# runHOG = False
runHOG = True

def getFeatureMethod():
	if(runHOG):
		return "HOG"
	else:
		return "INTENSITY"

def toGrayScale(image):
	return cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
	# return image[:,:,0].astype(float)

def imageTransformation(mlProject,sizeIndex,data):
	if(runHOG):
		flatData=hogTransformList(data)
	else:
		flatData = cnnRawTransform(data)# flatenImagesList(data)
	# flatData=hogTransformList(data)
	# X = self.normalize(sizeIndex,flatData)
	return flatData

def getWindowFromImageTransform(size,x,y,imageData):
	# raise IndexError("You callm e")
	window = getWindowFromImage(size,x,y,imageData)
	if(runHOG):
		window = hog(window)
	else:
		s = len(window)
		window = window.reshape(s*s)
	return window
def hogTransformList(listImages):
	listHistograms = []
	for image in listImages:
		listHistograms.append(hog(toGrayScale(image)))

	return listHistograms
def cnnRawTransform(listImages):
	listGrayImages = []
	for image in listImages:
		listGrayImages.append(toGrayScale(image))
	return listGrayImages

def flatenImagesList(listImages):
	flatenList = []
	i = 0
	for image in listImages:
		if(image ==None):
			print i
			i=i+1
			continue
		#print i
		s = len(image)

		flatImage = toGrayScale(image).reshape(s*s)
		# flatenImage = toGrayScale(flatImage)
		flatenList.append(flatImage)
		i=i+1
	# print i
	# exit()
	return flatenList

def extractLinearArray(cropData,x,y,size):
	return cropData[x:x+size,y]

def getAllWindowsFromImage(size,imageData):
	dx = size
	listExamplesImages = []
	s = imageData.shape
	W,H = s[0],s[1]
	mapW,mapH = W/size,H/size

	for y in range(mapH):
		for x in range(mapW):
			xWindow,yWindow = x*dx,y*dx
			window = getWindowFromImage(size,xWindow,yWindow,imageData)
			listExamplesImages.append(window)
	return listExamplesImages

def calculateScalerForImage(sizes,imageData):
	scalers = range(len(sizes))

	for sizeIndex in range(len(sizes)):
		size = sizes[sizeIndex]
		print size
		listExamplesImages = getAllWindowsFromImage(size,imageData)
		# pdb.set_trace()
		listExamplesImages = np.array(listExamplesImages)
		print listExamplesImages.shape
		listExamplesImages = listExamplesImages.reshape((-1,size*size))
		print listExamplesImages.shape

		scaler = StandardScaler().fit(listExamplesImages)

		scalers[sizeIndex] = scaler
	return scalers
		# print listExamplesImages.shape
		# x_Trans = scaler.transform(listExamplesImages)
		# mean = x_Trans.mean(axis=0)

		# debug ("mean.shpae "+str(mean.shape))
		# debug ("std "+str(x_Trans.std(axis=0)))
		# print listExamplesImages[0].shape
		# xt = scaler.transform(listExamplesImages[0].reshape(1,-1))
		# print xt 
		# debug ("mean "+str(mean))
		# debug ("mean "+str(x_Trans.mean(axis=1)))
		# debug ("std "+str(x_Trans.std(axis=0)))
		# debug ("std "+str(x_Trans.std(axis=1)))
		# exit()

def getWindowFromImageFlat(size,x,y,imageData):
	outWindow = []
	w,h,d= imageData.shape
	if(size+x > w):
		raise IndexError("Image index out off bounds size+x < w",size,x,w)
	if(size+y >h):
		raise IndexError("Image index out off bounds size+y > h",size,y,h)

	for i in range(size):
		outWindow.extend(extractLinearArray(imageData,x,y+i,size))
	w = np.float64(toGrayScale( np.array(outWindow)))
	return w

def getWindowFromImage(size,x,y,imageData):
	# raise IndexError("You callm e")
	return imageData[x:x+size,y:y+size] #.reshape(size*size)


def getWindowFromImageOld(size,x,y,imageData):
	outWindow = []
	w,h,d= imageData.shape
	if(size+x > w):
		raise IndexError("Image index out off bounds size+x < w",size,x,w)
	if(size+y >h):
		raise IndexError("Image index out off bounds size+y > h",size,y,h)
	# print w,h
	# if(size)
	

	for i in range(size):
		outWindow.extend(extractLinearArray(imageData,x,y+i,size))


	w = np.float64(toGrayScale( np.array(outWindow)))
	# return w
	flatWindow = w.reshape(1, -1)


	if(len(flatWindow.shape)!=1):
		# print "reshaping"
		flatWindow = flatWindow.T[:,0].reshape(1, -1)


	# if(flatWindow[0].shape[0]!=size*size):
	# 	print x,y,flatWindow[0].shape[0]==size*size


	# .T[:,0]
	# flatWindow = np.float64(toGrayScale( np.array(outWindow)).reshape(1, -1)).T[:,0]
	

	# print flatWindow.shape
	# exit()
	# print flatWindow.shape
	return flatWindow
	# scale the value!
				# print window.shape
				# exit()

		# print listExamplesImages.shape

		# scaler.fit_transform(listExamplesImages)

		# self.setCropAsMainImage()
		# sizes = classCtrl.getExampleSizes(None)

		# scalers = imageCtrl.getScaler(self.imageInfo)
		# if(scalers == None):

			# imageCtrl.saveScaler(self.imageInfo,scalers)
		# self.scaler = scalers
			




				#	print xWindow
					# print yWindow
				# exit()
				#print self.imageData.shape
						# self.getCropWindow_raw(sizeIndex,xWindow,yWindow)

			# exit()

		# "error"
	# adds 3 rotated examples per sample (0,90,180,270)