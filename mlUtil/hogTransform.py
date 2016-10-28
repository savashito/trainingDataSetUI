import numpy as np
import cv2
# from matplotlib import pyplot as plt

SZ=20
bin_n=16
affine_flags = cv2.WARP_INVERSE_MAP|cv2.INTER_LINEAR

def deskew(img):
	m = cv2.moments(img)
	if abs(m['mu02']) < 1e-2:
		return img.copy()
	skew = m['mu11']/m['mu02']
	M = np.float32([[1, skew, -0.5*SZ*skew], [0, 1, 0]])
	img = cv2.warpAffine(img,M,(SZ, SZ),flags=affine_flags)
	return img

def hog(img):

	gx = cv2.Sobel(img, cv2.CV_32F, 1, 0)
	gy = cv2.Sobel(img, cv2.CV_32F, 0, 1)
	mag, ang = cv2.cartToPolar(gx, gy)
	# # # print gx
	# plt.imshow(gx)
	# plt.figure()
	# plt.imshow(gy)
	# plt.figure()
	# plt.imshow(img)
	# plt.show()
	# return
	# quantizing binvalues in (0...16)
	bins = np.int32(bin_n*ang/(2*np.pi))
	aShape,bShape = bins.shape
	aShape,bShape = aShape/2,bShape/2
	half = aShape
	# print np.array(ang)
	# print np.array(bins)
	# print "binsShape "+str(bins.shape)
	# Divide to 4 sub-squares
	bin_cells = bins[:half,:half], bins[half:,:half], bins[:half,half:], bins[half:,half:]
	# print "bins_celssShape "+str(np.array(bin_cells).shape)
	mag_cells = mag[:half,:half], mag[half:,:half], mag[:half,half:], mag[half:,half:]
	hists = [np.bincount(b.ravel(), m.ravel() ,minlength=bin_n) for b, m in zip(bin_cells, mag_cells)]
	hist = np.hstack(hists)
	# print hist.shape
	return hist

