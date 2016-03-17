import sys
# py -m unittest -v test_MLProject
sys.path.append('../')
import imageCtrl
from marsSchema import Project,Image,Crop,Class,Example
from MLProject import MLProject,extractLinearArray,toGrayScale

import testData
class MLProjectTest(testData.peeweeDBUnitTest):
		def setUp(self):
			testData.peeweeDBUnitTest.setUp(self)
			self.mlProject = MLProject("test")
		'''
		def test_projectInited(self):
			self.assertTrue(self.mlProject.project.name == "test")

		def test_listImagesEmpty(self):
			names = self.mlProject.listImages()
			self.assertEqual(names,[])
		def test_listImages(self):
			testNames = ['a','b','c']
			# insert dummy images
			images = imageCtrl.insertImages(self.mlProject.project, testData.generateTestImages(testNames))
			names = self.mlProject.listImages()
			self.assertEqual(names,testNames)
		'''
		def test_extractLinearArray(self):
			image = testData.generate1DTestImage(100,100)
			arr = self.mlProject.getCropWindow(0,20,20,testCropData=image)

			
			#print image
			# x,y =self.mlProject.getExamples(3)
			# print image[:,0,:]
			# print image.shape
			# print x[0]
			# print "fdc"
			# print arr


		# # pass

'''
	def test_lookup_entry_by_name(self):
		phonebook = self.phonebook
		number = "12343"
		phonebook.add("Tania",number)
		self.assertEqual(number,phonebook.lookup("Tania"))
	def test_missing_entry_raises_KeyError(self):
		phonebook = self.phonebook
		with self.assertRaises(KeyError):
			phonebook.lookup("mising")

	def test_empty_phonebook_is_consistent(self):
		self.assertTrue(self.phonebook.is_consistent())
	
	def test_duplicate_number(self):
		number = "12334"
		self.phonebook.add("bob",number)
		self.phonebook.add("mary",number)
		self.assertFalse(self.phonebook.is_consistent())

	def test_phonebook_with_numbers_that_prefix_other_number_is_consistent(self):
		self.phonebook.add("bob","123")
		self.phonebook.add("mary","12334")
		self.assertFalse(self.phonebook.is_consistent())

	def test_phonebook_adds_names_and_numbers(self):
		self.phonebook.add("sue","1234")
		self.assertIn("sue",self.phonebook.get_names())
		self.assertIn("1234",self.phonebook.get_numbers())
'''