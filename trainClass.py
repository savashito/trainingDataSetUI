import exampleCtrl
import projectCtrl 
import classCtrl
from MLProject import MLProject

# from sklearn import cross_validation
from sklearn import svm
from sklearn.cross_validation import train_test_split
import numpy as np
import fitParameters


mlProject = MLProject("Craters")

nameImages = mlProject.listImages()
mlProject.setImage(nameImages[0])
nameCrops = mlProject.listCrops()
mlProject.setCrop(nameCrops[0])

# size = 2

bestFit = [{},{},{'C': 10.0, 'gamma': 0.001},{'C': 10.0, 'gamma': 0.0001}]
validationSetX =[]
validationSetY =[]
clfs = []
for size in range(len(bestFit)):
	try:
		print size
		gamma,C = bestFit[size]['gamma'],bestFit[size]['C']
		clf = svm.SVC(kernel='rbf',gamma=gamma,C=C,probability=True)
		images,target = mlProject.getExamples(size)
		X_train, X_validation, y_train, y_validation = train_test_split(images,target,test_size=0.20, random_state=42)
		clf.fit(X_train,y_train)
		clfs.append(clf)
		validationSetX.append(X_validation)
		validationSetY.append(y_validation)
	except:
		validationSetX.append(None)
		validationSetY.append(None)
		clfs.append(None)
# gamma,c,clf = fitParameters.findBestParametersSV(X_train,y_train)
'''
size = 3
testSet = validationSetX[size]
# testSet = X_train # validationSetX[size]
probas = clfs[size].predict_proba(testSet)
pred = clfs[size].predict(testSet)
print X_train
print validationSetX[size]
print validationSetY[size]
print probas
print pred
exit()
'''

# win = mlProject.getCropWindow(size,1116.0,6.0)
# win = mlProject.getCropWindow(size,0.0,0.0)
# print win
# print clfs[size].predict_proba(win)[0,0]
# exit()

import matplotlib.pyplot as plt

class Heatmap:
	def __init__(self,clfs,mlProject):
		self.clfs = clfs
		self.mlProject = mlProject
		print size
		window = mlProject.getCropWindow(size,1116.0,6.0)
		print clfs[size].predict_proba(window)[0,0]
	def generate(self):
		size = 2
		# overlapPercent = 0.90
		overlapPercent = 0.10
		clf = self.clfs[size]

		cropW,cropH =  mlProject.getCropShape()[0],mlProject.getCropShape()[1]

		windowW,windowH = mlProject.getWindowSize(size)
		print windowW
		dx = np.around(windowW*(1-overlapPercent))
		heatmapW = int(np.floor((cropW-windowW)/dx))
		heatmapH = int(np.floor((cropH-windowH)/dx))
		heatmapArray = np.zeros((heatmapW,heatmapH))
		# crop = mlProject.getCrop()
		for y in range(heatmapH):
			for x in range(heatmapW):
				xCrop,yCrop = x*dx,y*dx
				# get window
				# print x,y,heatmapW
				# print 
				window = mlProject.getCropWindow(size,xCrop,yCrop)
				#window = mlProject.getCropWindow(size,1116.0,6.0)
				#print window.shape
				# print window.shape
				# window = window.reshape(1, -1)
				# print window.shape
				# print clf.predict_proba(window)
				# return 
				#print clf.predict_proba(window)[0,0]
				# return
				# return
				
				if(clf.predict_proba(window)[0,0] < 0.5):
					heatmapArray[x][y] = 0 
				else :
					heatmapArray[x][y] = 1 
				
				# np.max( (0.5,clf.predict_proba(window)[0,0]) )
			# print xCrop,yCrop,heatmapArray[x][y]
		print heatmapArray.shape
		# print np.max(heatmapArray)
		# plt.imshow(heatmapArray)

		# plt.title(self.cropInfo.src)
		# plt.show()
		self.heatmapArray = heatmapArray
		# print heatmapArray.shape
		# print cropW,cropH
		# print dx
	def plot(self):
		self.mlProject.displayCrop(self.heatmapArray)


heatmap = Heatmap (clfs,mlProject)

heatmap.generate()
heatmap.plot()




# mlProject.displayCrop()
# print X_train[0].shape
# heatmap


# for x in np.linspace(0,w,100):
# 	x = np.around(x)
# 	print x

# windowData = mlProject.getCropWindow(size,0,0)
# print clf.predict(windowData)
#print y_train[0]
#print clf.predict(X_train[0])

# w,h =  mlProject.getCropShape()[0],mlProject.getCropShape()[1]

'''
for gamma in [1,0.001,10]:
	clf = svm.SVC(kernel='rbf',gamma=gamma,C=100)
	scores = cross_validation.cross_val_score(clf, X_train, y_train, cv=5)
	print "for gamma: %f -> %f "%(gamma,scores.mean())
'''

# clf.fit(X_train,y_train)
# print clf.score(X_test, y_test)  
# hog transform
# generate 2d plot



# import matplotlib.pyplot as plt
# import numpy as np

# a = np.random.random((16, 16))
# # print np.max(a)
# # print np.min(a)
# plt.imshow(a, cmap='hot', interpolation='nearest')
# plt.show()

# do training here

'''
images,target = mlProject.getExamples(0)

print nameImages
clf.fit(images,target)

# calc window 

w,h =  mlProject.getCropShape()[0],mlProject.getCropShape()[1]
for i in range (w):
	window = mlProject.getCropWindow(0,10,10)
	print window.shape
	print('pred ',clf.predict(w))

'''
# print('pred ',clf.predict(images[130]))


# Check if box is in correct range
# flat image linearly in window

