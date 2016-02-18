from Tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, StringVar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ttk
from tkFileDialog import askopenfilename
import matplotlib.pyplot as plt
# import imageUtil
# load dbstuff
from marsSchema import initDB
import imageCtrl
import imageUtil
import cropCtrl
from projectCtrl import getProject,updateLastLoadedFolder
import classCtrl
import exampleCtrl

from matplotlib.backend_bases import cursors
from matplotlib.widgets import Cursor
import matplotlib.backends.backend_tkagg as tkagg
import matplotlib.patches as patches
import math

def getLen(x):
	return x[1]-x[0]

class Square():
	def __init__(self,marsUI,ax,x,y,w,h):
		p = patches.Rectangle(
			(x,y),   # (x,y)
			w,          # width
			h,          # height
			hatch='x',
			fill=False
			)
		self.patch = p
		p.set_visible(False)
		ax.add_patch(p)
		self.w,self.h = w,h
		self.x,self.y = x,y
		self.marsUI= marsUI
		self.ax = ax
		self.cropIndex = 0
		self.cropping = [self.notCropping,self.croppingCursor,self.cropFirstPoint]
	def updateAx(self,ax):
		self.ax = ax
		ax.add_patch(self.patch)
	def notCropping(self,x,y):
		self.patch.set_visible(False)
		return 

	def croppingCursor(self,x,y):
		'''
		w = 0.1*getLen(self.ax.get_xlim())
		h = 0.1*getLen(self.ax.get_ylim())
		self.scale(w,h)
		self.patch.xy = x,y #(x-self.w/2),(y-self.h/2)
		self.patch.set_visible(True)
		'''
		return

	def cropFirstPoint(self,x,y):
		self.patch.xy = self.x,self.y
		self.scale(x-self.x,y-self.y)
		self.patch.set_visible(True)
		return

	def move(self,canvas,x,y):
		self.canvas = canvas
		self.cropping[self.cropIndex](x,y)
		# Redraw
		# canvas.draw()
	def scale(self,w,h):
		self.w,self.h = w,h
		self.patch.set_width(w)
		self.patch.set_height(h)
	def click(self,x,y):
		if(self.cropIndex==1):
			self.x,self.y = x,y
			self.cropIndex = 2
		elif(self.cropIndex==2):
			self.endCrop()
	def startCrop(self):
		self.cropIndex = 1
	def endCrop(self):
		self.marsUI.crop(self.x,self.y ,self.w,self.h)
		self.cropIndex = 0

