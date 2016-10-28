import mlUtil.mlUtil as mlUtil
from heatmap import Heatmap
from MLProject import MLProject
import imageCtrl
import exampleCtrl
import sys
import matplotlib.pyplot as plt
from debugUtil import debug

import numpy as np

sys.path.append('E:/Savage/craterRepo/craters/bayesCraterModeling')
from pythonMCMC.CraterRequest import CraterRequest
if __name__== "__main__":
	while(1):
		craterRequest = CraterRequest()
		craterRequest.loadImage("fd")
	exit()

	mlProject = MLProject("Craters")
	# img,ex = exampleCtrl.getExample(mlProject.project,"craters_1716")
	# exampleCtrl.test(ex._class)
	nameImages = mlProject.listImages()

	mlProject.setImage(nameImages[4])
	mlProject.loadImage()
	# mlProject.setCropAsMainImage()
	# nameCrops = mlProject.listCrops()
	# mlProject.setCrop(nameCrops[4])
	# mlProject.loadCrop()
	# mlProject.displayImage()
	# exit()	


	
	# mlProject.getBackgroundExamples(32)
	# exit()
	
	
	bestFit = mlUtil.findBestSVMHyperparameters(mlProject,False)
	# exit()
	# print "Hyper params",np.array(bestFit).shape
	clfs = mlUtil.getClasifiersForProject(mlProject,bestFit,False)


	crops = mlProject.getGPUCrops()
	heatmap = Heatmap (clfs,mlProject)
	for cropIndex in crops:
		crop = mlProject.getGPUCrop(cropIndex)
		mlProject.setCropRawDataGray(crop)
		craterRequest.loadCrop(crop)
		# mlProject.displayImage()
		# craterRequest.loadCrop(crop)
		
		heatmap.generateComposite()
		heatmap.plotComposite()
	heatmap.show()
		# exit()
	exit()
		# heatmap.generate(0)
		# heatmap.plot()

		# mlProject.saveCropForGPU()
	# exit()
	# mlUtil.plotPrecisionRecallForProject(mlProject,clfs)
	# plt.show()
	# exit()
	heatmap = Heatmap (clfs,mlProject)

	# heatmap.generate(0)
	# heatmap.plot()
	heatmap.generate(3)
	heatmap.plot()

	heatmap.generate(2)
	# # # # # centroids = heatmap.getCentroids()
	heatmap.plot()
	# # mlProject.getExamples(3)
	heatmap.generate(1)
	heatmap.plot()
	heatmap.plotComposite()

	heatmap.show()
	# mlProject.displayImage()

	exit()
	# exit()
	# print "Llego"
	# mlProject.safeDeleteImage()
	exit()
	debug(nameImages)
	

	# bestFit = mlUtil.findBestSVMHyperparameters(mlProject)
	# clfs = mlUtil.getClasifiersForProject(mlProject,bestFit)
	# mlUtil.plotPrecisionRecallForProject(mlProject,clfs)


	'''
	# list images within the project
	nameImages = mlProject.listImages()
	debug(nameImages)
	mlProject.setImage(nameImages[3])  # 1
	mlProject.loadImage()

	# exit()
	nameCrops = mlProject.listCrops()
	mlProject.setCropAsMainImage()

	# mlProject.setCrop(nameCrops[0])
	# mlProject.loadCrop()
	 # 3
	# mlProject.setCropAsMainImage()
	# mlProject.getExamplesFromCrop(0)
	# X_train, X_validation, y_train, y_validation = mlProject.getTrainTestSplit(0)
	# print X_train.shape
	# exit()
	

	#  ##mlProject.rotateExamplesCrater()

	# print nameCrops
	# exit()

	###########

	# plt.show()
	

	plt.show()
	# exit()
	# mlUtil.plotPrecisionRecallForProject(mlProject,clfs)

	# print validationSetX[0][0].shape
	# exit()

	heatmap = Heatmap (clfs,mlProject)

	heatmap.generate(0)
	heatmap.plot()
	heatmap.generate(1)
	heatmap.plot()

	heatmap.generate(2)
	# # # centroids = heatmap.getCentroids()
	heatmap.plot()
	# # mlProject.getExamples(3)
	heatmap.generate(3)
	heatmap.plot()

	heatmap.show()
	'''


'''
	nameImages = mlProject.listImages()
	print nameImages
	mlProject.setImage(nameImages[2])
	print mlProject.imageInfo.id
	print mlProject.imageInfo  
	X,y,z=mlProject.getBackgroundExamples(128)
	print (np.array(X).shape)
	print "----------------"
	mlProject.setImage(nameImages[4])
	print mlProject.imageInfo.id
	print mlProject.imageInfo
	X,y,z = mlProject.getBackgroundExamples(128)
	print (np.array(X).shape)

	print "----------------"
	# mlProject.loadImage()
	exit()
	'''