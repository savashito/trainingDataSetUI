import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys
sys.path.append('../')
import mlUtil.hogTransform as hogTransform
img = cv2.imread('digits.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# cells = [np.hsplit(row,100) for row in np.vsplit(img,50)]
# # First half is trainData, remaining is testData
# train_cells = [ i[:50] for i in cells ]
# test_cells = [ i[50:] for i in cells]

# Now we split the image to 5000 cells, each 20x20 size
cells = [np.hsplit(row,100) for row in np.vsplit(gray,50)]
x = np.array(cells)
train = x[:,:50].reshape(-1,20,20)  #.reshape(-1,400).astype(np.float32) # Size = (2500,400)
test = x[:,50:100].reshape(-1,20,20) #.reshape(-1,400).astype(np.float32) # Size = (2500,400)
# deskX = [map(deskew,trainImg) for trainImg in train]
# deskX = deskew(train[0])

x = hogTransform.hog(train[0])
print x.shape
# print np.array(x).shape
# deskX = [map(deskew,trainImg) for trainImg in train]
# print np.array(deskX).shape
# hogX = [map(hog,x) for x in deskX]
# print np.array(hogX).shape

# hogX = [map(hog,x) for x in train]

# print hogX[0]


# deskew(x)
# plt.imshow(x[0,0])
# 
# hog(deskX)


# plt.figure()
# plt.imshow)
# plt.show()