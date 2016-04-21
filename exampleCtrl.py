
from marsSchema import Example
from overlawManager import SmallCrop
import os
import imageUtil
import cropCtrl
from debugUtil import debug
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
# save a different copy of the examply, in same location but rotated
def saveExampleTransformed(formerExample,imageData,project):
	# print "saving rotated example "+str(formerExample.src)
	return saveExample(formerExample._class,project,formerExample.parentCrop,[formerExample.topLeftX,formerExample.topLeftY,formerExample.bottomRightX,formerExample.bottomRightY],imageData)
	

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

# def rotateExample(imageData):


def loadExample(project,example):
	_class = example._class
	sampleName = example.src
	sampleDir = getExamplesDir(project,_class)
	sampleFullName = "{0}{2}{1}.png".format(sampleDir,sampleName,os.sep)
	# print sampleFullName
	image,name = imageUtil.loadImage(sampleFullName)
	return image

# returns the image and the example
def getExample(project,exampleName):
	example = Example.select().where(Example.src == exampleName).get()
	sampleDir = getExamplesDir(project,example._class)
	imageData,name = imageUtil.loadImage(sampleDir+os.sep+example.src+".png")
	return imageData,example
def deleteExmplesBySrc(name):
	q = Example.delete().where(Example.src == name) # .where(Example._class == _class.id)
	q.execute()
def deleteExmplesBySrcRange(name,start,end):
	for i in range(start,end):
		exName = name+'_'+str(i)
		# print exName
		deleteExmplesBySrc(exName)

def deleteExmples(_class):
	q = Example.delete().where(Example._class == _class) # .where(Example._class == _class.id)
	q.execute()
def getExamplesDir(project,_class):
	name = _class.name
	directory = project.outputImageFolder
	imageDir = "{0}{2}examples{2}{1}".format(directory,name,os.sep)
	return imageDir

def listify(examples):
	l = []
	listExamples = {}
	for example in examples:
		name = example.src
		l.append(name)
		listExamples[name] = example
	return l,listExamples

def listExamples(_class):
	examples = Example.select().where(Example._class == _class)
	return listify(examples)

def getImagesFromExamples(examples,project):
	l = []
	listExamplesData = []
	listClassIdentifier = []
	for example in examples:
		l.append(example)
		image = loadExample(project,example)
		listExamplesData.append(image)
		# print "example._class.id "+str(example._class.id)
		listClassIdentifier.append(example._class.id) 
	return l,listExamplesData,listClassIdentifier

def getExampleSize(project,_class,size):
	examples = Example.select().where(Example._class == _class,Example.bottomRightX == size)
	l,listExamples,listClassIdentifier = getImagesFromExamples(examples,project)
	print "loaded %d samples of %s, size: %dx%d"%(len(listExamples),_class.name,size,size)
	# examplesInfo,examplesData,examplesClasses
	return l,listExamples,listClassIdentifier

# extract examples from imageInfo, 
# but also examples from each crop belonging to imageInfo
def getExamplesFromImage(project,_class,size,imageInfo):
	debug("getExamplesFromImage "+"class: "+_class.name+" "+imageInfo.src)
	imageName,listImageInfo = cropCtrl.retrieveCrops(project,imageInfo)
	listImageInfo[imageInfo.src]=imageInfo
	listExamplesClass,examplesData,examplesInfo = [],[],[]
	for imageName in listImageInfo:
		imageInfo = listImageInfo[imageName]
		examples = Example.select().where(Example._class == _class,Example.bottomRightX == size,Example.parentCrop == imageInfo)
		# print examples
		tExamplesInfo,tExamplesData,tClassIdentifier = getImagesFromExamples(examples,project)
		# print tExamplesInfo
		# print tClassIdentifier
		examplesInfo.extend(tExamplesInfo)
		examplesData.extend(tExamplesData)
		listExamplesClass.extend(tClassIdentifier)
	return examplesInfo,examplesData,listExamplesClass
	# exit(0)
	
	# print "crps "+str(listCrps)

def deleteAllExamplesFromImage(project,imageInfo):
	# Remove from DB
	q = Example.delete().where(Example.parentCrop == imageInfo) # .where(Example._class == _class.id)
	# its not necesary to remove the images, they would be overwritten
	q.execute()

def getAllExamples():
	return Example.select()

def getExampleSizeCrop(project,_class,size,parentCrop):
	examples = Example.select().where(Example._class == _class,Example.bottomRightX == size,Example.parentCrop == parentCrop)
	l,listExamples,listClassIdentifier = getImagesFromExamples(examples,project)
	print "loaded %d samples of %s, size: %dx%d"%(len(listExamples),_class.name,size,size)
	# examplesInfo,examplesData,examplesClasses
	return l,listExamples,listClassIdentifier


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



