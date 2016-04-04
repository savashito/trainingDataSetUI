import exampleCtrl
import projectCtrl 
import classCtrl
from MLProject import MLProject

# from sklearn import cross_validation
from sklearn import svm
from sklearn.cross_validation import train_test_split
import numpy as np
import fitParameters
from heatmap import Heatmap


mlProject = MLProject("Craters")

nameImages = mlProject.listImages()
mlProject.setImage(nameImages[0])  # 1
nameCrops = mlProject.listCrops()
mlProject.setCrop(nameCrops[0]) # 3

# print nameCrops[3]
# exit()

###########
'''
def findBestFit(mlProject):
	sizes = mlProject.getWindowSizes()
	bestFit = []
	print sizes
	for size in range(len(sizes)):
		images,target = mlProject.getExamples(size)
		X_train, X_validation, y_train, y_validation = train_test_split(images,target,test_size=0.20, random_state=42)
		gamma,c = fitParameters.findBestParametersSV(X_train,y_train)
		fit = {'gamma':gamma,'C':c}
		bestFit.append(fit)
		print bestFit
	return bestFit
		
bestFit = findBestFit(mlProject)
print bestFit
exit()
'''
# gamma,c,clf = fitParameters.findBestParametersSV(X_train,y_train)

###########
# size = 2

# bestFit = [{'C': 0.01, 'gamma': 1.0000000000000001e-09}, {'C': 1.0, 'gamma': 0.001}, {'C': 1.0, 'gamma': 0.0001}, {'C': 10.0, 'gamma': 1.0000000000000001e-05}]
bestFit = [{'C': 10.0, 'gamma': 0.10000000000000001},{'C': 10.0, 'gamma': 0.10000000000000001},{'C': 1.0, 'gamma': 0.001},{'C': 10.0, 'gamma': 0.0001}]
# bestFit = [{'C': 10.0, 'gamma': 0.10000000000000001},{'C': 10.0, 'gamma': 0.10000000000000001},{'C': 10.0, 'gamma': 0.001},{'C': 10.0, 'gamma': 0.0001}]

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




heatmap = Heatmap (clfs,mlProject)

# heatmap.generate(0)
# heatmap.plot()
# heatmap.generate(1)
# heatmap.plot()



heatmap.generate(2)
centroids = heatmap.getCentroids()
heatmap.plot()
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

