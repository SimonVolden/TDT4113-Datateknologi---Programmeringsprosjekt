""" t-SNE """
import time
from categorical_scatter_2d import categorical_scatter_2d
import numpy as np
import cupy as cp
import matplotlib.pyplot as plt
import random
from datetime import datetime



class T_sne:
    """ t-SNE """
    def __init__(self, filename):
        self.data = np.genfromtxt(filename, delimiter = ',') # filename is "digits.csv"
        self.data = cp.asarray(self.data)
        self.n_data = self.data.shape[0]
        self.dimension_input = self.data.shape[1] # dimension_input is 64
        self.dimension_output = 2
        self.iterations = 200
        #self.answer = None # answer, used in transform
        self.knn = 25
        self.t_sne_algorithm()

    def comp_sim_mat(self):
        dist = cp.sqrt(self.compute_euclidean_distances_squared(self.data))
        idx = dist.argsort()
        neighbours = idx[:, :self.knn + 1 ]
        #print(neighbours)
        dist_knn = cp.zeros((self.n_data, self.n_data))
        for i in range(self.n_data):
            dist_knn[i, neighbours[i, :]] = 1
        return dist_knn

    def compute_euclidean_distances_squared(self, icput_matrix):
        x_matrix = icput_matrix #high_dim_icput_matrix
        x_matrix_squared = cp.square(x_matrix) # squared_high_dim_icput_matrix
        v_matrix = cp.sum(x_matrix_squared, axis=1, keepdims=True) # row_sum_matrix
        product_matrix = v_matrix -2 * ( x_matrix @ x_matrix.transpose() ) # W
        squared_distance_matrix  = v_matrix.transpose() + product_matrix
        squared_distance_matrix = cp.abs(squared_distance_matrix)
        return squared_distance_matrix
    

    def pairwise_euclidean_distances(self, X):
        V = cp.sum(X*X, axis = 1, keepdims = True)
        return cp.abs(V.T + V - 2*(X@X.T))
        

    def comp_P(self):
        p = self.comp_sim_mat()
        p_sum = cp.sum(p)
        P = p / p_sum
        return P  

    def t_sne_algorithm(self):
        t2 = time.time()
        epsilon = 500
        cp.random.seed(1)
        Y =  cp.random.normal(0., 0.0001, (self.n_data, 2))
        gain = cp.ones((self.n_data, 2))
        delta = cp.zeros((self.n_data, 2))
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
            Q = q/cp.sum(q)

            # treigt ~1 sec
            if n > 100:
                G = (P - Q) * q
            else:
                G = (4*P - Q) * q
            S = cp.diag(cp.sum(G, axis = 1))
            grad = 4 * (S - G) @ Y
            
            #Det går fort herfra
            gain[cp.sign(grad) == cp.sign(delta)] *= 0.8
            gain[cp.sign(grad) != cp.sign(delta)] += 0.2
            gain[gain < 0.01] = 0.01
            
            delta = (alpha * delta) - (epsilon * gain * grad)
            Y += delta

            t1 = time.time() - t0
            print(str(n) + ": " + str(t1))
        print("Finished in {:0.4f} seconds".format(time.time() - t2))

        if self.dimension_input == 64:
            digits = np.genfromtxt("digits_label.csv", delimiter = ',')
            categorical_scatter_2d(Y.get(), digits, alpha=1.0, ms=6,
                                    show=True, savename="runs/200_1000")

        else:
            colors_count = []
            for i in range(2000):
                colors_count.append(i)
            colors = np.array(colors_count)
            plt.scatter(Y[:,0].get(), Y[:,1].get(),c = colors, s=10, marker=".")

        

    """

    def comp_q(self):
        dist = self.compute_euclidean_distances_squared()
        idx = dist.argsort()
        neighbours = idx[:, :self.knn + 1 ]
        print(neighbours)
        dist_knn = cp.zeros((self.n_data, self.n_data))
        for i in range(self.n_data):
            dist_knn[i, neighbours[i, :]] =  1 / 1 + dist[i, neighbours[i, :]]
        return dist_knn


    
    def comp_Q(self):
        q = self.comp_q()
        q_sum = cp.sum(q)
        Q = q /q_sum
        return Q

    def comp_D(self):
        P = self.comp_P()
        Q = self.comp_Q()
        D = 0
        for i in range(self.n_data):
            for j in range(self.n_data):
                D += P[i,j] * cp.log(P[i,j]/Q[i,j])
        return D
        
    """     


def main():
    
    t_sne = T_sne("digits.csv")
    

if __name__ == "__main__":
    main()
