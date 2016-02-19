import matplotlib.patches as patches

def collision(patch,x,y):
	px,py = patch.xy
	xcol = (px < x) and (x < px+patch.get_width())
	ycol = (py < y) and (y < py+patch.get_height())
	# print "xcol "+str(xcol)
	# print "ycol "+str(ycol)
	return (xcol and ycol)
def insideRec(crop,x,y,w,h):
	return True
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
		# move each patch to correct position
		i = 0
		for key in crops:
			print "Crop "
			crop = crops[key]
			self.crops[i] = crop
			# self.overlayManager.updateCrop(crop)
			patch = self.patches[i]
			patch.xy = crop.cropTopLeftX,crop.cropTopLeftY
			patch.set_width(crop.cropBottomRightX)
			patch.set_height(crop.cropBottomRightY)
			i +=1 
		self.marsUI.redraw()
		self.setVisible(True)



	def transformToCropSpace(x,y,crop):
		return {"cropTopLeftX":crop.cropTopLeftX + x,"cropTopLeftY":cropInfo.cropTopLeftY + y,"cropBottomRightX" :cropInfo.cropBottomRightX,"cropBottomRightY" : cropInfo.cropBottomRightY}

	def drawOverlawsOnCrop(self,cropInfo,crops):

		x,y = cropInfo.cropTopLeftX,cropInfo.cropTopLeftY
		w = cropInfo.cropBottomRightX
		
		h = cropInfo.cropBottomRightY
		overlayCrops = {}
		# transform crops to cropInfo Space
		for crop in crops:
			if(insideRec(crop,x,y,w,h)):
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

	def click(self,x,y):
		if(self.active==False):
			return
		print "check for collision "+str(x)
		i=0
		for i in range(len(self.patches)):
			p = self.patches[i]
			if(collision(p,x,y)):
				crop = self.crops[i]
				self.marsUI.loadCrop(crop)
				return 
				# print "{0} {1} --> {2} {3} {4} {5} ".format(x,y,crop.cropTopLeftX,crop.cropTopLeftY,crop.cropBottomRightX,crop.cropBottomRightY)
				# collision
				# print "collision with "+crop.src