import mlUtil.mlUtil as mlUtil
from heatmap import Heatmap
from MLProject import MLProject

import sys

mlProject = MLProject("Craters")
nameImages = mlProject.listImages()
mlProject.setImage(nameImages[0])  # 1

# print nameImages
nameCrops = mlProject.listCrops()
# print 
mlProject.setCropAsMainImage()
# mlProject.setCrop(nameCrops[1]) # 3
mlProject.getExamplesFromCrop(0)
X_train, X_validation, y_train, y_validation = mlProject.getTrainTestSplit(0)
print X_train.shape
exit()
# mlProject.setCropAsMainImage()

#  ##mlProject.rotateExamplesCrater()

# print nameCrops
# exit()

###########

bestFit = mlUtil.findBestSVMHyperparameters(mlProject)
# print bestFit
# exit()

# gamma,c,clf = fitParameters.findBestParametersSV(X_train,y_train)

###########
# size = 2

# bestFit = [{'C': 0.01, 'gamma': 1.0000000000000001e-09}, {'C': 1.0, 'gamma': 0.001}, {'C': 1.0, 'gamma': 0.0001}, {'C': 10.0, 'gamma': 1.0000000000000001e-05}]
# bestFit = [{'C': 10.0, 'gamma': 0.10000000000000001},{'C': 10.0, 'gamma': 0.10000000000000001},{'C': 1.0, 'gamma': 0.001},{'C': 10.0, 'gamma': 0.0001}]
# bestFit = [{'C': 10.0, 'gamma': 0.10000000000000001},{'C': 10.0, 'gamma': 0.10000000000000001},{'C': 10.0, 'gamma': 0.001},{'C': 10.0, 'gamma': 0.0001}]

clfs = mlUtil.getClasifiersForProject(mlProject,bestFit)

# mlUtil.plotPrecisionRecallForProject(mlProject,clfs)

# print validationSetX[0][0].shape
# exit()

heatmap = Heatmap (clfs,mlProject)

heatmap.generate(0)
heatmap.plot()
# heatmap.generate(1)
# heatmap.plot()

# heatmap.generate(2)
# centroids = heatmap.getCentroids()
# heatmap.plot()
# heatmap.generate(3)
# heatmap.plot()
heatmap.show()





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

