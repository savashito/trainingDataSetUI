import fitParameters
import exampleCtrl
import projectCtrl 
import classCtrl
import os.path
 

# from sklearn import cross_validation
from sklearn import svm

import numpy as np
from sklearn.externals import joblib
from precisionRecall import plotPrecisionRecall 


def findBestSVMHyperparameters(mlProject,recalculate=False):
	sizes = mlProject.getWindowSizes()
	bestFit = []
	print sizes
	fname = 'hyperparameters.pkl'
	# try to load pickle
	if(os.path.isfile(fname) and recalculate == False):
		bestFit = joblib.load(fname)
	else:
		for size in range(len(sizes)):
			# images,target = mlProject.getExamples(size)
			# X_train, X_validation, y_train, y_validation = train_test_split(images,target,test_size=0.20, random_state=42)
			X_train, X_validation, y_train, y_validation = getTrainTestSplit(size)
			gamma,c = fitParameters.findBestParametersSV(X_train,y_train)
			fit = {'gamma':gamma,'C':c}
			bestFit.append(fit)
			print bestFit
		joblib.dump(bestFit, fname) 
	return bestFit


	
def plotPrecisionRecallForProject(mlProject,clfs):
	for i in range(len(clfs)):
		clf = clfs[i]
		X_train, X_validation, y_train, y_validation = mlProject.getTrainTestSplit(i)
		plotPrecisionRecall(clf,X_validation,y_validation)
		
def getClasifiersForProject(mlProject,hyperparameters,recalculate=False):
	clfs = []
	# fetch validation sets
	validationSetX =[]
	validationSetY =[]
	fname = 'clfs.pkl'
	fNorm = 'normalization.pk1'
	# try to load pickle
	if(os.path.isfile(fname) and recalculate == False):
		clfs = joblib.load(fname)
		scalar = joblib.load(fNorm)
		mlProject.setDataNormalizer(scalar)
		print clfs
	else:
		for size in range(len(hyperparameters)):
			try:
				print size
				gamma,C = hyperparameters[size]['gamma'],hyperparameters[size]['C']
				clf = svm.SVC(kernel='rbf',gamma=gamma,C=C,probability=True)
				# images,target = mlProject.getRotatedExamples(size)
				# images,target = mlProject.getExamples(size)
				# X_train, X_validation, y_train, y_validation = train_test_split(images,target,test_size=0.20, random_state=42)
				X_train, X_validation, y_train, y_validation = getTrainTestSplit(size)
				print "starting to fit"
				clf.fit(X_train,y_train)
				print "fitted completed"
				clfs.append(clf)
				validationSetX.append(X_validation)
				validationSetY.append(y_validation)
			except:
				import traceback
				traceback.print_exc()
				validationSetX.append(None)
				validationSetY.append(None)
				clfs.append(None)
		joblib.dump(clfs, fname) 
		joblib.dump(mlProject.getDataNormalizer(), fNorm) 


	return clfs

def toClassSpace(y):
	y = np.array(y)-1
	return y