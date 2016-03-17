import unittest
import sys
sys.path.append('../')
import projectCtrl
from marsSchema import Project,Image
import peewee
from playhouse.test_utils import test_database

test_db = peewee.SqliteDatabase(':memory:')

class test_projectCtrl(unittest.TestCase):
	# def setUp(self):
		# self.mlProject = MLProject("test")
	def test_insertProject(self):
		 with test_database(test_db, (Project,Image),create_tables=True):
		 	proj =projectCtrl.insertProject("rod")
		 	 # projectCtrl.getProject("rod")
		 	self.assertEqual ( proj.name , "rod")
	def test_getExistingProject(self):
		 with test_database(test_db, (Project,Image)):
		 	projectCtrl.insertProject("rod")
		 	proj = projectCtrl.getProject("rod")
		 	self.assertEqual ( proj.name , "rod")
	def test_getNonExistingProject(self):
		 with test_database(test_db, (Project,Image)):
		 	proj = projectCtrl.getProject("rod")
		 	self.assertEqual ( proj.name , "rod")
