import peewee
import os
from marsSchema import Image
import imageUtil # import saveImage3,loadImage
from debugUtil import debug
from sklearn.externals import joblib

def insertImages(project,listImages):
	images = []
	for image in listImages:
		try:
			images.append(Image.create(
				src=image['src'],
				longitud=image['longitud'],
				latitide=image['latitide'],
				resolution=image['resolution'],
				project = project))
			print "Image inserted "
		except peewee.IntegrityError as e:
			print "image already exists {0}  ".format(e)
			# imageRecord = Image.get(src=image['src'])
			'''
			imageRecord.longitud = image['longitud']
			imageRecord.latitide = image['latitide']
			imageRecord.resolution = image['resolution']
			imageRecord.save()
			'''
	return images
def deleteImageBySrc(name):
	q = Image.delete().where(Image.src == name) # .where(Example._class == _class.id)
	q.execute()

def getScalarPickleName(imgInfo):
	# print 
	name = getImageDir(imgInfo.src,imgInfo.project)+os.sep+'scalar_'+imgInfo.src.split('.')[0]+'.pkl'
	debug( "getting scalar in :"+name)
	# exit()
	return name 

def saveScaler(imgInfo,scalar):
	# save the scalar for all the sizes
	fname = getScalarPickleName(imgInfo)
	joblib.dump(scalar, fname) 
	debug("Scalar save succss")
	# "needs to be implemented"


def getScaler(imgInfo):
	# retrieves the scalar for all the sizes
	fname =getScalarPickleName(imgInfo)
	debug("fetching scalar "+str(fname))
	if(os.path.isfile(fname)):
		scalar = joblib.load(fname)
		# debug("lodad success"+str(scalar))
	else:
		scalar = None
	return scalar

def saveImage(project,img,name,metadata):
	meta = readMetadata(metadata)
	imageInfo = None

	try:
		imageInfo = Image.create(src=name,
				longitud=meta['longitud'],
				latitide=meta['latitide'],
				resolution=meta['resolution'],
				metadata = metadata,
				project= project
				)
	except peewee.IntegrityError:
		print "Key exists: "+name
		imageInfo = Image.select().where(Image.src==name).get()
	directory = getImageDir(name,project)
	print 'Dir: '+directory
	# save image to HD
	imageUtil.saveImage(img,name,directory)
	return imageInfo
# retrive image from DB,
# if the image is not existant, it will load ot
def getImage(name,project,path=None,imageInfo=None):
	imageData = None
	if(imageInfo==None):
		try:
			imageInfo = Image.select().where(Image.src==name).get()
		except Image.DoesNotExist:
			print "bark bark"
			# no metadata
			filename = "{0}{2}{1}".format(path,name,os.sep)
			# print filename
			imageData,name = imageUtil.loadImage(filename)
			# print imageData
			imageInfo = saveImage(project,imageData,name,readMetadata(filename))
			# return None,None
	# print "imageInfo "+imageInfo.src
	# print "imageData "+str(imageData)
	if(imageData==None):
		directory = getImageDir(name,project)
		filename = "{0}{2}{1}".format(directory,name,os.sep)
		# print "trying to load "+str(filename)
		debug("Loaded image "+filename+" id "+str(imageInfo.id) )
		imageData,name = imageUtil.loadImage(filename)
		# debug("Loaded image "+filename+" id "+str(imageInfo.id) )
		debug(" Shape "+str(imageData.shape))
		# imageData,name = imageUtil.loadImageForDisplay(filename)
		
	# print "imageData "+str(imageData)

	return imageData,imageInfo
def getImageDir(name,project):
	directory = project.outputImageFolder
	print directory
	l = name.split('.')
	name = l[0]
	imageDir = "{0}{2}{1}".format(directory,name,os.sep)
	# print imageDir
	return imageDir
def readMetadata(m):
	return {
		 'longitud': 10,
		 'latitide': 3.2,
		 'resolution':1
		 } 
def retrieveImages(project):
	images = Image.select()
	l = []
	listImages = {}
	# print images
	for image in images:
		l.append(image.src)
		listImages[image.src] = image
		# listImages.append(image)
	return l,listImages
		# print "src: {0}, id: {1}".format(image.src,image.id)
	# image = images.where(Image.id==1)
	# print image.get().src
	# for i in image:
		# print "id 1 is "+i.src
