import time
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import pairwise_distances

"""def pairwise_euclidean_distances(self, X):
        V = np.sum(X*X, axis = 1, keepdims = True)
        return np.abs(V.T + V - 2*(X@X.T))"""



data = np.genfromtxt("digits.csv", delimiter = ',')
print(data.shape)

np.random.seed(42)

rndperm = np.random.permutation(data.shape[0])

time_start = time.time()
tsne = TSNE(n_iter=300)
tsne_results = tsne.fit_transform(data)
print(tsne_results.shape)
print('t-SNE done! Time elapsed: {} seconds'.format(time.time()-time_start))


"""colors_count = []
for i in range(5620):
    colors_count.append(i)
colors = np.array(colors_count)"""
plt.scatter(tsne_results[:,0], tsne_results[:,1], s=10, marker=".")
plt.show()