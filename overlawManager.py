import matplotlib.patches as patches


class SmallCrop():
	def __init__(self,x,y,w,h,src):
		self.cropTopLeftX = x
		self.cropTopLeftY = y
		self.cropBottomRightX =w
		self.cropBottomRightY = h
		self.src = src

def collision(patch,x,y):
	px,py = patch.xy

	xcol = (px < x) and (x < px+patch.get_width())
	ycol = (py < y) and (y < py+patch.get_height())
	print "y {0} h {1} ".format(py,patch.get_height() )
	print "xcol "+str(xcol)
	print "ycol "+str(ycol)
	return (xcol and ycol)
def insideRec(cropInfo,px,py,pw,ph):
	x,y = cropInfo.cropTopLeftX,cropInfo.cropTopLeftY
	print "x: {0},y: {1} ".format(x,y)
	w = cropInfo.cropBottomRightX
	h = cropInfo.cropBottomRightY
	xcol = (px < x) and (w+x < pw+px)
	ycol = (py < y) and (y+h < py+ph)
	# print "xcol "+str(xcol)
	# print "ycol "+str(ycol)
	return (xcol and ycol)
	return True
def transformToCropSpace(x,y,crop):
	return SmallCrop(crop.cropTopLeftX-x ,crop.cropTopLeftY-y ,crop.cropBottomRightX,crop.cropBottomRightY,crop.src)
	# return {"cropTopLeftX":crop.cropTopLeftX + x,"cropTopLeftY":crop.cropTopLeftY + y,"cropBottomRightX" :crop.cropBottomRightX,"cropBottomRightY" : crop.cropBottomRightY}

class OverlayManager():
	def __init__(self,marsUI):
		self.patches = []
		self.crops = []
		self.marsUI = marsUI
		self.active = False
	def drawOverlaws(self,crops):
		# match patch leght
		n = len(crops)
		while len(self.patches) < n:
			self.addPatch()
		# hide all patches
		self.setVisible(False)
		# move each patch to correct position
		i = 0
		for key in crops:
			crop = crops[key]
			print "Crop: {0} {1}".format(crop.cropTopLeftX,crop.cropTopLeftY)
			self.crops[i] = crop
			# self.overlayManager.updateCrop(crop)
			patch = self.patches[i]
			patch.xy = crop.cropTopLeftX,crop.cropTopLeftY
			patch.set_width(crop.cropBottomRightX)
			patch.set_height(crop.cropBottomRightY)
			patch.set_visible(True)
			i +=1 
		self.active = True
		self.marsUI.redraw()
		# self.setVisible(True)



	
	def drawOverlawsOnCrop(self,cropInfo,crops):

		x,y = cropInfo.cropTopLeftX,cropInfo.cropTopLeftY
		w = cropInfo.cropBottomRightX
		h = cropInfo.cropBottomRightY
		overlayCrops = {}
		print "Crop location {0} {1} ".format(x,y)
		# transform crops to cropInfo Space
		for key in crops:
			crop = crops[key]
			if(insideRec(crop,x,y,w,h)):
				print 'InsideRec '+crop.src
				overlayCrops[crop.src] = transformToCropSpace(x,y,crop)
		self.drawOverlaws(overlayCrops)
		# return overlayCrops
		# draw crops that are smaller than crop
	def setVisible(self,b):
		self.active = b
		for p in self.patches:
			p.set_visible(b)


	def addPatch(self):
		p = patches.Rectangle(
			(0,0),   # (x,y)
			1,          # width
			1,          # height
			hatch='x',
			fill=False
			)
		self.marsUI.add_patch(p)
		self.patches.append(p)
		self.crops.append(None)
		return p

	def click(self,x,y,lock):
		if(lock.adquire('SmallCrop')==False):
			return
		if(self.active==False):
			lock.release()
			return
		print "check for collision "+str(x)
		i=0
		for i in range(len(self.patches)):
			p = self.patches[i]
			if(p.get_visible()):
				print 'Patch {0} is selectable'.format(self.crops[i].src)
				if(collision(p,x,y)):
					crop = self.crops[i]
					print "collision with patch "+crop.src
					self.marsUI.loadCrop(crop)
					x,y = crop.cropTopLeftX,crop.cropTopLeftY
					print "Crop location in DB {0} {1} ".format(x,y)
					return 
					# print "{0} {1} --> {2} {3} {4} {5} ".format(x,y,crop.cropTopLeftX,crop.cropTopLeftY,crop.cropBottomRightX,crop.cropBottomRightY)
					# collision
					# print "collision with "+crop.src
		lock.release()

class TagOverlayManager(OverlayManager):
	def addPatch(self):
		p = patches.Rectangle(
			(0,0),   # (x,y)
			1,          # width
			1,          # height
			hatch='//',
			fill=False
			)
		self.marsUI.add_patch(p)
		self.patches.append(p)
		self.crops.append(None)
		return p
