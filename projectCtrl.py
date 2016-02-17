from marsSchema import Project,initDB

def insertProject(name):
	Project.create(name = name,
		outputImageFolder="/Users/rodrigosavage/Documents/software/python/dbTutorial/marsML/images",
		lastLoadedFolder="/Users/rodrigosavage/Documents/software/python/dbTutorial/marsML")

def listProjects():
	projects = Project.select()
	for p in projects:
		print "Project: {0}".format(p.name)

def getProject(name):
	project = Project.select().where(Project.name == name)
	return project.get()

def updateLastLoadedFolder(proj,path):
	return ""

# initDB()
# print getProject("Craters").name
#  listProjects()
# insertProject("Craters")
#insertProject("Mars 2016")