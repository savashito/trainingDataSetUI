
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


def calculateScalerForImage(sizes,imageData):
	s = imageData.shape
	W,H = s[0],s[1]
	scalers = range(len(sizes))

	for sizeIndex in range(len(sizes)):
		size = sizes[sizeIndex]
		dx = size
		listExamplesImages = []
		mapW,mapH = W/size,H/size
		for y in range(mapH):
			for x in range(mapW):
				xWindow,yWindow = x*dx,y*dx
				window = getWindowFromImage(sizeIndex,xWindow,yWindow,imageData)
				listExamplesImages.append(window)
		listExamplesImages = np.array(listExamplesImages)
		scaler = StandardScaler().fit(listExamplesImages)
		scalers[sizeIndex] = scaler

def getWindowFromImage(size,x,y,imageData):
	# imageData = # testCropData if testCropData!=None else self.cropData
	outWindow = []
	for i in range(size):
		outWindow.extend(extractLinearArray(imageData,x,y+i,size))
	# scaler = StandardScaler()
	flatWindow = np.float64(toGrayScale( np.array(outWindow)).reshape(1, -1))
	
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