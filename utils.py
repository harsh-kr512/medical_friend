import numpy as np

def sparse_to_dense(X):
    return np.asarray(X.todense())