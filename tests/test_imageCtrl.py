
import sys

sys.path.append('../')
import imageCtrl
import projectCtrl
import testData



class test_imageCtrl(testData.peeweeDBUnitTest):
	def setUp(self):
		testData.peeweeDBUnitTest.setUp(self)
		self.project = projectCtrl.getProject("test")
	def test_insertImages(self):
		testNames = ['a','b','c']
		images = imageCtrl.insertImages(self.project, testData.generateTestImages(testNames))
		names = []
		for image in images:
			names.append(image.src)
		self.assertEqual(testNames,names)
		# print len(images)