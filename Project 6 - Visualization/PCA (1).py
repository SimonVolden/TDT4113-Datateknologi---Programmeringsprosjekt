import numpy as np
from numpy import mean
from numpy import cov
from numpy.linalg import eig
import scipy.sparse.linalg.eigen as eigs
import matplotlib.pyplot as plt
import matplotlib.cm as cm



class PCA:

    def __init__(self, D):
        self.swiss_array = np.genfromtxt('swiss_data.csv', delimiter=",")
        self.digits = np.genfromtxt('digits.csv', delimiter=",")
        self.D = D

    def fit_transform(self):
        self.swiss_array = self.swiss_array.T
        print(self.swiss_array.shape)

        mean_x = np.mean(self.swiss_array[0, :])
        mean_y = np.mean(self.swiss_array[1, :])
        mean_z = np.mean(self.swiss_array[2, :])
        mean_vector = np.array([[mean_x], [mean_y], [mean_z]])

        #print('Mean Vector:\n', mean_vector)

        scatter_matrix = np.zeros((3,3))
        for i in range(self.swiss_array.shape[1]):
            scatter_matrix += (self.swiss_array[:,i].reshape(3,1) - mean_vector).dot((self.swiss_array[:,i].reshape(3,1) - mean_vector).T)
        #print('Scatter Matrix:\n', scatter_matrix)

        cov_mat = np.cov([self.swiss_array[0,:], self.swiss_array[1,:], self.swiss_array[2,:]])
        #print('Covariance Matrix:\n', cov_mat)

        eig_val_sc, eig_vec_sc = np.linalg.eig(scatter_matrix)
            

        for i in range(len(eig_val_sc)):
            eigv = eig_vec_sc[:,i].reshape(1,3).T
            np.testing.assert_array_almost_equal(scatter_matrix.dot(eigv), eig_val_sc[i] * eigv,
                                         decimal=6, err_msg='', verbose=True)

        for ev in eig_vec_sc:
            np.testing.assert_array_almost_equal(1.0, np.linalg.norm(ev))

        # Make a list of (eigenvalue, eigenvector) tuples
        eig_pairs = [(np.abs(eig_val_sc[i]), eig_vec_sc[:,i]) for i in range(len(eig_val_sc))]

        # Sort the (eigenvalue, eigenvector) tuples from high to low
        eig_pairs.sort(key=lambda x: x[0], reverse=True)

        matrix_w = np.hstack((eig_pairs[0][1].reshape(3,1), eig_pairs[1][1].reshape(3,1)))
        #print('Matrix W:\n', matrix_w)
        
        transformed = matrix_w.T.dot(self.swiss_array)

        C = np.array([i for i in range(2000)])
        colors = cm.rainbow(np.linspace(0, 1, len(C)))

        plt.scatter(transformed[1,0:2000], transformed[0,0:2000], s=10, c=colors, marker=".")
        plt.xlim([-2,2])
        plt.ylim([-2,2])
        plt.xlabel('x_values')
        plt.ylabel('y_values')
        plt.title('PCA Result')

        plt.show()

    def fit_digits(self):
        c = self.digits.view()
        c.reshape(5620, 8, 8)
        d = self.digits.reshape(5620, 8, 8)
        print(d.shape)
        print(d[0])
        
        e = d[0:5].reshape(40, 8)
        
        f = d[5:10].reshape(40, 8)
        e = list(e)
        for i in range(len(e)):
            if i%9 == 0:
                e.insert(i, [0, 0, 0, 0, 0, 0, 0, 0])
        print(e)


        plt.imshow(e, cmap=plt.cm.binary)
        plt.show()        

        #self.digits.reshape((5620, 8))
        



def main():
    pca = PCA(3)
    pca.fit_transform()
    #pca.fit_digits()
    
if __name__ == "__main__":
    main()
