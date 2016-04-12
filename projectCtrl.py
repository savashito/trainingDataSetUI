from marsSchema import Project,initDB
import peewee
import os
from debugUtil import debug


def insertProject(name):
	return Project.create(name = name,
		outputImageFolder="/Users/rodrigosavage/Documents/software/python/dbTutorial/marsML/images",
		lastLoadedFolder="/Users/rodrigosavage/Documents/software/python/dbTutorial/marsML")

def listProjects():
	projects = Project.select()
	for p in projects:
		print "Project: {0}".format(p.name)

def updateOutputImageFolder(project):
	# print(os.path.dirname(__file__))
	project.outputImageFolder = os.path.dirname(__file__)+os.sep+"images"
	# print project.outputImageFolder
	project.save()
def getProject(name):
	project = None
	try:
		project = Project.select().where(Project.name == name).get()
	except peewee.DoesNotExist as e:
		print e
		print "Creating new project"
		project = insertProject(name)
		print "created project "+project.name
	debug ("Project %s loaded successfuly"%name)
	# print "miauu"
	# print project.get()
	return project

def updateLastLoadedFolder(proj,path):
	return ""

# def initTestProject():
	# print "creating test Project"

# initDB()
# print getProject("Craters").name
#  listProjects()
# insertProject("Craters")
#insertProject("Mars 2016")