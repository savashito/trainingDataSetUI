import unittest
import sys
sys.path.append('../')
import mlUtil.hogTransform as hogTransform
import numpy as np
import projectCtrl
import unittest
import scalarCtrl
import exampleCtrl
import classCtrl
import imageCtrl
from MLProject import MLProject

class MLProjectTest(unittest.TestCase):
	def setUp(self):
		# pass
		self.mlProject = MLProject("Craters")		
		nameImages = self.mlProject.listImages()
		# print nameImages
		self.mlProject.setImage(nameImages[4])

		return
		classesName,classes = classCtrl.listClassesName(self.project)
		print classesName
		self.craters = classes['craters']
		self.background = classes['background']
		names,self.imagesInfo = imageCtrl.retrieveImages(self.project)
		self.imageInfo = self.imagesInfo[names[4]]
	def testHog(self):
		return
		size = 64
		cratersInfo,cratersData,cratersClass = exampleCtrl.getExamplesFromImage(self.project,self.craters,size,self.imageInfo)
		# backgroundInfo,backgroundData,backgroundClass = exampleCtrl.getExamplesFromImage(self.project,self.background,size,self.imageInfo)
		# cratersData = scalarCtrl.flatenImagesList(cratersData)
		crater = scalarCtrl.toGrayScale(cratersData[0])
		print crater.shape

		# X = scalarCtrl.flatenImagesList(np.array(X))
		x = hogTransform.hog(crater)

		print x.shape
		print x
	def testHogTransform(self):
		X_train, X_validation, y_train, y_validation  = self.mlProject.getTrainTestSplit(2)
		print np.array(X_train).shape