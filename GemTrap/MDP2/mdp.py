
import numpy as np
import pysparse
from markovChain import MarkovChain


class Action(MarkovChain):
    def __init__(self):
        super(Action, self).__init__()
        self.mpd = None
        self.mapping = None

    def __repr__(self):
        return self.name

    def costs(self, state):
        """
        To be provided by the subclass.  Return a cost when action a
        is chosen when in the state .
        """
        raise NotImplementedError

    def generateCosts(self):
        self.c = np.zeros(self.size)
        map = self.mapping
        for state in self.space:
            i = map[state]
            self.c[i] = self.costs(state)


class MDP(object):
    def __init__(self , actions, initstate):
        self.actions = actions
        self.initstate = initstate
        self.mapping = {}

        for a in self.actions:
            a.mdp = self
            a.mapping = self.mapping
        self.gamma = 1.    #discount factor

    @property
    def size(self):
        return len(self.mapping)

    @property
    def space(self):
        return  self.mapping.keys()

    def generateAll(self):
        self.generateStateSpace()
        self.generateTransitionMatrices()
        self.generateCosts()

    def generateStateSpace(self):
        map = self.mapping
        map[self.initstate] = 0
        frontier = set( [self.initstate] )
        while len(frontier) > 0:
            fromstate = frontier.pop()
            fromindex = map[fromstate]
            for a in self.actions:
                for tostate, rate in a.transitionStates(fromstate).items():
                    if tostate not in map:
                        frontier.add(tostate)
                        map[tostate] = len(map)
                    toindex = map[tostate]
                    a.rates[(fromindex, toindex)] = rate

    def generateCosts(self):
        for a in self.actions:
            a.generateCosts()

    def generateTransitionMatrices(self):
        for a in self.actions:
            a.generateTransitionMatrix()

    def save(self):
        for a in self.actions:
            print a.P.getnnz()
            print len(self.space)
            for s in sorted(a.P.items()):
                i, j = s[0]
                print a, self.mapping[i], self.mapping[j], s[1]

    def bellman(self, V):
        C = np.zeros((len(V),len(self.actions)))
        for i, a in enumerate(self.actions):
            res = np.zeros(len(V))
            a.P.matvec(V,res)  # P*V
            C[:,i] = a.c + self.gamma*res 
        x = np.amin(C, axis=1)
        optPol = np.argmin(C,axis=1)
        return x,optPol

    def valueIteration(self, eps = 1e-10):    
        diff = 1.
        V = np.zeros(self.size)
        mn = 0.
        numIter = 0
        while diff > eps*mn:
            Vnew, optPol = self.bellman(V)
            mn = np.amin(Vnew - V); Mn = np.amax(Vnew - V);
            diff = Mn - mn
            V = Vnew
            numIter += 1
        print numIter
        self.V = V
        self.optPol = optPol
        self.Mn, self.mn = Mn, mn

    def modifiedValueIteration(self, eps = 1e-10):    
        diff = 1.
        V = np.zeros(len(self.space))
        mn = 0.
        numIter = 0
        while diff > eps*mn:
            Vnew, optPol = self.bellman(V)
            mn = np.amin(Vnew - V); Mn = np.amax(Vnew - V);
            omega = self.relaxationFactor(V, Vnew, optPol)
            diff = Mn - mn
            V += omega*(Vnew-V)
            numIter += 1
            if numIter % 100 == 0:
                print numIter, mn, Mn
        print numIter
        self.V = V
        self.optPol = optPol
        self.g = (mn+Mn)/2.
        self.Mn, self.mn = Mn, mn

    def relaxationFactor(self, V, Vnew, pol):
        u = int(np.argmin(Vnew- V))
        v = int(np.argmax(Vnew - V))
        Ru = self.actions[pol[u]]
        Rv = self.actions[pol[v]]
        w1 = np.zeros(1)
        Ru.P[u,:].matvec(Vnew - V, w1) 
        w2 = np.zeros(1)
        Rv.P[v,:].matvec(Vnew - V, w2) 
        mn = np.amin(Vnew - V); Mn = np.amax(Vnew - V)
        omega = (Mn- mn)/(Mn-mn + w1-w2)
        return omega


    def improvePolicy(self, policy):
        size = len(policy)
        A = pysparse.spmatrix.ll_mat(size+1,size+1)
        rewards = np.zeros(size+1)
        # build  P - 1
        for i in xrange(size):
            a  = self.actions[policy[i]]
            rewards[i] = a.c[i]
            A[i,:-1] = a.P[i,:]
            A[i,i] -= 1.
            A[i,size] = -1.
        A.scale(-1)
        A[size,0] = 1
        x = np.empty(size+1)
        LU = pysparse.umfpack.factorize(A, strategy="UMFPACK_STRATEGY_UNSYMMETRIC")
        LU.solve(rewards, x)
        V, betterpol = self.bellman(x[:-1])
        g = x[-1] # average cost
        return V, betterpol, g
        """
        # Other  solvers, just in case umfpack does not work.
        from pysparse import itsolvers
        #info, iter, relres = itsolvers.pcg(A, rewards, x, 1e-8, 2000)
        #info, iter, relres = itsolvers.qmrs(A.to_sss(), rewards, x, 1e-8, 2000)
        print info
        if info == 0:
            print x[size]
        """
        """
        from pysparse import superlu
        LU = superlu.factorize(A.to_csr(), diag_pivot_thresh=0.0)
        LU.solve(rewards, x)
        values, optPol = bellman(actions, x[:-1], MIN = False,gamma = 1)
        print x[-1]
        """

    def policyIteration(self):
        # Just get an initial policy
        V, oldPol = self.bellman(np.zeros(self.size))
        values, newPol, g = self.improvePolicy(oldPol)
        it =0
        while not np.equal(oldPol,newPol).all():
            oldPol = newPol
            V, newPol,g = self.improvePolicy(oldPol)
            it +=1
            print "policy Iteration, number of iterations: ", it
        self.g = g
        self.V = V
        self.optPol = newPol

    def printOptimalPolicy(self):
        for s in self.space:
            print s, self.actions[self.optPol[self.mapping[s]]]

