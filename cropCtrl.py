import peewee
from marsSchema import Crop
import imageUtil
import imageCtrl
# saveCrop(self.project,self.imageInfo,self.imageData,(x,y,w,h))
# Save crop, first queries imageInfo to figure out whats the next crop id.
# creates a new crop
def saveCrop(project,imageInfo,imageData,rec):
	# find index of the next crop from the current image being cropped
	i = Crop.select().where(Crop.originalImage == imageInfo.id).count()
	print "The next crop index is: "+str(i)
	name = imageInfo.src.split('.')[0]
	cropName = name+"_crop_"+str(i)+".png"
	cropDir = imageCtrl.getImageDir(imageInfo.src,project)
	print cropDir
	print cropName
	# create crop
	cropData = imageUtil.cropImage(imageData,rec[0],rec[1],rec[2],rec[3])
	# save crop into db
	cropInfo = insertCrop(cropName,imageInfo,rec)
	# save crop image to hd
	imageUtil.saveImage(cropData,cropName,cropDir)
	return cropData,cropInfo
def insertCrop(name,imageInfo,rec):
	return Crop.create(src=name,
		originalImage=imageInfo,
		cropTopLeftX = rec[0],
		cropTopLeftY = rec[1],
		cropBottomRightX = rec[2],
		cropBottomRightY = rec[3]
		)

	'''
	try:
		Crop.create(src=name,
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


(TicketBooking
 .select(
     TicketBooking, 
     Ticket, 
     TicketCategory, 
     Event)
 .join(Ticket)
 .join(TicketCategory)
 .join(Event)
 .where(
     TicketBooking.user_id == user_id,
     TicketBooking.deleted >> None
 ))


	'''