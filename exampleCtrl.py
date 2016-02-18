
from marsSchema import Example
import imageUtil
def insertExample(_class,parentImageInfo,name,rec):
	return Example.create(
		_class = _class,
		src = name,
		parentCrop = parentImageInfo,
		topLeftX = rec[0],
		topLeftY = rec[1],
		bottomRightX = rec[2],
		bottomRightY = rec[3]
		)
# the name is infeared from the next index to insert to db
def saveExample(_class,project,parentImageInfo,rec,imageData):
	# find index of the next example from the current image being sampled
	i = Example.select().where(Example._class == _class).count()
	print "the next index is " + str(i)
	# create the name for the next sample
	sampleName = _class.name+"_"+str(i)
	sampleDir = getExamplesDir(project,_class)
	print sampleName
	print sampleDir
	imageUtil.saveImage(imageData,sampleName+".png",sampleDir)
	# Save to db
	insertExample(_class,parentImageInfo,sampleName,rec)
# returns the image and the example
def getExample(project,exampleName):
	example = Example.select().where(Example.src == exampleName).get()
	sampleDir = getExamplesDir(project,example._class)
	imageData,name = imageUtil.loadImage(sampleDir+"/"+example.src+".png")
	return imageData,example
def getExamplesDir(project,_class):
	name = _class.name
	directory = project.outputImageFolder
	imageDir = "{0}/examples/{1}".format(directory,name)
	return imageDir
def listExamples(_class):
	examples = Example.select().where(Example._class == _class)
	l = []
	listExamples = {}
	for example in examples:
		name = example.src
		l.append(name)
		listExamples[name] = example
	return l,listExamples