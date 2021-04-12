""" isomap """
import numpy as np
from scipy.sparse.linalg import eigs
import matplotlib.pyplot as plt
#from sklearn.utils.graph_shortest_path import graph_shortest_path as djikstra
from sklearn.utils.graph import graph_shortest_path
import time


class Isomap:
    """ isomap """
    def __init__(self, filename, knn = 10):
        self.data = np.genfromtxt(filename, delimiter = ',') # filename is "digits.csv"
        self.dimension_input = self.data.shape[1] # dimension_input is 64
        self.dimension_output = 2
        #self.answer = None # answer, used in transform
        self.n_data = self.data.shape[0]
        self.knn = knn

    def compute_euclidean_distances(self):
        """ helper to compute_geodesics """
        start = time.time()
        x_matrix = self.data
        x_matrix_squared = np.square(x_matrix)
        v_matrix = np.sum(x_matrix_squared, axis=1, keepdims=True)
        product_matrix = v_matrix -2 * ( x_matrix @ x_matrix.transpose() )
        squared_distance_matrix  = v_matrix.transpose() + product_matrix
        squared_distance_matrix = np.abs(squared_distance_matrix)
        distance_matrix = np.sqrt(squared_distance_matrix)
        end = time.time()
        print("Compute euclidian distances: " + "{:.4f}".format(end - start))
        return distance_matrix

    def compute_geodesics(self):
        """ part 1 """
        start = time.time()
        dist_knn = self.keep_k_nearest()
        d_geodesic = graph_shortest_path(dist_knn)
        end = time.time()
        print("Compute geodesics: " + "{:.4f}".format(end - start))
        return d_geodesic

    def keep_k_nearest(self):
        """ keeps the k nearest, sets the rest to 0"""
        start = time.time()
        dist = self.compute_euclidean_distances()
        idx = dist.argsort()
        neighbours = idx[:, :self.knn + 1 ]
        dist_knn = np.zeros((self.n_data, self.n_data))
        for i in range(self.n_data):
            dist_knn[i, neighbours[i, :]] = dist[i, neighbours[i, :]]
        end = time.time()
        print("Compute keep k nearest: " + "{:.4f}".format(end - start))
        return dist_knn


    def multidimensional_scaling(self):
        """ MDS classic """
        start = time.time()
        d_geodesic = self.compute_geodesics() # D
        d_geodesic_square = np.square(d_geodesic) # D^2
        centering_matrix = np.eye(self.n_data) - np.ones(d_geodesic.shape) / self.n_data
        double_centering = (-1/2) * (centering_matrix @ d_geodesic_square @ centering_matrix) # B = (-1/2)* J @ D^2 @ J
        [eigenvalues, eigenvectors] = eigs(double_centering, k=self.dimension_output)
        coord = eigenvectors @ np.diag(np.sqrt(eigenvalues))
        end = time.time()
        print("Compute multidimensional scaling: " + "{:.4f}".format(end - start))
        return np.real(coord)

    def scatter(self):
        """dig plotter"""
        answer = self.multidimensional_scaling()
        if self.dimension_input == 64:
            colors = np.genfromtxt("digits_label.csv", delimiter = ',')
            plt.scatter(answer[:,0], answer[:,1],c = colors, s=10, marker=".")
            plt.xlim([-130,130])
            plt.ylim([-100,100])
            plt.title('Isomap digits Result')
        else:
            colors_count = []
            for i in range(2000):
                colors_count.append(i)
            colors = np.array(colors_count)
            plt.scatter(answer[:,0], answer[:,1],c = colors, s=10, marker=".")
            plt.xlim([-7,10])
            plt.ylim([-1,1])
            plt.title('Isomap swiss Result')
        plt.xlabel('x_values')
        plt.ylabel('y_values')
        plt.show()


def main():
    """ main """
    iso = Isomap("digits.csv", 30) #5620,64
    iso.scatter()
    iso2 = Isomap("swiss_data.csv", 30) #2000,3
    iso2.scatter()

    #print(iso.compute_euclidean_distances().shape)
    #print(iso.compute_geodesics())
    #points = iso.multidimensional_scaling()
    
    #print('\n points \n')
    #print(points)
    #print(points.shape)
    #colors_count = []
    #for i in range(2000):
    #    colors_count.append(i)
    #colors = np.array(colors_count)
    #colors = np.genfromtxt("digits_label.csv", delimiter = ',')
    #plt.scatter(points[:,0], points[:,1],c = colors, s=10, marker=".")
    #plt.xlim([-10,6])
    #plt.ylim([-1,1])
    #plt.xlabel('x_values')
    #plt.ylabel('y_values')
    #plt.title('Isomap Result')
    #plt.show()



if __name__ == "__main__":
    main()
