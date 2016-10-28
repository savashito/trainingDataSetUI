import sys
sys.path.append('E:/Savage/craterRepo/craters/bayesCraterModeling')
from MLProject import MLProject


mlProject = MLProject("Craters")
c = mlProject.getCraters()

primary = [0,1,2,3,4,5]
secondary = [6,7,8,9,10,11]
# print c
color = ['r']*6+['b']*6+['g']*10
dtm_color = ['r','b','r','b','r','b'] + ['r']*3+['b']*3
from time import time

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import offsetbox
from sklearn import (manifold)



#----------------------------------------------------------------------
# Scale and visualize the embedding vectors
def plot_embedding(X, title=None):
    x_min, x_max = np.min(X, 0), np.max(X, 0)
    X = (X - x_min) / (x_max - x_min)

    plt.figure()
    
    ax = plt.subplot(111)
    lp,ls =None,None
    for i in range(X.shape[0]):
    	print i
        if(i==0):
         	lp = plt.plot(X[i,0],X[i,1],'o',color = color[i],label="Primary crater")
         	print lp
        elif(i==6):
         	ls = plt.plot(X[i,0],X[i,1],'o',color = color[i],label="Secondary crater")
         	print ls
        elif(i==12):
         	ls = plt.plot(X[i,0],X[i,1],'o',color = color[i],label="Unknow crater")
         	print ls
        else:
         	plt.plot(X[i,0],X[i,1],'o',color = color[i])

        # plt.text(X[i, 0], X[i, 1], str(i),color = color[i],
        #          fontdict={'weight': 'bold', 'size': 9})
        # plt.text(X[i, 0], X[i, 1], str(digits.target[i]),
        #          color=plt.cm.Set1(y[i] / 10.),
        #          fontdict={'weight': 'bold', 'size': 9})
	plt.legend()
	# plt.legend(handles=[lp, ls])
    # if hasattr(offsetbox, 'AnnotationBbox'):
    #     # only print thumbnails with matplotlib > 1.0
    #     shown_images = np.array([[1., 1.]])  # just something big
    #     for i in range(digits.data.shape[0]):
    #         dist = np.sum((X[i] - shown_images) ** 2, 1)
    #         if np.min(dist) < 4e-3:
    #             # don't show points that are too close
    #             continue
    #         shown_images = np.r_[shown_images, [X[i]]]
    #         imagebox = offsetbox.AnnotationBbox(
    #             offsetbox.OffsetImage(digits.images[i], cmap=plt.cm.gray_r),
    #             X[i])
    #         ax.add_artist(imagebox)
    plt.xticks([]), plt.yticks([])
    if title is not None:
        plt.title(title)


#----------------------------------------------------------------------
# t-SNE embedding of the digits dataset
print("Computing t-SNE embedding")
tsne = manifold.TSNE(n_components=2, init='pca', random_state=0)
t0 = time()
X_tsne = tsne.fit_transform(c)

# plt.plot(X_tsne.T,'o')
# print X_tsne[0]
plot_embedding(X_tsne,
               "t-SNE embedding of crater parameters (time %.2fs)" %
               (time() - t0))

plt.show()

