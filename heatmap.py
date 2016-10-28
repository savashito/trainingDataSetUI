
import matplotlib.pyplot as plt
import numpy as np
import time
import sys
sys.path.append('tutorials')
sys.path.append('../tutorials')
import connectedComponnets as CC
import imageUtil
from debugUtil import debug
import pdb;
class Heatmap:
	def __init__(self,clfs,mlProject):
		self.clfs = clfs
		self.mlProject = mlProject
		self.heatmapArrayComposite = None
		self.output_name = "./"
		self.output_results_filename = "heatmap_output.txt"
		self.output_results_file = None
		# print size
		# window = mlProject.getCropWindow(size,1116.0,6.0)
		# print clfs[size].predict_proba(window)[0,0]
	def generate(self,size,overlapPercent = 0.1):
		# size = 3
		# overlapPercent = 0.90
		
		clf = self.clfs[size]
		if(clf==None):
			debug("Error! Clasifier is Null")
			exit()
		mlProject = self.mlProject
		cropW,cropH =  mlProject.getCropShape()[0],mlProject.getCropShape()[1]

		windowW,windowH = mlProject.getWindowSize(size)
		print windowW
		dx = np.around(windowW*(1-overlapPercent))
		heatmapW = int(np.floor((cropW-windowW)/dx))+1
		heatmapH = int(np.floor((cropH-windowH)/dx))+1
		# Initialize arrays 
		self.heatmapArray = np.zeros((cropW,cropH))
		self.heatmapContinousArray = np.zeros((cropW,cropH))
		
		start = time.time()
		# window = mlProject.getCropWindow(size,0.0,6.0)
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
				# print clf.predict_proba(window).shape
				# print clf.predict_proba(window)[0,0]
				# exit()
				# return 
				#print clf.predict_proba(window)[0,0]
				# return
				# return
				pred = clf.predict_proba(window)[0,0] 
				setHeatmapArray(xCrop,yCrop,windowW,pred,self.heatmapContinousArray)
				# continue

				if(pred < 0.5):
					setHeatmapArray(xCrop,yCrop,windowW,0,self.heatmapArray)
					# heatmapArray[x][y] = 0 
				else :
					setHeatmapArray(xCrop,yCrop,windowW,1,self.heatmapArray)
				# setHeatmapArray(xCrop,yCrop,windowW,pred,self.heatmapContinousArray)
			print xCrop,yCrop,self.heatmapArray[x][y]


					# heatmapArray[x][y] = 1 
		end = time.time()
		total_time = (end - start)
		print "took ",total_time,"for ",heatmapH*heatmapW
		self.output_results_file.write("window size %dx%d with %f %s Overlap took: %f s\n"%(windowW,windowH,overlapPercent*100,'%',total_time))
		# np.max( (0.5,clf.predict_proba(window)[0,0]) )
		self.compositeMap()
		# plot and save the heat maps
		self.mlProject.displayCrop(self.heatmapArray,self.output_name+"binary_size_%d"%size,suptitle="Threshold: 0.5. Window size %dx%d"%(windowW,windowH))
		self.mlProject.displayCrop(self.heatmapContinousArray,self.output_name+"continous_size_%d"%size,suptitle="Window size %dx%d"%(windowW,windowH))
		# print self.heatmapArray.shape
		# print np.max(heatmapArray)
		# plt.imshow(heatmapArray)

		# plt.title(self.cropInfo.src)
		# plt.show()
		# self.heatmapArray = heatmapArray
		# print heatmapArray.shape
		# print cropW,cropH
		# print dx
	def clearComposite(self):
		self.heatmapArrayComposite=None

	def openOutputfile(self):
		self.output_results_file = open(self.output_name+self.output_results_filename,'w')
	def closeOutputfile(self):
		self.output_results_file.close()
	def generateComposite(self):
		# clear composite
		self.openOutputfile()
		self.clearComposite()
		self.generate(3)
		self.generate(2)
		self.generate(1)
		self.closeOutputfile()
	
	def compositeMap(self):
		if(self.heatmapArrayComposite==None):
			self.heatmapArrayComposite = self.heatmapArray
			self.heatmapContinousArrayComposite = self.heatmapContinousArray
		else:
			self.heatmapArrayComposite += self.heatmapArray
			self.heatmapContinousArrayComposite += self.heatmapContinousArray


	def getCentroids(self,heatMap):
		# heatmap = self.heatmapArrayComposite
		blobs = CC.getBlobs(heatMap) 
		circles = CC.getCentroids(blobs)
		CC.plotCircles(heatMap,circles)
		return circles
	def setOutputName(self,output_name,x,y):
		self.output_name = output_name
	def plotComposite(self):
		self.mlProject.displayCrop(self.heatmapArrayComposite,self.output_name+"binary_composite")
		self.mlProject.displayCrop(self.heatmapContinousArrayComposite,self.output_name+"continous_composite")
		# pdb.set_trace()
		compositeMap = 1.0*(self.heatmapContinousArrayComposite>1.5)
		compositeMap = imageUtil.clean(compositeMap)
		self.compositeMap = compositeMap
		self.mlProject.displayCrop(compositeMap,self.output_name+"composite_final")
		return self.getCentroids(compositeMap)
	def plot(self):
		self.mlProject.displayCrop(self.heatmapArray)
		self.mlProject.displayCrop(self.heatmapContinousArray)
	def show(self):
		plt.show()

def setHeatmapArray(x,y,size,value,array):
	a = (np.ones(size*size)*value).reshape(size,size)

	array[x:x+size,y:y+size] += a
	# for j in range(size):
	# 	for i in range(size):
	# 		array[x+i,y+j] += value