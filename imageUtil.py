import cv2
import matplotlib.image as mpimg
import os
import numpy as np
import matplotlib.pyplot as plt

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

def displayImage(img):
	fig, ax = plt.subplots()
	ax.imshow(img)
	# plt.title(self.cropInfo.src)
	plt.show()
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
import struct
def saveRawFloatImage(img,src,directory):
	print "saveRawFloatImage",img.shape
	newFileBytes = [img.shape[0], img.shape[1]]
	# make file
	newFile = open (directory+os.sep+src, "wb")
	# write to file
	bytes = struct.pack('i'*len(newFileBytes), *newFileBytes)
	flatArray = img.ravel()/255.0
	print flatArray
	# exit()
	bytes += struct.pack('f'*len(flatArray), *flatArray)
	newFile.write(bytes)
	newFile.close()
	# if not os.path.exists(directory):
	# 	os.makedirs(directory)
	# filename = "{0}{2}{1}".format(directory,src,os.sep)
	# print "Saving image in "+filename
	# cv2.imwrite(filename, img)


kernel = np.ones((5,5),np.uint8)
def openning(img):
	return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel,iterations = 4)
def closing(img):
	return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

def clean(img):
	return openning(img)

from skimage.measure import profile_line


def testImg():
	x = np.array([[1, 1, 1, 2, 2, 2]])
	img = np.vstack([np.zeros_like(x), x, x, x, np.zeros_like(x)])
	return img

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return np.array((x, y))
def distance(p1,p2):
	pd = p1-p2
	return np.linalg.norm(pd)
# import imageUtil
from pythonMorphologyUI.meloshTest import plotCraterProfile
import scipy.stats as st

def getConfidenceInterval(mean,std,n,confidence):
	c = confidence
	a = st.norm.interval(c, loc=mean, scale=std/np.sqrt(n))
	return mean-a[0]
	# o = 1-(1-confidence)
	# o = st.norm.ppf(o)
	# return mean -o*std/np.sqrt(n)

