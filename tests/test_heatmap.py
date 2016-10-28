import sys
# py -m unittest -v test_MLProject
sys.path.append('../')
import heatmap
import testData
import scalarCtrl
import unittest


class HeatmapTest(unittest.TestCase):
	def setUp(self):
		pass
	
	@unittest.skip("demonstrating skipping")
	def testMatrixAddition(self):
		imageData = testData.generate2DTestImage(10,10)
		print imageData
		heatmap.setHeatmapArray(1,1,5,3,imageData)
		# imageData[0,0] = 3
		print imageData

	def test_getWindowFromImage(self):

		imageData = testData.generate2DTestImageIncs(10,10)
		window = scalarCtrl.getWindowFromImage(1,1,5,3,imageData)
		print window