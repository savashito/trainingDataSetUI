import peewee
from marsSchema import Image
import imageUtil # import saveImage3,loadImage
def insertImages(listImages):
	for image in listImages:
		try:
			Image.create(
				src=image['src'],
				longitud=image['longitud'],
				latitide=image['latitide'],
				resolution=image['resolution'])
			print "Image inserted "
		except peewee.IntegrityError as e:
			print "image updated {0}  ".format(e)
			# imageRecord = Image.get(src=image['src'])
			'''
			imageRecord.longitud = image['longitud']
			imageRecord.latitide = image['latitide']
			imageRecord.resolution = image['resolution']
			imageRecord.save()
			'''
	
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
			filename = "{0}/{1}".format(path,name)
			print filename
			imageData,name = imageUtil.loadImage(filename)
			print imageData
			imageInfo = saveImage(project,imageData,name,readMetadata(filename))
			# return None,None
	if(imageData==None):
		directory = getImageDir(name,project)
		filename = "{0}/{1}".format(directory,name)
		imageData,name = imageUtil.loadImage(filename)
		
	return imageData,imageInfo
def getImageDir(name,project):
	directory = project.outputImageFolder
	l = name.split('.')
	name = l[0]
	imageDir = "{0}/{1}".format(directory,name)
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
