# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state) # states
              mdp.getTransitionStatesAndProbs(state, action) # transition model
              mdp.getReward(state, action, nextState) # utility
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        # print "discount: ", discount
        # print "iterations: ", iterations
        # print "values: ", self.values
        #
        # print "states: ", mdp.getStates()
        # for state in mdp.getStates():
        #     print "state: ", state
        #     print "possible actions: ", mdp.getPossibleActions(state)
        #
        #     for action in mdp.getPossibleActions(state):
        #         print "action: ", action
        #
        #         for transState, prob in mdp.getTransitionStatesAndProbs(state, action):
        #             print "nextState: ", transState
        #             print "probability: ", prob
        #             print "reward: ", mdp.getReward(state, action, transState)
        #
        #         print "\n"

        # print mdp.getTransitionStatesAndProbs(state, action)
        # print mdp.getReward(state, action, nextState)
        # print mdp.isTerminal(state)

        """
        Algorithm developed with help from pseudocode at:
            http://artint.info/html/ArtInt_227.html
            and
            https://github.com/aimacode/aima-pseudocode/blob/master/md/
                Value-Iteration.md
            and
            http://stackoverflow.com/questions/8337417/markov-decision-process-
                value-iteration-how-does-it-work
        """
        i = 0
        while(i < iterations):
            # 'vector'/dict of utilities for states
            U = self.values.copy();
            for state in mdp.getStates():
                actionCost = util.Counter()
                if mdp.isTerminal(state) == False:
                    for action in mdp.getPossibleActions(state):
                        utilities = util.Counter()
                        j = 0;
                        for (nextState, probability) in mdp.getTransitionStatesAndProbs(state, action):

                            reward = mdp.getReward(state, action, nextState)
                            utilities[j] = probability * (reward + (discount * U[nextState]))
                            j += 1

                        actionCost[action] = utilities.totalCount()
                    self.values[state] = actionCost[actionCost.argMax()]
            i += 1


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        mdp = self.mdp
        value = 0
        if mdp.isTerminal(state) == False:
            for (nextState, probability) in mdp.getTransitionStatesAndProbs(state, action):
                reward = mdp.getReward(state, action, nextState)
                value += probability * (reward + (self.discount * self.values[nextState]))
        return value

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        mdp = self.mdp
        if mdp.isTerminal(state) == False:
            scores = list() # add all score-action tuples to a list

            for action in mdp.getPossibleActions(state):
                score = self.getQValue(state, action)
                scores.append((score, action))
            # find the best score in the list and return the action
            bestMove = max(scores, key=lambda x: x[0])
            return bestMove[1]
        else:
            return None

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
