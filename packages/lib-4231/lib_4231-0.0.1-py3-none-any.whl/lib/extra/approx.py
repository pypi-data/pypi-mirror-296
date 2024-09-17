import numpy as np
import scipy as sp
import numpy.polynomial.chebyshev as Che

def tau(n,x):
    return sp.special.eval_chebyt(n, 2*x-1., out=None) 

##########  This function takes as entry any matrix of weights and yields the approximation
def approx(C,x,y):
    ss = 0
    N1 = len(C)
    N2 = len(C[0])
    for i in range(N1):
        for j in range(N2):
            ss = ss + C[i][j]*tau(i,x)*tau(j,y)
    return ss