import cv2
import matplotlib.image as mpimg
import os
import numpy as np
# import numpy as np
def loadImage(imgFullName):
	# print imgFullName
	image = cv2.imread(imgFullName)
	# print image.shape
	# exit()
	# calc aspect ratio
	names = imgFullName.split(os.sep)
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
def rotateImage(image, angle):
	try:
		image_center = ((image.shape[0]-1)/2.0,(image.shape[1]-1)/2.0)
		# print (8,8)
		# print image_center
		rot_mat = cv2.getRotationMatrix2D(image_center,angle,1.0)
		# print rot_mat.shape
		result = cv2.warpAffine(image, rot_mat, (image.shape[0],image.shape[1]),flags=cv2.INTER_LINEAR)
		return result

	except  Exception as e:
		import traceback
		traceback.print_exc()
		# traceback.print_tb()
	return 
def saveImage(img,src,directory):
	# print "{0} {1} {2} ".format(image,src,directory)
	# save image
	if not os.path.exists(directory):
		os.makedirs(directory)
	filename = "{0}{2}{1}".format(directory,src,os.sep)
	print "Saving image in "+filename
	cv2.imwrite(filename, img)



# def rotateImage(image, angle):
# 	print "rotateImage "+angle
# 	return image
	# image_center = tuple(np.array(image.shape)/2)
	# rot_mat = cv2.getRotationMatrix2D(image_center,angle,1.0)
	# result = cv2.warpAffine(image, rot_mat, image.shape,flags=cv2.INTER_LINEAR)
	# return result