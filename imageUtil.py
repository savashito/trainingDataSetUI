import cv2
import matplotlib.image as mpimg
import os

def loadImage(str):
	image = cv2.imread(str)
	# calc aspect ratio
	names = str.split('/')
	name = names[len(names)-1]
	return image,name

def loadImageForDisplay(str):
	image,name = loadImage(str)
	width = 600
	r = width / image.shape[1]
	dim = (width, int(image.shape[0] * r))
	resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
	return resize,name
def cropImage(image,x,y,w,h):
	print "Crop image {0} {1} {2} {3} ".format(x,y,w,h)
	return image[y:(y+h),x:(x+w)]

def saveImage(img,src,directory):
	# print "{0} {1} {2} ".format(image,src,directory)
	# save image
	if not os.path.exists(directory):
		os.makedirs(directory)
	filename = "{0}/{1}".format(directory,src)
	print "Saving image in "+filename
	cv2.imwrite(filename, img)

