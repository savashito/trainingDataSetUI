
from marsSchema import Example
from overlawManager import SmallCrop
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
	print "Rec is {0},{1} ,{2}, {3}".format(rec[0],rec[1],rec[2],rec[3])
	print "the next index is " + str(i)
	# create the name for the next sample
	sampleName = _class.name+"_"+str(i)
	sampleDir = getExamplesDir(project,_class)
	print sampleName
	print sampleDir
	imageUtil.saveImage(imageData,sampleName+".png",sampleDir)
	print "parentCrop "+parentImageInfo.src
	# Save to db
	return insertExample(_class,parentImageInfo,sampleName,rec)

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
def getExampleSizeCount(project,_class,sizes):
	l = []
	for size in sizes:
		examples = Example.select().where(Example._class == _class,Example.bottomRightX == size)
		l.append(examples.count())
	print l
	return l
def retriveExamples(project,_class,cropInfo,size):
	examples = Example.select().where(Example._class == _class, Example.parentCrop == cropInfo,Example.bottomRightX == size)
	l = []
	listCrops = {}
	try :
		for example in examples:
			l.append(example.src)
			listCrops[example.src] = SmallCrop(example.topLeftX,example.topLeftY,example.bottomRightX,example.bottomRightY,example.src)
		
		# print examples.count()
		# print len(examples)
	except Exception as e:
		print "No craters here"
		print e
	return l,listCrops

	# print examples
	# # if(examples==None):
	# # 	print "None"
	# # 	return
	# for example in examples:
	# 	name = example.src
	# 	print name



