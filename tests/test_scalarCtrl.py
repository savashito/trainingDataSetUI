import sys
# py -m unittest -v test_MLProject
sys.path.append('../')
import imageCtrl
from marsSchema import Project,Image,Crop,Class,Example
from MLProject import MLProject
import unittest
import numpy as np
import scalarCtrl
import projectCtrl
import testData
mlProject = None

class MLProjectTest(unittest.TestCase):
	def setUp(self):
		pass
		# self.mlProject = MLProject("Craters")
		# # print "Miauuu"
		# nameImages = self.mlProject.listImages()
		# # print nameImages
		# self.mlProject.setImage(nameImages[4])
		# nameCrops = self.mlProject.listCrops()

		# self.mlProject.setCrop(nameCrops[3])
		# self.imageData = self.mlProject.loadCrop()
		# #self.imageData = mlProject.loadImage()
	# @unittest.skip("demonstrating skipping")
	# @unittest.skip("demonstrating skipping")
	def test_getWindowFromImage(self):
		# getWindowFrom image, should raise an exception when accessing a block that is not part off.
		imageData = testData.generate1DTestImage(10,10)
		imageDataGray = scalarCtrl.toGrayScale(imageData)
		print imageDataGray
		flatWindow = scalarCtrl.getWindowFromImage(4,1,1,imageDataGray)
		print flatWindow
		# print imageData.shape
		# print imageDataGray.shape

		# flatWindow = scalarCtrl.getWindowFromImage(4,1,1,imageData)
		# print flatWindow
		# print flatWindow.shape
		# arr = self.mlProject.getCropWindow(0,20,20,testCropData=image)

	def test_toGrayScale(self):
		size = 10
		imageData = testData.generate1DTestImage(size,size)
		imageDataGray = scalarCtrl.toGrayScale(imageData)
		# print imageDataGray.shape 
		v= imageDataGray.shape== (size,size)
		# print v
		self.assertTrue(v)

	@unittest.skip("demonstrating skipping")
	def test_scaledImages(self):
		# print "Bark"
		mlProject = self.mlProject
		# projectCtrl.updateOutputImageFolder(mlProject.project)
		# print mlProject.project.outputImageFolder
		# exit()

		nameImages = self.mlProject.listImages()
		# print nameImages
		mlProject.setImage(nameImages[4])
		sizeIndex=3
		# 
		# exit()
		# Xt = mlProject.getAllWindowsFromImage(sizeIndex)
		# X = mlProject.normalize(sizeIndex,Xt)
		
		y,X,lCraterInfo = mlProject.getExamplesFromImage(sizeIndex)
		X = scalarCtrl.flatenImagesList(np.array(X))
		X = mlProject.normalize(sizeIndex,X)
		
		# print X.shape
		m = np.array(X.mean(axis=0))
		print m
		# exit()
		# print m.shape
		print X.std(axis=0)
		
		############
		mlProject.setImage(nameImages[4])
		y,X,lCraterInfo = mlProject.getExamplesFromImage(sizeIndex)
		Xt = mlProject.getAllWindowsFromImage(sizeIndex)

		X = mlProject.normalize(sizeIndex,Xt)
		# X = scalarCtrl.flatenImagesList(np.array(X))
		# X = mlProject.normalize(sizeIndex,X)
		# print X.shape
		m = np.array(X.mean(axis=0))
		print m
		# print m.shape
		print X.std(axis=0)
		self.assertEqual(1,1)

	@unittest.skip("demonstrating skipping")
	def test_calculateScalerForImage(self):
		scalarCtrl.calculateScalerForImage([128],self.imageData)

