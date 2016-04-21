import mlUtil.mlUtil as mlUtil
from heatmap import Heatmap
from MLProject import MLProject
import imageCtrl
import sys
import matplotlib.pyplot as plt
from debugUtil import debug


if __name__== "__main__":
	mlProject = MLProject("Craters")
	nameImages = mlProject.listImages()
	mlProject.setImage(nameImages[3])
	mlProject.deleteAllExamples()
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



