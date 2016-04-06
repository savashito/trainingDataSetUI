
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

# def rotateExample(imageData):
	

def loadExample(project,_class,example):
	sampleName = example.src
	sampleDir = getExamplesDir(project,_class)
	sampleFullName = "{0}/{1}.png".format(sampleDir,sampleName)
	# print sampleFullName
	image,name = imageUtil.loadImage(sampleFullName)
	return image

# returns the image and the example
def getExample(project,exampleName):
	example = Example.select().where(Example.src == exampleName).get()
	sampleDir = getExamplesDir(project,example._class)
	imageData,name = imageUtil.loadImage(sampleDir+"/"+example.src+".png")
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
	imageDir = "{0}/examples/{1}".format(directory,name)
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
def getExampleSize(project,_class,size):
	examples = Example.select().where(Example._class == _class,Example.bottomRightX == size)
	l = []
	listExamples = []
	listClassIdentifier = []
	for example in examples:
		l.append(example)
		image = loadExample(project,_class,example)
		listExamples.append(image)
		listClassIdentifier.append(_class.id)
	print "loaded %d samples of %s, size: %dx%d"%(len(listExamples),_class.name,size,size)
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



