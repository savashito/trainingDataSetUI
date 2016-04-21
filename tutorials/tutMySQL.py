import MySQLdb
from peewee import *
import sys
sys.path.append('../')
# from marsSchema import initDB
# import classCtrl
import projectCtrl
import imageCtrl
import cropCtrl
import classCtrl
import exampleCtrl
db = MySQLDatabase("mars",user="root",passwd="rtopdfrtio") # MySQLdb.connect(passwd="rtopdfrtio",db="mars",user="root")

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

def initMyDB(dbIn = None):
	# if(dbIn!=None):
	# 	print "using dbin"
	# 	dbIn.connect()
	# 	dbIn.create_tables([Image,Project,Crop,Class,Example],safe=True)
	# else:
	# db.connect()
	db.create_tables([Image,Project,Crop,Class,Example],safe=True)
	print "mySQL Database Initialized"
	return db
	# listImages = createTestImages()
	# insertImages(listImages)
	# retrieveImages()


# liteDB = initDB()
#with initMyDB() as myDB:
#projectCtrl.listProjects()


def migrateProjects():
	proj = Project.select()
	if(len(proj)>0):
		print "projects exits"
		return
	projects = projectCtrl.listProjects()
	print projects
	for p in projects:
		Project.create(	name = p.name,
			outputImageFolder = p.outputImageFolder, 
			lastLoadedFolder = p.lastLoadedFolder)
	print "created projects"
def migrateImages(proj):
	images = Image.select()
	print images
	if(len(images)>0):
		print "images exist "
		return
	names,imgsInfo = imageCtrl.retrieveImages(proj)
	for name in imgsInfo:
		imageInfo = imgsInfo[name]
		# print imageInfo
		Image.create(src=imageInfo.src   ,
			longitud=imageInfo.longitud   ,
			latitide=imageInfo.latitide  ,
			resolution=imageInfo.resolution  ,
			metadata =imageInfo.metadata   ,
			id = imageInfo.id,
			project=imageInfo.project   
			)
	print "inserted images "+ str(names)
def migrateCrop(proj):
	crops = Crop.select()
	print crops
	if(len(crops)>0):
		print "crops exist "
		return
	crops = cropCtrl.getAllCrops()
	for crop in crops:
		Crop.create(
			src = crop.src,
			id = crop.id,
			originalImage = crop.originalImage,
			cropTopLeftX = crop.cropTopLeftX,
			cropTopLeftY = crop.cropTopLeftY,
			cropBottomRightX = crop.cropBottomRightX,
			cropBottomRightY = crop.cropBottomRightY)
		print "inserted crop "+crop.src

def migrateClass(proj):
	_class = Class.select()
	print _class
	if(len(_class)>0):
		print "_class exist "
		return
	_classes = classCtrl.getAllClasses()
	for _class in _classes:
		Class.create(
			id = _class.id,
			name = _class.name,
			project = _class.project)
		print "created class "+_class.name

def migrateExample(proj):
	examples = Example.select()
	print examples
	if(len(examples)>0):
		print "examples exist "
		return
	examples = exampleCtrl.getAllExamples()

	for example in examples:
		print "created example "+example.src
		Example.create(
			_class = example._class,
			src = example.src,
			parentCrop = example.parentCrop,
			topLeftX = example.topLeftX,
			topLeftY = example.topLeftY,
			bottomRightX = example.bottomRightX,
			bottomRightY = example.bottomRightY
			)
		print "created example "+example.src

# exit()


def migrate():
	# list projects and insert them
	proj = projectCtrl.getProject("Craters")
	migrateProjects()
	migrateImages(proj)
	migrateCrop(proj)
	migrateClass(proj)
	migrateExample(proj)
	print "migration sucessfuly"
initMyDB()
migrate()

# projects = Project.select()
# print len(projects)
# for p in projects:
# 	print "Project: {0}".format(p.name)



# # with liteDB:
# 	# classCtrl.listClassesName()
# # liteDB.__enter__()

# myDB.__enter__()
# projectCtrl.listProjects()
# myDB.__exit__(None, None, None)

# # 
# # 

