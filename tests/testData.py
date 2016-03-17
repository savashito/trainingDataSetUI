import unittest
import peewee
from playhouse.test_utils import test_database
from marsSchema import Project,Image,Crop,Class,Example
import numpy as np
test_db = peewee.SqliteDatabase(':memory:')
db = test_database(test_db,(Project,Image,Crop,Class,Example),create_tables=True)

class peeweeDBUnitTest(unittest.TestCase):
	def setUp(self):
		db.__enter__()
	def tearDown(self):
		db.__exit__(None, None, None)

def generateTestImages(names):
	images = []
	for name in names:
		images.append({'src':name,'longitud':'1','latitide':'2','resolution':'3'})
	return images

def generate1DTestImage(w,h):
	a = np.arange(w*h).reshape(w,h)
	return np.array([a,a,a]).T