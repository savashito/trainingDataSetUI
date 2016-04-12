import mlUtil.mlUtil as mlUtil
from heatmap import Heatmap
from MLProject import MLProject

import sys

mlProject = MLProject("Craters")
# list images within the project
# exit()
nameImages = mlProject.listImages()
mlProject.setImage(nameImages[0])  # 1
nameCrops = mlProject.listCrops()
mlProject.setCropAsMainImage()

# mlProject.setCrop(nameCrops[1]) # 3
# mlProject.getExamplesFromCrop(0)
# X_train, X_validation, y_train, y_validation = mlProject.getTrainTestSplit(0)
# print X_train.shape
# exit()
# mlProject.setCropAsMainImage()

#  ##mlProject.rotateExamplesCrater()

# print nameCrops
# exit()

###########

bestFit = mlUtil.findBestSVMHyperparameters(mlProject,True)


clfs = mlUtil.getClasifiersForProject(mlProject,bestFit,True)
# exit()
# mlUtil.plotPrecisionRecallForProject(mlProject,clfs)

# print validationSetX[0][0].shape
# exit()

heatmap = Heatmap (clfs,mlProject)

# heatmap.generate(0)
# heatmap.plot()
# heatmap.generate(1)
# heatmap.plot()

# heatmap.generate(2)
# # centroids = heatmap.getCentroids()
# heatmap.plot()
# mlProject.getExamples(3)
heatmap.generate(3)
heatmap.plot()

heatmap.show()




