from peewee import *

db = SqliteDatabase('mars.db')

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
	metadata = CharField(null =True)
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



def initDB():
	db.connect()
	db.create_tables([Image,Project,Crop,Class],safe=True)
	print "Database Initialized"
	return db
	# listImages = createTestImages()
	# insertImages(listImages)
	# retrieveImages()
# init()

	
