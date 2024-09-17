import numpy as np
import scipy as sp


Nx = 10   # number of x coefficients in basis  [GLOBAL VARIABLE]
Ny = 10   # number of y coefficients in basis  [GLOBAL VARIABLE]

##############################
def aStruc(n):
    return 1/(2.*(n+1)*(1+(n>0)))

##############################
def bStruc(n):
    return -0.25*(n>=2)/(n-1.)

##############################


def inv(n,m):
	if m>n:
		return 0
	elif (m+n)%2==0:
		ss = 1
		for a in range(m+2,n+1,2):
			ss = - ss * bStruc(a)/aStruc(a)
		return (1/aStruc(m))*ss
	else:
		return 0



def ders(A):
    nx = len(A)
    ny = len(A[0])
    ###############
    Lambda = np.zeros([nx, ny])   # the x derivative
    Eta    = np.zeros([nx, ny])   # the y derivative
    gamma  = np.zeros([nx, ny])   # the xy derivative
    beta   = np.zeros([nx, ny])   # the yy derivative
    alpha  = np.zeros([nx, ny])   # the xx derivative
    ## Lambda computation
    for j in range(ny):
        for i in range(nx):
            for l in range(1,nx):
                Lambda[i][j] = Lambda[i][j] + A[l][j]*inv(l-1,i)
    ## Eta computation
    for i in range(nx):
        for j in range(ny):
            for l in range(1,nx):
                Eta[i][j] = Eta[i][j] + A[i][l]*inv(l-1,j)
    ## gamma computation
    for i in range(nx):
        for j in range(ny):
            for l in range(1,nx):
                for m in range(1,ny):
                    gamma[i][j] = gamma[i][j] + A[m][l]*inv(l-1,j)*inv(m-1,i)
    ## alpha computation
    for i in range(nx):
        for j in range(ny):
            for l in range(2,nx):
                for m in range(1,nx+1):
                    alpha[i][j] = alpha[i][j] + A[l][j]*inv(l-1,m)*inv(m-1,i)
    ## beta computation
    for i in range(nx):
        for j in range(ny):
            for l in range(2,nx):
                for m in range(1,nx+1):
                    beta[i][j] = beta[i][j] + A[i][l]*inv(l-1,m)*inv(m-1,j)
    return [A, Lambda, Eta, alpha, gamma, beta]