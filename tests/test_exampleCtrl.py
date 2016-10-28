import sys

sys.path.append('../')
# import imageCtrl
from marsSchema import initDB
import projectCtrl
import unittest
import testData
import exampleCtrl
import classCtrl
import imageCtrl
import numpy as np
# from peewee import SqliteDatabase



class test_exampleCtrl(unittest.TestCase):
	def setUp(self):
		# db = SqliteDatabase('../marsj.db')
		initDB()
		# db.connect()
		# db.create_tables([Image,Project,Crop,Class,Example],safe=True)
		self.project = projectCtrl.getProject("Craters")
		classesName,classes = classCtrl.listClassesName(self.project)
		print classesName
		self.craters = classes['craters']
		self.background = classes['background']
		names,self.imagesInfo = imageCtrl.retrieveImages(self.project)
		self.imageInfo = self.imagesInfo[names[4]]
	def test_listExamples(self):
		# pass
		# exampleCtrl.deleteExmplesBySrc("craters_49")
		# exampleCtrl.deleteExmplesBySrc("craters_50")
		# exampleCtrl.deleteExmplesBySrcRange("background",27,50)
		l,obj= exampleCtrl.listExamples(self.background)
		# print l
		# exampleCtrl.deleteExmples(self.background)
	def test_listExamplesFromImage(self):
		size = 128
		cratersInfo,cratersData,cratersClass = exampleCtrl.getExamplesFromImage(self.project,self.craters,size,self.imageInfo)
		backgroundInfo,backgroundData,backgroundClass = exampleCtrl.getExamplesFromImage(self.project,self.background,size,self.imageInfo)

		print np.array(cratersData).shape
		print np.array(backgroundData).shape
		# All examples should be of correct size
	# def 