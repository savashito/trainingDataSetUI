
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize
from debugUtil import debug
class MidpointNormalize(Normalize):

    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))




# remove dimensions to make it 2D
# and 2 clases only
# X_2d = X[:, :2]
# # remove class 0
# X_2d = X_2d[y > 0]
# y_2d = y[y > 0]
# # shift all the classes down
# y_2d -= 1

def findBestParametersSV(X,y,disp=True):
	# scale the data

	# if(scaleData):
	# 	scaler = StandardScaler()
	# 	X = scaler.fit_transform(X)

	# X_2d = scaler.fit_transform(X_2d)

	# search over the entire space
	C_range = np.logspace(-2,10,13)
	gamma_range = np.logspace(-9,3,13)
	param_grid = dict(gamma=gamma_range,C=C_range)
	# Croos validate
	cv = StratifiedShuffleSplit(y, n_iter=5, test_size=0.2, random_state=42)
	debug("Initiating grid search")
	grid = GridSearchCV(SVC(), param_grid=param_grid, cv=cv)
	grid.fit(X,y)
	print("The best parameters are %s with a score of %0.2f"
	      % (grid.best_params_, grid.best_score_))
	gamma, C = grid.best_params_['gamma'],grid.best_params_['C']
	scores = [x[1] for x in grid.grid_scores_]
	scores = np.array(scores).reshape(len(C_range), len(gamma_range))

	if(disp):
		plt.figure(figsize=(8, 6))
		plt.subplots_adjust(left=.2, right=0.95, bottom=0.15, top=0.95)
		plt.imshow(scores, interpolation='nearest', cmap=plt.cm.hot,
		           norm=MidpointNormalize(vmin=0.2, midpoint=0.92))
		plt.xlabel('gamma')
		plt.ylabel('C')
		plt.colorbar()
		plt.xticks(np.arange(len(gamma_range)), gamma_range, rotation=45)
		plt.yticks(np.arange(len(C_range)), C_range)
		plt.title('Validation accuracy')
		plt.show()
	return gamma,C