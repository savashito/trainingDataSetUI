# list images
# load images
# for each image create a normilizer.
# all examples will be normilized with the image
# import sys
# import os
# os.chdir("../")
# sys.path.append('../')

def normalize(mlProject):
	imagesName = mlProject.listImages()
	for imageName in imagesName:
		# load image
		mlProject.setImage(imageName)
		mlProject.createCalculateScalerForImage()

	print imageName


from MLProject import MLProject

mlProject = MLProject("Craters")
normalize(mlProject)