def plotProfiles(crater,bumps,cropDTM,file_name=None):
	print "TaniaJojo"
	hg = crater.getGroundLevelHeight() # height of ground
	print "hg",hg
	start_point =  np.array((crater.y,crater.x))
	print (crater.y,crater.x)

	# (670,0)
	# norm_vec = start_point/np.linalg.norm(start_point)
	# print norm_vec,start_point
	# return
	line_x,line_y = 0,0
	lt_y = None
	# lt_x = None
	lt_y_interp = None
	generated_profile_y_array_interp = None
	st = 0 #/2 #np.pi# 3*np.pi/2
	thetas = np.arange(0,np.pi*2,.5)

	for theta in thetas:

		end_point = start_point+pol2cart(crater.D2*2.6,theta+np.pi/2) # np.pi/2)
		# print crater.getTransformRadious(theta)
		# v = end_point-start_point
		# v = v /np.linalg.norm(v)
		d = distance(start_point,end_point)
		line_y = profile_line(cropDTM, start_point, end_point)+hg
		# line_y = profile_line(cropDTM, start_point+v*0, end_point)+hg
		n_pts = line_y.shape[0]
		line_x_flat = np.linspace(0.0,d,n_pts)
		line_x = np.linspace(0.0,d,n_pts) # /crater.getTransformRadious(theta)
		# plt.figure(2)
		# plt.plot(line_x_flat,line_y)
		plt.figure(1)
		# plt.plot(line_x,line_y)
		l, = plt.plot(line_x,line_y)
		
		## Error!!
		profile_generated_x,profile_generated_y = plotCraterProfile(l,crater,bumps,theta)
		###

		line_y_interp = np.interp(line_x_flat, line_x, line_y)
		generated_profile_y_interp = np.interp(line_x_flat, profile_generated_x, profile_generated_y)
		# l=0
		# plotCraterProfile(l,crater)
		if(lt_y==None):
			# lt_x = line_x
			lt_y  = line_y
			lt_y_interp  = line_y_interp
			generated_profile_y_array_interp  = generated_profile_y_interp
			# get interpoled values to match all arrays for averaging
		else:
			# print lt_y.shape,line_y.shape
			lt_y = np.vstack((lt_y,line_y))
			lt_y_interp  = np.vstack((lt_y_interp,line_y_interp))
			generated_profile_y_array_interp  = np.vstack((generated_profile_y_array_interp,generated_profile_y_interp))


	# plt.show()

			# lt_x = np.vstack((lt_x,line_x))
		# print lt_y.shape
		# print line_y.shape
	# lt_y = np.array(line_y)
	# return lt_x,lt_y
	# print lt_y.shape
	# l_mean = np.mean(lt_y,axis=0)
	# l_std = np.std(lt_y,axis=0)


	l_mean_interp = np.mean(lt_y_interp,axis=0)
	l_std_interp = np.std(lt_y_interp,axis=0)
	generated_mean_interp = np.mean(generated_profile_y_array_interp,axis=0)
	generated_std_interp = np.std(generated_profile_y_array_interp,axis=0)
	# print "lens ",len(thetas),len(lt_y_interp),len(l_mean_interp) 
	confidence = getConfidenceInterval(l_mean_interp,l_std_interp,len(lt_y_interp),0.95)
	confidence_generated = getConfidenceInterval(generated_mean_interp,generated_std_interp,len(lt_y_interp),0.95)
	# print "confidence"
	# print l_std_interp
	# print confidence
	# print l_mean.shape
	# print crater.D2
	# print start_point,end_point
	# print cropDTM.shape
	
	# print n_pts
	# print d
	
	# print line_x.shape,line_y.shape
	# return
	plt.figure(2)
	# plt.clf()
	plt.xlim([0,crater.D2*2.4])
	l = plt.errorbar(line_x,l_mean_interp, confidence,alpha=1,color='red',label="95% confidence interval profile crater from DTM ")
	le = plt.errorbar(line_x,generated_mean_interp, confidence_generated,alpha=.3,color='blue',label="95% confidence interval generated crater")
	plt.xlabel('lenght [m]')
	plt.ylabel('height [m]')

	# plt.errorbar(line_x,l_mean, l_std, linestyle='None', marker='^')
	plt.plot(line_x,l_mean_interp,lw=2, color='blue',alpha=.7)
	plt.plot(line_x,generated_mean_interp,lw=2, color='red',alpha=.7)
	

	# l, = plt.plot(line_x,l_mean_interp,lw=2, color='black',alpha=.7,label="MCMC fitted profile crater")
	plt.legend(handles=[le, l],loc=4)
	# plt.show()
	# return
	# plotCraterProfile(l,crater)
	# # plt.figure(2)
	# # l, = plt.plot(line_x,l_mean,lw=6, color='black',alpha=.5)
	# # plotCraterProfile(l,crater)
	# plt.figure(1)
	# plt.xlim([0,crater.D2*2.4])
	# plt.errorbar(line_x,l_mean_interp, l_std_interp, linestyle='None', marker='^')
	# # l, = plt.plot(line_x,l_mean_interp,lw=6, color='red',alpha=.5)
	# l, = plt.plot(line_x,l_mean,lw=6, color='black',alpha=.5)
	# plotCraterProfile(l,crater)
	# plt.xlabel('lenght [m]')
	# plt.ylabel('height [m]')

	# save the plots
	if(file_name!=None):
		plt.figure(2)
		plt.savefig(file_name+"_mcmc_vs_std.png")
		plt.savefig(file_name+"_mcmc_vs_std.svg")
		plt.figure(1)
		plt.savefig(file_name+"_crater_profiles.png")
		plt.savefig(file_name+"_crater_profiles.svg")
	plt.show()
	# print n_pts

	# print "bark"
	# return line_x,line_y
'''
img = testImg()
plt.imshow(img)
plt.show()
print img

array = profile_line(img, (2, 1), (2, 4))
print array
array = profile_line(img, (1, 0), (2, 5), cval=69)
print array
'''



# def rotateImage(image, angle):
# 	print "rotateImage "+angle
# 	return image
	# image_center = tuple(np.array(image.shape)/2)
	# rot_mat = cv2.getRotationMatrix2D(image_center,angle,1.0)
	# result = cv2.warpAffine(image, rot_mat, image.shape,flags=cv2.INTER_LINEAR)
	# return result