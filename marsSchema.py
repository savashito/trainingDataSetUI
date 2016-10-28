from peewee import *

# db = SqliteDatabase('E:\\Savage\\craterRepo\\svmCraters\\trainingDataSetUI\\'+'mars.db')
db = MySQLDatabase("mars",user="root",passwd="rtopdfrtio",  host='192.168.5.67')
class BaseModel(Model):
	class Meta:
		database = db

class Project(BaseModel):
	name = CharField(unique=True)
	outputImageFolder = CharField()
	lastLoadedFolder = CharField(null=True)
	# classes = ForeignKeyField(Class)
	# Images = ForeignKeyField(Image)

class Image(BaseModel):
	src = CharField(unique=True)
	longitud = FloatField()
	latitide = FloatField()
	resolution = FloatField() # meters per pixel
	metadata = CharField(null=True)
	project = ForeignKeyField(Project)
	class Meta:
	 	order_by = ('src',)

class Crop(BaseModel):
	src = CharField(unique=True)
	originalImage = ForeignKeyField(Image)
	cropTopLeftX = IntegerField()
	cropTopLeftY = IntegerField()
	cropBottomRightX = IntegerField()
	cropBottomRightY = IntegerField()

class Class(BaseModel):
	name = CharField(unique=True)
	# description = TextField(null=True)
	project = ForeignKeyField(Project)
	# examples = ForeignKeyField(Example)

class Example(BaseModel):
	_class = ForeignKeyField(Class)
	src = CharField(unique=True)
	parentCrop = ForeignKeyField(Crop)
	topLeftX = IntegerField()
	topLeftY = IntegerField()
	bottomRightX = IntegerField()
	bottomRightY = IntegerField()

class Crater(BaseModel):
	imageInfo = CharField()# ForeignKeyField(Image)
	lat = FloatField()
	lon = FloatField()
	hs = FloatField()
	D2 = FloatField()
	hr = FloatField()
	aRepose = FloatField()
	lemp = FloatField()
	lema = FloatField()
	bump1_xc = FloatField()
	bump1_yc = FloatField()
	bump1_w = FloatField()
	bump2_xc = FloatField()
	bump2_yc = FloatField()
	bump2_w = FloatField()
	bump3_xc = FloatField()
	bump3_yc = FloatField()
	bump3_w = FloatField()
	bump4_xc = FloatField()
	bump4_yc = FloatField()
	bump4_w = FloatField()
	# [0, 0.0, 0.25*4,3.1415, 0.0, 0.25*4,3*3.1415/2.0, 0.0, 0.25*4,3.1415/2.0, 0.0, 0.25*4]
def initDB(dbIn = None):
	# if(dbIn!=None):
	# 	print "using dbin"
	# 	dbIn.connect()
	# 	dbIn.create_tables([Image,Project,Crop,Class,Example],safe=True)
	# else:
	db.connect()
	# db.create_tables([Image,Project,Crop,Class,Example],safe=True)
	db.create_table(Crater,safe=True)
	print "MySQLDatabase Initialized"

	return db
	# listImages = createTestImages()
	# insertImages(listImages)
	# retrieveImages()
# init()

	