class TagSquare():
	def __init__(self,marsUI):
		self.marsUI = marsUI
		self.tagIndex = 0
		self.tag = [self.notTagging,self.taggingCursor]
		self.p1 = self.addPatch()
		self.p2 = self.addPatch()
		self.p3 = self.addPatch()
		self.p4 = self.addPatch()
		self.r = 0
		self.scaleX,self.scaleY = 0.1,0.1
		self.setVisibilityPatch(False)
		self.ang = math.pi/4
		
		self.scaleIncrement = 0.01
	def addPatch(self):
		p = patches.Rectangle(
			(0,0),   # (x,y)
			1,          # width
			1,          # height
			hatch='x',
			fill=False
			)
		self.marsUI.add_patch(p)
		return p
	def getPatchRec(self,p):
		w = p.get_width()
		h = p.get_height()
		x,y = p.xy
		return [x,y,w,h]
	def click(self,x,y):
		if(self.tagIndex==1):
			if(self.marsUI.getSelectedClass()!= None):
				taggedClass = self.marsUI.getSelectedClass()
				print taggedClass.name
				rec1 = self.getPatchRec(self.p1)
				rec2 = self.getPatchRec(self.p2)
				rec3 = self.getPatchRec(self.p3)
				rec4 = self.getPatchRec(self.p4)
				self.marsUI.saveExample(taggedClass,rec1)
				self.marsUI.saveExample(taggedClass,rec2)
				self.marsUI.saveExample(taggedClass,rec3)
				self.marsUI.saveExample(taggedClass,rec4)
				
				# print " tagged "+self.marsUI.getSelectedClass().name
				
				# 
			# self.endTag()
	def notTagging(self,x,y):
		return
	def taggingCursor(self,x,y):
		print "tagging {0} {1}".format(x,y)
		if(x == None):
			return
		w,h = self.marsUI.getCanvasDimensions()
		self.scalePatch(self.scaleX*w,self.scaleY*h)
		self.movePatch(x,y,True)
		return
	def move(self,x,y):
		self.tag[self.tagIndex](x,y)
	def setVisibilityPatch(self,visible):
		self.p1.set_visible(visible)
		self.p2.set_visible(visible)
		self.p3.set_visible(visible)
		self.p4.set_visible(visible)

	def scalePatch(self,w,h):
		self.w,self.h = w,h
		self.p1.set_width(w)
		self.p1.set_height(h)
		self.p2.set_width(w)
		self.p2.set_height(h)
		self.p3.set_width(w)
		self.p3.set_height(h)
		self.p4.set_width(w)
		self.p4.set_height(h)

	def movePatch(self,x,y,center=False):
		# if(center):
			# x,y= x-self.w/2,y-self.h/2
		r = 0.05
		# cos45,sin45 = ,
		rcos,rsin = r*math.cos(self.ang),r*math.sin(self.ang)
		self.p1.xy = x+rcos ,y+rsin
		self.p2.xy = x-self.w-rcos,y-self.h-rsin
		self.p3.xy = x+rcos,y-self.h-rsin
		self.p4.xy = x-self.w-rcos,y+rsin
		self.x,self.y = x,y
	def keyEvent(self,key):
		print key
		if(key == 'q'):
			self.ang += (math.pi/32.0)
			x,y = self.x ,self.y 
			self.movePatch(x,y)
		elif(key == 'w'):
			self.ang -= (math.pi/32.0)
			x,y = self.x ,self.y 
			self.movePatch(x,y)
		elif(key == '+'):

			self.scaleX += self.scaleIncrement
			self.scaleY += self.scaleIncrement
			# x,y = self.x + self.w/2,self.y + self.h/2
			x,y = self.x ,self.y 
			# self.movePatch(0,0,True)
			# self.taggingCursor(self.x,self.y)
			self.taggingCursor(x,y)
		elif(key == '-'):
			x,y = self.x ,self.y 
			self.scaleX,self.scaleY = self.scaleX-self.scaleIncrement,self.scaleY-self.scaleIncrement
			self.taggingCursor(x,y)
			# w,h = self.marsUI.getCanvasDimensions()
			# self.scalePatch(self.scaleX*w,self.scaleY*h)

	def startTag(self):
		if(self.tagIndex ==0):
			self.tagIndex = 1
			self.marsUI.setTextTagButton("Stop tagging")
			# show patching thinggy
			self.setVisibilityPatch(True)
		else:
			selectedClass = self.marsUI.getSelectedClass()
			if(selectedClass!=None):
				self.marsUI.setTextTagButton("Tag "+selectedClass.name)
			else:
				self.endTag()
			self.tagIndex = 0
	def endTag(self):
		self.marsUI.setTextTagButton("Tag class")
		self.setVisibilityPatch(False)
		self.tagIndex = 0
		print "hide setVisibilityPatch"


class OnHover(object):
	def __init__(self,marsUI, c,fig,ax, cursor='hand1'):
		self.ax = ax
		self.cursor = cursor
		self.default_cursor = tkagg.cursord[1]
		self.fig = fig # ax.axes.figure
		self.canvas = c
		self.sqr = Square(marsUI,ax,0.1,0.1,0.4,0.4)
		self.tagSqr = TagSquare(marsUI)
		self.marsUI = marsUI
	def __call__(self, event):
		self.canvas._tkcanvas.focus_set()
		# self.canvas.takefocus = True
		if (event.key!=None):
			self.tagSqr.keyEvent(event.key)
			# return

		# print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(event.button, event.x, event.y, event.xdata, event.ydata)
		elif(event.button==1):
			self.sqr.click(event.xdata, event.ydata)
			self.tagSqr.click(event.xdata, event.ydata)
		elif(event.xdata!=None):
			self.sqr.move(self.canvas,event.xdata, event.ydata)
			self.tagSqr.move(event.xdata, event.ydata)
		self.marsUI.redraw()
	def crop(self):
		self.sqr.startCrop()
	def tag(self):
		print "taggg"
		self.tagSqr.startTag()
		'''
		if(event.button==1):
			canvas.draw()
			print 'click'
		else:
			self.sqr.move(self.canvas,event.xdata, event.ydata)
		print event
		print self.ax
		print self.fig
		print self.canvas
		'''
		# print event
		# inside, _ = self.ax.contains(event)
		# if inside:
		# 	self.sqr.move(self.canvas,event.xdata, event.ydata)
		# 	if(event.button==1):
		# 		print 'click'
		# 	print('Your x and y mouse positions are ', event.xdata, event.ydata)
		# 	tkagg.cursord[0] = self.cursor
		# else:
		# 	tkagg.cursord[0] = self.default_cursor

		# self.canvas.set_cursor(1)

