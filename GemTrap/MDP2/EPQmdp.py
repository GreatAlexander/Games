
from __future__ import division

from collections import namedtuple
import numpy as np

import mdp as m


left= -4
right = 5
n = 100

start = n*left
end = n*right
deltaX = 1./n

q = 1.
r = 1.8
deltaT = deltaX/(r+q)
alpha = q/(r+q)
beta = 1. - alpha

K = 30.


def h(n):
    x = n*deltaX
    return  deltaT*(-2.*np.minimum(0,x) + np.maximum(0,x))


State = namedtuple('State', "P I")

class On(m.Action):
    def __init__(self):
        super(On, self).__init__()
        self.name = "On"
    
    def reachableStates(self, state):
        if state.I < end:
            return set([State(P=1, I=state.I+1)])
        else:
            return set([State(P=0, I=state.I)])

    def transitionStates(self, state):
        if start < state.I < end:
            t = {State(P=1, I=state.I-1): alpha, 
                 State(P=1, I=state.I+1): beta
                 }
        elif state.I == end:
            t = {State(P=1, I=state.I-1): alpha, 
                 State(P=1, I=state.I): beta
                 }
        elif state.I == start:
            t = {State(P=1, I=state.I): alpha, 
                 State(P=1, I=state.I+1): beta
                 }
        return  t

    def costs(self, state):
        cost = alpha*h(state.I-1)+ beta*h(state.I + 1)
        if state.P == 0:
            cost  += K
        return cost


class Off(m.Action):
    def __init__(self):
        super(Off, self).__init__()
        self.name = "Off"

    def reachableStates(self, state):
        if state.I > start:
            return set([State(P=0, I=state.I-1)])
        else:
            return set([State(P=1, I=state.I)])

    def transitionStates(self, state):
        if start < state.I < end:
            t = {State(P=0, I=state.I-1): alpha, 
                 State(P=0, I=state.I): beta
                 }
        elif state.I == end:
            t = {State(P=0, I=state.I-1): alpha, 
                 State(P=0, I=state.I): beta
                 }
        elif state.I == start:
            t = {State(P=0, I=state.I): 1.}
        return  t

    def costs(self, state):
        return alpha*h(state.I-1)+ beta*h(state.I)


class MDP(m.MDP):
    def __init__(self, actions, initspace):
        super(MDP, self).__init__(actions, initspace)

    def printPolicyChanges(self):
        print "Policy changes on the off-line"
        prev = State(P=0, I = start)
        for s in sorted(self.space):
            if s.P == 0:
                prevaction = self.optPol[self.mapping[prev]]
                action = self.optPol[self.mapping[s]]
                if action != prevaction:
                    print "At level: %4.3f"%(1.*s.I/n),
                    print " choose: ", self.actions[action]
                prev = s
        
        print "Policy changes on the on-line"
        prev = State(P=1, I = start)
        for s in sorted(self.space):
            if s.P == 1:
                prevaction = self.optPol[self.mapping[prev]]
                action = self.optPol[self.mapping[s]]
                if action != prevaction:
                    print "At level: %4.3f"%(1.*s.I/n),
                    print " choose: ", self.actions[action]
                prev = s
            

actions = (Off(), On())

mdp = MDP(actions, State(P=1, I=0) )
mdp.generateAll()
mdp.policyIteration()


#mdp.printOptimalPolicy()
mdp.printPolicyChanges()
print "Average cost per unit time g = ", mdp.g/deltaT


class EPQ(object):
    def __init__(self, r, q, b, h, K):
        self.r = r
        self.q = q
        self.b = b
        self.h = h
        self.K = K

    def EPQ(self):
        g = np.sqrt(self.q*(self.r-self.q)/self.r)
        g *= np.sqrt(2.*self.b*self.h/(self.b+self.h)*self.K)
        self.g =g 
        self.S = g/self.h
        self.s = -g/self.b

epq = EPQ(r=r, q=q, K=K, b =2., h =1.)
epq.EPQ()
print epq.s, epq.S, epq.g
