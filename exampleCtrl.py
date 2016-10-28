
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

def test(cla):

	# print 
	print finalEx
	return
	names = []
	ids = []
	i =0
	for ex in examples:
		name = ex.src.split('_')
		num = int(name[1])

		if(num!=ex.id-8771):
			print num-ex.id-8771,num,ex.id,i
			# exit()
		names.append(ex.src)
		ids.append(ex.id-8771)
		i=i+1

	print getNextId()
	print names
	print ids
	print i
def getNextId(_class):
	examples =  Example.select().where(Example._class == _class)
	i = examples.count()-1
	finalEx = 0
	if(i>=0):
		finalEx = int(examples[i].src.split('_')[1])+1

	return finalEx
	# return Example.select().where(Example._class == _class).count()
# the name is infeared from the next index to insert to db
def saveExample(_class,project,parentImageInfo,rec,imageData):
	# find index of the next example from the current image being sampled
	i = getNextId(_class)
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

def rotateExampleAndSave(taggedClass,project,imageInfo,rec,imgData):
		exampleInfo = saveExample(taggedClass,project,imageInfo,rec,imgData)
		img90 = imageUtil.rotateImage(imgData,90.0)
		img180 = imageUtil.rotateImage(imgData,180.0)
		img270 = imageUtil.rotateImage(imgData,270.0)
		saveExampleTransformed(exampleInfo,img90,project)
		saveExampleTransformed(exampleInfo,img180,project)
		saveExampleTransformed(exampleInfo,img270,project)
		return exampleInfo
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
def deleteAllExmples():
	q = Example.delete()
	q.execute()
	print "successfuly deleted all examples! Forever!"


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
import numpy as np
def getImagesFromExamples(examples,project):
	l = []
	listExamplesData = []
	listClassIdentifier = []
	listNullExampleImages = []
	for example in examples:
		
		image = loadExample(project,example)
		if(image == None ):
			listNullExampleImages.append(example)
			print "Error, image doesn't exist!",example.src,(example.bottomRightX,example.bottomRightX)
			continue
		
		if(image[:,:,0].shape != (example.bottomRightX,example.bottomRightX)):
			print "Error, image shape is inconsistent with db?",example.src,(example.bottomRightX,example.bottomRightX), image.shape
			listNullExampleImages.append(example)
			continue
			#exit()
		l.append(example)
		listExamplesData.append(image)
		# print "example._class.id "+str(example._class.id)
		listClassIdentifier.append(example._class.id) 
	# clean up null examples
	if(len(listNullExampleImages) > 0):
		debug("Cleaning null examples")
		for nullExample in listNullExampleImages:
			deleteExmplesBySrc( nullExample.src)
			debug("Deleted example "+ nullExample.src)
		# exit()			
	# if(len(listExamplesData)>0):
		# print "loaded image ",examples[0].src,listExamplesData[0].shape,np.array(listExamplesData).shape

	# print "getImagesFromExamples",np.array(listExamplesData).shape
	return l,listExamplesData,listClassIdentifier

def getExampleSize(project,_class,size):
	examples = Example.select().where(Example._class == _class,Example.bottomRightX == size)
	l,listExamples,listClassIdentifier = getImagesFromExamples(examples,project)
	# print "loaded %d samples of %s, size: %dx%d"%(len(listExamples),_class.name,size,size)
	# examplesInfo,examplesData,examplesClasses
	return l,listExamples,listClassIdentifier

# extract examples from imageInfo, 
# but also examples from each crop belonging to imageInfo
def getExamplesFromImage(project,_class,size,imageInfo):
	# debug("getExamplesFromImage "+"class: "+_class.name+" "+imageInfo.src)
	# imageName,listImageInfo = cropCtrl.retrieveCrops(project,imageInfo)
	listImageInfo = {}
	listImageInfo[imageInfo.src]=imageInfo
	listExamplesClass,examplesData,examplesInfo = [],[],[]
	# print listImageInfo
	for imageName in listImageInfo:
		
		imageInfo = listImageInfo[imageName]
		# print "retriveExamples ",_class.name,imageInfo.src,size
		examples = Example.select().where(Example._class == _class,Example.parentCrop == imageInfo,Example.bottomRightX == size)
		# print "examplesN "+str(examples.count())
		# print examples
		tExamplesInfo,tExamplesData,tClassIdentifier = getImagesFromExamples(examples,project)
		# print "accum size : "+str( np.array(examplesData).shape)
		# print "size is :"+str( np.array(tExamplesData).shape)
		# print "getExamplesFromImage",_class.name, np.array(tExamplesData).shape
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
	print "retriveExamples ",_class.name,cropInfo.src,len(examples),size
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



