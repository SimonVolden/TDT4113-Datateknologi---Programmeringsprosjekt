""" t-SNE """
import time
from categorical_scatter_2d import categorical_scatter_2d
import numpy as np
import matplotlib.pyplot as plt
import random
from datetime import datetime



class T_sne:
    """ t-SNE """
    def __init__(self, filename):
        self.data = np.genfromtxt(filename, delimiter = ',') # filename is "digits.csv"
        self.n_data = self.data.shape[0]
        self.dimension_icput = self.data.shape[1] # dimension_icput is 64
        self.dimension_output = 2
        self.iterations = 200
        #self.answer = None # answer, used in transform
        self.knn = 25
        self.t_sne_algorithm()

    def comp_sim_mat(self):
        dist = np.sqrt(self.compute_euclidean_distances_squared(self.data))
        idx = dist.argsort()
        neighbours = idx[:, :self.knn + 1 ]
        #print(neighbours)
        dist_knn = np.zeros((self.n_data, self.n_data))
        for i in range(self.n_data):
            dist_knn[i, neighbours[i, :]] = 1
        return dist_knn

    def compute_euclidean_distances_squared(self, icput_matrix):
        x_matrix = icput_matrix #high_dim_icput_matrix
        x_matrix_squared = np.square(x_matrix) # squared_high_dim_icput_matrix
        v_matrix = np.sum(x_matrix_squared, axis=1, keepdims=True) # row_sum_matrix
        product_matrix = v_matrix -2 * ( x_matrix @ x_matrix.transpose() ) # W
        squared_distance_matrix  = v_matrix.transpose() + product_matrix
        squared_distance_matrix = np.abs(squared_distance_matrix)
        return squared_distance_matrix

    def pairwise_euclidean_distances(self, X):
        V = np.sum(X*X, axis = 1, keepdims = True)
        return np.abs(V.T + V - 2*(X@X.T))
        

    def comp_P(self):
        p = self.comp_sim_mat()
        p_sum = np.sum(p)
        P = p / p_sum
        return P  

    def t_sne_algorithm(self):
        t2 = time.time()
        epsilon = 1000
        np.random.seed(1)
        Y =  np.random.normal(0., 0.0001, (self.n_data, 2))
        gain = np.ones((self.n_data, 2))
        delta = np.zeros((self.n_data, 2))
        P = self.comp_P()
        for n in range(self.iterations):
            t0 = time.time()
            #print(n)
            if n < 250:
                alpha = 0.5
            else:
                alpha = 0.8

            #treigt ~1 sec
            q = 1 / (1 + self.pairwise_euclidean_distances(Y) )

            #fort
            q[range(self.n_data).stop-1, range(self.n_data).stop-1] = 0
            
            #0.2 sec max
            Q = q/np.sum(q)

            # treigt ~1 sec
            if n > 100:
                G = (P - Q) * q
            else:
                G = (4*P - Q) * q
            S = np.diag(np.sum(G, axis = 1))
            grad = 4 * (S - G) @ Y
            
            #Det går fort herfra
            gain[np.sign(grad) == np.sign(delta)] *= 0.8
            gain[np.sign(grad) != np.sign(delta)] += 0.2
            gain[gain < 0.01] = 0.01
            
            delta = (alpha * delta) - (epsilon * gain * grad)
            Y += delta

            t1 = time.time() - t0
            print(str(n) + ": " + str(t1))
        print("Finished in {:0.4f} seconds".format(time.time() - t2))

        if self.dimension_icput == 64:
            digits = np.genfromtxt("digits_label.csv", delimiter = ',')
            categorical_scatter_2d(Y, digits, alpha=1.0, ms=6,
                                    show=True, savename="runs/200_1000")
        else:
            colors_count = []
            for i in range(2000):
                colors_count.append(i)
            colors = np.array(colors_count)
            plt.scatter(Y[:,0], Y[:,1],c = colors, s=10, marker=".")

        
  


def main():
    t_sne = T_sne("digits.csv")
    

if __name__ == "__main__":
    main()
