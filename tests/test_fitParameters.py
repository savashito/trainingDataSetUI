import sys
import unittest
sys.path.append('../')
import fitParameters
from sklearn.datasets import load_iris
class fitParametersTest(unittest.TestCase):
	def testFindBestParametersSV(self):
		iris = load_iris()
		X = iris.data
		y = iris.target
		gamma,c,cfl = fitParameters.findBestParametersSV(X,y,disp=False)
		self.assertAlmostEqual(gamma,0.1)
		self.assertAlmostEqual(c,1.0)
		# 'gamma': 0.10000000000000001, 'C': 1.0