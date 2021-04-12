""" pca """
import numpy as np
#import scipy
from scipy.sparse.linalg import eigs
import matplotlib.pyplot as plt
#import matplotlib.cm as cm

class Pca:
    """ pca """
    def __init__(self, filename, dimension_input):
        self.file = np.genfromtxt(filename, delimiter = ',') # filename is "digits.csv"
        self.data = self.file - self.file.mean(axis = 0)  # center
        self.dimension_input = dimension_input # dimension_input is 64
        self.dimension_output = 2
        self.answer = None # answer, used in transform

    def fit(self):
        """ fit """
        sigma = np.cov(self.data.T)
        #print(sigma)
        if self.dimension_input - 1 > self.dimension_output:
            [_eigenvalues, eigenvectors] = eigs(sigma, k=self.dimension_output)

        elif self.dimension_input -1 == self.dimension_output:
            [eigenvalues, eigenvectors] = np.linalg.eigh(sigma)
            idx = eigenvalues.argsort()#[::1]
            eigenvalues = eigenvalues[idx]
            eigenvectors = eigenvectors[:, idx[-self.dimension_output:]]
            #eigenvectors = eigenvectors[0:self.dimension_output]
            #print(eigenvectors)
        return np.real(eigenvectors)

    def transform(self):
        """ transform """
        center = self.file - self.file.mean()
        eigenvectors = self.fit()
        #trans = eigenvectors
        self.answer = np.matmul(center, eigenvectors)

    def scatter(self):
        """dig plotter"""
        if self.dimension_input == 64:
            colors = np.genfromtxt("digits_label.csv", delimiter = ',')
            plt.scatter(self.answer[:,0], self.answer[:,1],c = colors, s=10, marker=".")
            plt.xlim([-30,30])
            plt.ylim([-30,30])
        else:
            colors_count = []
            for i in range(2000):
                colors_count.append(i)
            colors = np.array(colors_count)
            plt.scatter(self.answer[:,0], self.answer[:,1],c = colors, s=10, marker=".")
            plt.xlim([-2,2])
            plt.ylim([-2,2])
        plt.xlabel('x_values')
        plt.ylabel('y_values')
        plt.title('PCA Result')
        plt.show()


def main():
    pca = Pca("digits.csv", 64)
    pca.transform()
    pca.scatter()


    pca2 = Pca("swiss_data.csv", 3)
    pca2.transform()
    pca2.scatter()


if __name__ == "__main__":
    main()
