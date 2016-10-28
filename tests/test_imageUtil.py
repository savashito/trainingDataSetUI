import sys
# py -m unittest -v test_MLProject
sys.path.append('../')
import imageUtil
import unittest
# import numpy as np
import scalarCtrl
import testData
from MLProject import MLProject
# mlProject = None

class MLProjectTest(unittest.TestCase):
	def setUp(self):
		# pass
		self.mlProject = MLProject("Craters")
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
		return
		# getWindowFrom image, should raise an exception when accessing a block that is not part off.
		# imageData = testData.generate1DTestImage(10,10)
		# imageDataGray = scalarCtrl.toGrayScale(imageData)
		imageDataGray = testData.generate2DTestImage(1024+512,1024+512)
		print imageDataGray.shape
		imageUtil.saveRawFloatImage(imageDataGray,"img.dat","")

		# flatWindow = scalarCtrl.getWindowFromImage(4,1,1,imageDataGray)
		# print flatWindow
	def test_saveCropForGPU(self):
		self.mlProject.imageDataGray = testData.generate2DTestImage((1024+512)*3+100,1024+512+200)
		lCrops = self.mlProject.getGPUCrops()
		print self.mlProject.getGPUCrop(0)
		print lCrops
		# self.mlProject.saveCropForGPU(imageDataGray)