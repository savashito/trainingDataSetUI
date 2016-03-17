import matplotlib.pyplot as plt
import numpy as np
from skimage import filters
from scipy import ndimage

import matplotlib.pyplot as plt
from skimage import measure
def initConnectedComponentsData():
	n = 20
	l = 256
	im = np.zeros((l, l))
	points = l * np.random.random((2, n ** 2))
	# print points
	im[(points[0]).astype(np.int), (points[1]).astype(np.int)] = 1
	im = filters.gaussian_filter(im, sigma=l / (4. * n))
	blobs = im > im.mean()
	return blobs

def testConnectedComponnets():

	all_labels = measure.label(blobs)
	blobs_labels = measure.label(blobs, background=0)
	centers = ndimage.measurements.center_of_mass(blobs_labels)	
	print blobs_labels
	print centers
	# print centers
	'''
	plt.figure()
	plt.imshow(blobs)

	plt.figure()
	plt.imshow(im)
	plt.figure()
	plt.imshow(all_labels)
	plt.figure()
	plt.imshow(blobs_labels)
	plt.show()
	'''
def initCentroids():
	b = np.array(([0,1,0,3],
	              [0,1,0,3],
	              [0,0,0,0],
	              [2,0,4,4],
	              [2,0,4,4]))
	return b
def getCentroids(blobs):
	max = np.max(blobs)
	# print max
	arr = range(1,max+1)
	lbl = ndimage.label(blobs)[0]
	return ndimage.measurements.center_of_mass(blobs, lbl, arr)

def plotCircles(img,circles):
	fig, ax = plt.subplots()
	ax.imshow(img)
	for i in range(len(circles)):
		c = circles[i]
		circle1=plt.Circle((c[1],c[0]),2,color='r')
		fig.gca().add_artist(circle1)
	
	plt.show()

blobs = measure.label(initConnectedComponentsData(), background=0)
# blobs = initCentroids()
circles = getCentroids(blobs)
# print circles
plotCircles(blobs,circles)
