import cv2
import matplotlib.image as mpimg
import os

def loadImage(str):
	image = cv2.imread(str)
	# calc aspect ratio
	width = 600
	r = width / image.shape[1]
	dim = (width, int(image.shape[0] * r))
	resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
	# return mpimg.imread(str)
	#cropped = resized[0:170, 0:540]
	names = str.split('/')
	name = names[len(names)-1]
	return resized,name
def cropImage(image,x,y,w,h):
	if(w<0):
		x = x + w
		w = -w
	if(h<0):
		y = y +h
		h=-h
	return image[y:(y+h),x:(x+w)]

def saveImage(img,src,directory):
	# print "{0} {1} {2} ".format(image,src,directory)
	# save image
	if not os.path.exists(directory):
		os.makedirs(directory)
	filename = "{0}/{1}".format(directory,src)
	print "Saving image in "+filename
	cv2.imwrite(filename, img)

