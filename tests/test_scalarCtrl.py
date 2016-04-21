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
mlProject = None

class MLProjectTest(unittest.TestCase):
	def setUp(self):
		self.mlProject = MLProject("Craters")
		# print "Miauuu"

	def test_scaledImages(self):
		# print "Bark"
		mlProject = self.mlProject
		projectCtrl.updateOutputImageFolder(mlProject.project)
		# print mlProject.project.outputImageFolder
		# exit()

		nameImages = self.mlProject.listImages()
		# print nameImages
		mlProject.setImage(nameImages[0])
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
		# print m.shape
		print X.std(axis=0)
		# return
		############
		mlProject.setImage(nameImages[3])
		y,X,lCraterInfo = mlProject.getExamplesFromImage(sizeIndex)
		Xt = mlProject.getAllWindowsFromImage(sizeIndex)

		# X = mlProject.normalize(sizeIndex,X)
		X = scalarCtrl.flatenImagesList(np.array(X))
		X = mlProject.normalize(sizeIndex,X)
		# print X.shape
		m = np.array(X.mean(axis=0))
		print m
		# print m.shape
		print X.std(axis=0)
		self.assertEqual(1,1)
