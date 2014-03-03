
from collections import namedtuple

import numpy as np
from scipy.stats import poisson

import mdp as m


State = namedtuple('State', "c") 


class No(m.Action): #no repair
    def __init__(self):
        super(No, self).__init__()
        self.name = "No"
    
    def transitionStates(self, state):
        t = {}
        if state.c == 1:
            t[State(c=1)] = 0.9
            t[State(c=2)] = 0.1
        elif state.c == 2:
            t[State(c=2)] = 0.8
            t[State(c=3)] = 0.1
            t[State(c=4)] = 0.05
            t[State(c=5)] = 0.05
        elif state.c == 3:
            t[State(c=3)] = 0.7
            t[State(c=4)] = 0.1
            t[State(c=5)] = 0.2
        elif state.c == 4:
            t[State(c=4)] = 0.5
            t[State(c=5)] = 0.5
        else:
            return {state: 1.}
        return t

    def costs(self, state):
        if 5<= state.c <= 6:
            return np.inf
        else:
            return 0.


class Pr(m.Action): #preventive
    def __init__(self):
        super(Pr, self).__init__()
        self.name = "Pr"
    
    def transitionStates(self, state):
        if 1< state.c < 5: 
            return  {State(c=1): 1.}
        else:
            return  {state: 1.}

    def costs(self, state):
        if state.c == 2:
            return 7.
        if state.c == 3:
            return 7.
        if state.c == 4:
            return 5.
        else:
            return np.inf


class Re(m.Action): #repair
    def __init__(self):
        super(Re, self).__init__()
        self.name = "Re"
    
    def transitionStates(self, state):
        if state.c == 5:
            return  {State(c=6): 1.}
        if state.c == 6:
            return  {State(c=1): 1.}
        else:
            return {state: 1.}

    def costs(self, state):
        if state.c == 5:
            return 10.
        if state.c == 6:
            return 0.
        else:
            return np.inf


class MDP(m.MDP):
    def __init__(self, actions, initspace):
        super(MDP, self).__init__(actions, initspace)


actions = (No(), Pr(), Re())

mdp = MDP(actions, State(c=1) )
mdp.generateAll()


mdp.valueIteration(eps = 1.e-4)
mdp.printOptimalPolicy()
print mdp.mn, mdp.Mn


mdp.policyIteration()
mdp.printOptimalPolicy()
print mdp.g
