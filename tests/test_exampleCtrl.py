import sys

sys.path.append('../')
# import imageCtrl
from marsSchema import initDB
import projectCtrl
import unittest
import testData
import exampleCtrl
import classCtrl
from peewee import SqliteDatabase



class test_exampleCtrl(unittest.TestCase):
	def setUp(self):
		db = SqliteDatabase('../marsj.db')
		initDB(db)
		# db.connect()
		# db.create_tables([Image,Project,Crop,Class,Example],safe=True)
		self.project = projectCtrl.getProject("Craters")
		classesName,classes = classCtrl.listClassesName(self.project)
		print classesName
		self.craters = classes['craters']
		self.background = classes['background']

	def test_listExamples(self):
		# pass
		# exampleCtrl.deleteExmplesBySrc("craters_49")
		# exampleCtrl.deleteExmplesBySrc("craters_50")
		exampleCtrl.deleteExmplesBySrcRange("background",27,50)
		l,obj= exampleCtrl.listExamples(self.background)
		print l
		# exampleCtrl.deleteExmples(self.background)
