from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from pickle import load
import time
from categorical_scatter_2d import categorical_scatter_2d
import numpy as np

"""
Implementation of t-SNE based on Van Der Maaten and Hinton (2008)
http://www.jmlr.org/papers/volume9/vandermaaten08a/vandermaaten08a.pdf
Author: Liam Schoneveld
"""

from sklearn.datasets import load_digits

import numpy as np
from t_sne41 import estimate_sne, tsne_grad, q_tsne
from t_sne41 import p_joint


# Set global parameters
PERPLEXITY = 20
SEED = 1                    # Random seed
MOMENTUM = 0.80
LEARNING_RATE = 10.
NUM_ITERS = 1000           # Num iterations to train for
NUM_PLOTS = 5               # Num. times to plot in training


def main():
    # numpy RandomState for reproducibility
    rng = np.random.RandomState(SEED)

    # Load the first NUM_POINTS 0's, 1's and 8's from MNIST
    X = np.genfromtxt("digits copy.csv", delimiter = ',') # filename is "digits.csv"
    y = np.genfromtxt("digits_label copy.csv", delimiter = ',') # filename is "digits.csv"
    

    # Obtain matrix of joint probabilities p_ij
    P = p_joint(X, PERPLEXITY)
    t0 = time.time()
    # Fit SNE or t-SNE
    Y = estimate_sne(X, y, P, rng,
                     num_iters=NUM_ITERS,
                     q_fn=q_tsne,
                     grad_fn=tsne_grad,
                     learning_rate=LEARNING_RATE,
                     momentum=MOMENTUM,
                     plot=NUM_PLOTS)
    print(time.time() - t0)

if __name__ == "__main__":
    main()