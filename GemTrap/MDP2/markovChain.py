
import itertools as it

import numpy as np
from scipy.linalg import norm
import pysparse

class MarkovChain(object):
    def __init__(self):
        self.P = None # transition matrix
        self.pi = None # steady state probability vector
        self.mapping = {}
        self.rates = {}

    @property
    def size(self):
        # return the number of states in the state space
        return len(self.mapping)

    @property
    def space(self):
        # return all states in the state space
        return  self.mapping.keys()

    def transitionStates(self, state):
        """
        To be provided by the subclass.  Return a dict of reachable
        states with probabilities or rates.
        """
        raise NotImplementedError

    def generateStateSpace(self, initState):
        map = self.mapping
        map[initState] = 0
        frontier = set( [initState] )
        while len(frontier) > 0:
            fromstate = frontier.pop()
            fromindex = map[fromstate]
            for tostate, rate in self.transitionStates(fromstate).items():
                if tostate not in map:
                    frontier.add(tostate)
                    map[tostate] = len(map)
                toindex = map[tostate]
                self.rates[(fromindex, toindex)] = rate

    def convertRateMatrixToTransitionMatrix(self, P):
        Q = P
        # fill diagonal of the rate matrix
        x =  np.empty(self.size)
        Q.matvec(np.ones(self.size),x)
        Q.put(-x)
        # uniformize
        l = np.amin(Q.values())*1.001
        P = pysparse.spmatrix.ll_mat(self.size,self.size)
        P.put(np.ones(self.size))
        P.shift(-1./l, Q)
        return P

    def generateTransitionMatrix(self, rates= False):
        # if rates = True the transitions are given as rates rather
        # than as probabilities
        P = pysparse.spmatrix.ll_mat(self.size,self.size)
        while self.rates:
            key, value = self.rates.popitem()
            P[key] = value
        if rates:  #  Convert the rate matrix to a transition matrix
            P = self.convertRateMatrixToTransitionMatrix(P)
        self.P = P

    def powerMethod(self, tol = 1e-8, numIter = 1e5):
        # use the power method
        P = self.P.to_csr()
        pi = np.zeros(self.size);  pi1 = np.zeros(self.size)
        pi[0] = 1;
        n = norm(pi - pi1,1); i = 0;
        while n > tol and i < numIter:
            P.matvec_transp(pi,pi1)
            P.matvec_transp(pi1,pi)
            n = norm(pi - pi1,1); i += 1
        self.pi = pi

    def inverseMethod(self):
        # use another trick
        size = self.size
        A = pysparse.spmatrix.ll_mat(size+1,size+1)
        rewards = np.zeros(size+1)
        # build  P - 1
        for i in xrange(size):
            A[i,:-1] = self.P[i,:]
            A[i,i] -= 1.
            A[i,size] = -1.
        A.scale(-1)
        A[size,0] = 1
        x = np.empty(size+1)
        rewards[-1] = 1
        LU = pysparse.umfpack.factorize(A, strategy="UMFPACK_STRATEGY_UNSYMMETRIC")
        LU.solve(rewards, x)
        
    def printPi(self):
        for s in sorted(self.space):
            print s, self.pi[self.mapping[s]]