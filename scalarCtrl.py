import numpy as np
from debugUtil import debug

from sklearn.preprocessing import StandardScaler

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
		# print size
		listExamplesImages = getAllWindowsFromImage(size,imageData)

		listExamplesImages = np.array(listExamplesImages)
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

def getWindowFromImage(size,x,y,imageData):
	# imageData = # testCropData if testCropData!=None else self.cropData
	outWindow = []
	for i in range(size):
		outWindow.extend(extractLinearArray(imageData,x,y+i,size))

	# print x,y,size
	# scaler = StandardScaler()
	# print np.array(outWindow).shape
	# print len(outWindow)

	flatWindow = np.float64(toGrayScale( np.array(outWindow)).reshape(1, -1))
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