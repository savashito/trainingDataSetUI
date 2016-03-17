from marsSchema import Class,initDB
from projectCtrl import getProject

def insertClass(name,project):
	Class.create(name = name,
		project=project)


def listClassesName(project):
	_class = Class.select()
	l = []
	classes = {}
	for p in _class:
		# print "Class: {0}".format(p.name)
		l.append(p.name)
		classes[p.name]=p
	return l,classes

def getClass(name):
	return Class.select().where(Class.name == name).get()

def getExampleSizes(_class):
	return [16,32,64,128]

# initDB()
# cratersProject = getProject("Craters")
# insertClass("craters",cratersProject)

# l = listClassesName(cratersProject)
# print l