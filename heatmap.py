
import matplotlib.pyplot as plt
import numpy as np
import time
import sys
sys.path.append('tutorials')
import connectedComponnets as CC

class Heatmap:
	def __init__(self,clfs,mlProject):
		self.clfs = clfs
		self.mlProject = mlProject
		# print size
		# window = mlProject.getCropWindow(size,1116.0,6.0)
		# print clfs[size].predict_proba(window)[0,0]
	def generate(self,size,overlapPercent = 0.001):
		# size = 3
		# overlapPercent = 0.90
		
		clf = self.clfs[size]
		mlProject = self.mlProject
		cropW,cropH =  mlProject.getCropShape()[0],mlProject.getCropShape()[1]

		windowW,windowH = mlProject.getWindowSize(size)
		print windowW
		dx = np.around(windowW*(1-overlapPercent))
		heatmapW = int(np.floor((cropW-windowW)/dx))
		heatmapH = int(np.floor((cropH-windowH)/dx))
		# heatmapArray = np.zeros((heatmapW,heatmapH))
		self.heatmapArray = np.zeros((cropW,cropH))
		# crop = mlProject.getCrop()
		start = time.time()
		for y in range(heatmapH):
			for x in range(heatmapW):
				xCrop,yCrop = x*dx,y*dx
				# get window
				# print x,y,heatmapW
				# print 
				window = mlProject.getCropWindow(size,xCrop,yCrop)
				#window = mlProject.getCropWindow(size,1116.0,6.0)
				#print window.shape
				# print window.shape
				# window = window.reshape(1, -1)
				# print window.shape
				# print clf.predict_proba(window)
				# return 
				#print clf.predict_proba(window)[0,0]
				# return
				# return
				
				if(clf.predict_proba(window)[0,0] < 0.5):
					self.setHeatmapArray(xCrop,yCrop,windowW,0)
					# heatmapArray[x][y] = 0 
				else :
					self.setHeatmapArray(xCrop,yCrop,windowW,1)
			print xCrop,yCrop,self.heatmapArray[x][y]

					# heatmapArray[x][y] = 1 
		end = time.time()
		print "took ",(end - start),"for ",heatmapH*heatmapW
				# np.max( (0.5,clf.predict_proba(window)[0,0]) )
		print self.heatmapArray.shape
		# print np.max(heatmapArray)
		# plt.imshow(heatmapArray)

		# plt.title(self.cropInfo.src)
		# plt.show()
		# self.heatmapArray = heatmapArray
		# print heatmapArray.shape
		# print cropW,cropH
		# print dx
	def getCentroids(self):
		blobs = CC.getBlobs(self.heatmapArray) 
		circles = CC.getCentroids(blobs)
		# CC.plotCircles(self.heatmapArray,circles)
		return circles

	def setHeatmapArray(self,x,y,size,value):
		for j in range(size):
			for i in range(size):
				self.heatmapArray[x+i,y+j] += value
	def plot(self):
		self.mlProject.displayCrop(self.heatmapArray)
	def show(self):
		plt.show()

