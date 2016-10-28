from marsSchema import Crater
class CraterDB:
	def __init__(self,rawCraterDB):
		self.imageInfo = rawCraterDB.imageInfo 
		self.lat = rawCraterDB.lat  
		self.lon = rawCraterDB.lon  
		self.hs = rawCraterDB.hs  
		self.D2 = rawCraterDB.D2  
		self.hr = rawCraterDB.hr  
		self.aRepose = rawCraterDB.aRepose  
		self.lemp = rawCraterDB.lemp  
		self.lema = rawCraterDB.lema  
		self.bump1_xc 	= rawCraterDB.bump1_xc   
		self.bump1_yc 	= rawCraterDB.bump1_yc   
		self.bump1_w 	= rawCraterDB.bump1_w   
		self.bump2_xc 	= rawCraterDB.bump2_xc   
		self.bump2_yc 	= rawCraterDB.bump2_yc   
		self.bump2_w 	= rawCraterDB.bump2_w   
		self.bump3_xc 	= rawCraterDB.bump3_xc   
		self.bump3_yc 	= rawCraterDB.bump3_yc   
		self.bump3_w 	= rawCraterDB.bump3_w   
		self.bump4_xc 	= rawCraterDB.bump4_xc   
		self.bump4_yc 	= rawCraterDB.bump4_yc   
		self.bump4_w	= rawCraterDB.bump4_w
	def getEigenCraterArray(self):
		return [
			self.hs,
			self.D2,
			self.hr,
			self.aRepose,
			self.lemp,
			self.lema,
			self.bump1_xc,
			self.bump1_yc,
			self.bump1_w,
			self.bump2_xc,
			self.bump2_yc,
			self.bump2_w,
			self.bump3_xc,
			self.bump3_yc,
			self.bump3_w,
			self.bump4_xc,
			self.bump4_yc,
			self.bump4_w]

def insertCrater(imageInfo,pds,crater,bumps):
	print imageInfo
	lat,lon = pds.getLatLonFromCenter(crater.x,crater.y)
	return Crater.create(
		imageInfo=imageInfo,
		lat = lat, 
		lon = lon, 
		hs = crater.hs, 
		D2 = crater.D2, 
		hr = crater.hr, 
		aRepose = crater.aRepose, 
		lemp = crater.lemp, 
		lema = crater.lema, 
		bump1_xc 	= bumps [ 0 ],
		bump1_yc 	= bumps [ 1 ],
		bump1_w 	= bumps [ 2 ],
		bump2_xc 	= bumps [ 3 ],
		bump2_yc 	= bumps [ 4 ],
		bump2_w 	= bumps [ 5 ],
		bump3_xc 	= bumps [ 6 ],
		bump3_yc 	= bumps [ 7 ],
		bump3_w 	= bumps [ 8 ],
		bump4_xc 	= bumps [ 9 ],
		bump4_yc 	= bumps [ 10 ],
		bump4_w 	= bumps [ 11 ]
		)
import numpy as np
def getCraters():
	craters =None
	try:
		craters = Crater.select()# .aggregate_rows()
	except Crater.DoesNotExist:
		print "bark bark"
	arrayCraters = None
	for crater in craters:
		craterDB = CraterDB(crater)
		flatCrater = craterDB.getEigenCraterArray()
		np.vstack
		if(arrayCraters == None):
			arrayCraters = flatCrater
		else:
			arrayCraters= np.vstack((arrayCraters,flatCrater))

	print arrayCraters
	return arrayCraters