class MarsUI:

	def __init__(self, master):
		self.master = master
		master.title("MarsUI")
		# ImageName labels
		self.lblImageNameText = StringVar()
		self.lblImageNameStatic = Label(master, text="Image: ")
		self.lblImageName = Label(master, textvariable=self.lblImageNameText)
		# Load and crop image buttons
		self.btnLoadImage = Button(master, text="Load image", cursor="plus",command=self.openImageDialog)
		self.btnCropImage = Button(master, text="Crop image", command=self.cropImage)
		
		# class dropdowns
		self.cbxClass = self.addCombobox()
		self.cbxImage = self.addCombobox(self.imageSelected)
		self.cbxCrop = self.addCombobox(self.cropSelected)

		self.lblTagImageText = StringVar()
		self.btnTagImage = Button(master, textvariable=self.lblTagImageText, command=self.tagImage)
		self.setTextTagButton("Tag class")
		# New class text and button
		self.btnAddClass = Button(master, text="Add class", command=self.addClass)
		vcmd = master.register(self.validate)
		self.entClass = Entry(master,width=10,validate="key",validatecommand=(vcmd, '%P'))

		# Display labels # samples
		self.lblClassText = StringVar()
		self.lblClassNegativeText = StringVar()
		self.lblClass = Label(master, textvariable=self.lblClassText)
		self.lblClassBackground = Label(master, textvariable=self.lblClassNegativeText)
		# load db and project
		initDB()
		self.project = getProject("Craters")

		self.updateFields()
		self.updateCbxImages()
		

		# labels for current class and negatives

		# LAYOUT
		# tkagg.cursord[cursors.POINTER] = 'coffee_mug' 
		f,ax = plt.subplots()# plt.figure(1)
		f.tight_layout(pad=0.1) 
		# for item in [f, ax]:
		# 	item.patch.set_visible(False)
		self.canvas = FigureCanvasTkAgg(f, master=self.master)
		self.canvas.get_tk_widget().grid(row=0,column=0,columnspan=12) # .pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
		# cursor
		self.ax = ax
		self.eventManager = OnHover(self,self.canvas,f,ax)
		self.canvas.mpl_connect('button_press_event',self.eventManager)
		self.canvas.mpl_connect('motion_notify_event', self.eventManager)
		self.canvas.mpl_connect('key_press_event', self.eventManager)
		# remove horrible background
		# self.canvas.get_tk_widget().configure(background='black',  highlightcolor='black', highlightbackground='black')

		#ax.config(cursor='hand')
		# cursor = Cursor(ax, useblit=True, color='red', linewidth=2)
		self.canvas.show()
		self.lblImageNameStatic.grid(row=1, column=0, sticky=W)
		self.lblImageName.grid(row=1, column=1, sticky=W)
		
		self.btnLoadImage.grid(row=2, column=1,sticky=W)
		self.btnCropImage.grid(row=2, column=0,sticky=W)

		self.cbxClass.grid(row=8, column=0,pady=10,sticky=W)
		self.cbxImage.grid(row=8, column=2,pady=10,sticky=W)
		self.cbxCrop.grid(row=8, column=3,pady=10,sticky=W)
		self.btnTagImage.grid(row=8, column=1,pady=10,sticky=W)

		self.btnAddClass.grid(row=9, column=1,sticky=W,pady=10)
		self.entClass.grid(row=9, column=0,sticky=W)

		self.lblClassBackground.grid(row=10, column=0,sticky=W,pady=10)
		self.lblClass.grid(row=11, column=0,sticky=W)
		# clean variables
		self.cropInfo,self.cropData,self.imageInfo,self.imageData = None,None,None,None
		self.crops={}
	def saveExample(self,taggedClass,rec):
		# need to crop image
		if(self.cropInfo!=None):
			tagData = imageUtil.cropImage(self.cropData,rec[0],rec[1],rec[2],rec[3])
			exampleCtrl.saveExample(taggedClass,self.project,self.cropInfo,rec,tagData)


	def addCombobox(self,fn=None):
		cbxClass = ttk.Combobox(self.master,width=10)
		cbxClass.state(['readonly'])
		if(fn!=None):
			cbxClass.bind('<<ComboboxSelected>>', fn)
		return cbxClass
	def updateCbxImages(self):
		self.cbxImagesKey,self.images = imageCtrl.retrieveImages(self.project)# ['crater', 'cone', 'background']
		self.cbxImage['values'] = self.cbxImagesKey
	def updateCbxCrop(self,image):
		self.cbxCropKey,self.crops = cropCtrl.retrieveCrops(self.project,image)# ['crater', 'cone', 'background']
		self.cbxCrop['values'] = self.cbxCropKey
	def updateFields(self):
		self.setImageName("")
		self.cbxClassValues,self.classes = classCtrl.listClassesName(self.project)# ['crater', 'cone', 'background']
		self.cbxClass['values'] = self.cbxClassValues

		self.setClassNumber(3)

	def tagImage(self):
		print "Tag"
		self.eventManager.tag()
	def setTextTagButton(self,text):
		self.lblTagImageText.set(text)
	def validate(self, new_text):
		if not new_text: # the field is being cleared
			self.classText = None
			return True
		self.classText = new_text
		# print new_text
		return True
	def addClass(self):
		classCtrl.insertClass(self.classText,self.project)
		print "addClass "+str(self.classText)
		self.updateFields()
	def imageSelected(self,event):
		imageName = self.cbxImage.get()
		imageInfo = self.images[imageName]
		self.imageData,self.imageInfo = imageCtrl.getImage(imageName,self.project,None,imageInfo)
		self.updateImageDisplay()
		# load crop combobox
		self.updateCbxCrop(imageInfo)
		# self.cbxImage 
		print "selected "
	def cropSelected(self,event):
		cropName = self.cbxCrop.get()
		cropInfo = self.crops[cropName]
		print "SelectedCrop "+cropInfo.src
		self.cropData = cropCtrl.getCrop(self.project,self.imageInfo,cropInfo)
		self.cropInfo = cropInfo
		self.updateCropDisplay()
		# load crop combobox
		# self.updateCbxCrop(imageInfo)
	def getPathAndName(self,filename):
		path = filename.split("/")
		name = path[len(path)-1]
		print path
		path = "/".join(path[0:len(path)-1])
		return path,name
	def openImageDialog(self):
		Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing "/Users/rodrigosavage/Documents/software/python/dbTutorial/marsML"
		filename = askopenfilename(message="Load an image",initialdir=self.project.lastLoadedFolder) # show an "Open" dialog box and return the path to the selected file
		# print filename
		if(filename==None or filename == ""):
			return
		path,name = self.getPathAndName(filename)
		
		print "name: "+name
		print "path "+path

		# DB project changes
		updateLastLoadedFolder(self.project,path)
		# DB save image or check existance
		self.imageData,self.imageInfo = imageCtrl.getImage(name,self.project,path)
		print self.imageData
		# self.img = imageUtil.loadImage('testImages/stinkbug.png')
		self.updateImageDisplay()
		# contact db
		
		# path,name = filename.split(":")
		# print "Path {0} name {1} ".format(path,name)
	def updateImageDisplay(self):
		plt.imshow(self.imageData)
		self.canvas.show()
		#Window changes
		self.setImageName(self.imageInfo.src )
	def updateCropDisplay(self):
		plt.imshow(self.cropData)
		self.canvas.show()
		#Window changes
		self.setImageName(self.cropInfo.src )
	def add_patch(self,p):
		self.ax.add_patch(p)
	def getSelectedClass(self):
		selected = self.cbxClass.get()
		if(selected!= ""):
			return self.classes[selected]
	def getCanvasDimensions(self):
		w = getLen(self.ax.get_xlim())
		h = getLen(self.ax.get_ylim())
		return w,h
	def redraw(self):
		self.canvas.draw()
	def cropImage(self):
		self.eventManager.crop()

	def crop(self,x,y,w,h):
		w = int(w)
		h = int(h)
		x = int(x)
		y = int(y)
		print "Crop {0} {1} {2} {3} ".format(x,y,w,h)
		self.cropImg,self.cropInfo = cropCtrl.saveCrop(self.project,self.imageInfo,self.imageData,(x,y,w,h))

		# imageUtil.cropImage(self.img,x,y,w,h)
		plt.imshow(self.cropImg)
		# self.img = cropImg
		self.canvas.show()

		# update the db
		self.crops[self.cropInfo.src]=self.cropInfo
		print "Crop image"
	def setClassNumber(self,number):
		self.lblClassText.set("{0}: {1}".format("Crater",str(number)))
		self.lblClassNegativeText.set("Background: {0}".format(5))
	def setImageName(self,name):
		self.lblImageNameText.set("{0}".format(name))
root = Tk()
my_gui = MarsUI(root)
root.mainloop()


# Error analisys
# analyse error from infer parameters
# compare model A, B and c based on error parameter
# 
# 28  -- 250
# 4   -- 

(24 * 250) /28 