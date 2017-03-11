# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
        stack will hold a 3-tuple:
        current: position of the current node in the graph
        directions list: list of directions used to move to this node
        visited list: list of nodes already visisted

        Summary:
        1. Initialise stack
        2. Take currentNode from top of stack
        3. If already visited, take next node
        4. If not visisted, check if it is the goal and return list of directions used to get there
        5. If not the goal, push the currentNode to the stack, along with the nextDirection used to get there, and add it to the list of visisted nodes
        6. When returning, the list of directions stored in stack[1] should be the correct solution using DFS
    """
    # first initialise the stack
    from util import Stack
    stack = Stack()
    stack.push((problem.getStartState(), [], []))

    while not stack.isEmpty():
        current, directions, visited = stack.pop()
        for nextNode, nextDirection, previousNodes in problem.getSuccessors(current):
            if nextNode not in visited:
                if problem.isGoalState(nextNode):
                    return directions + [nextDirection]
                stack.push((nextNode, directions + [nextDirection], visited
                    + [current] ))

    # return []

def breadthFirstSearch(problem):

    """
        Summary:
        1. Queue contains frontier of nodes that algorithm is searching (FIFO)
        2. Each node is visited or not visited
        3. For each node that is in frontier that has not been visited, mark it as visisted and check for goal
    """

    from util import Queue
    q = Queue()
    q.push((problem.getStartState(), [], []))

    while not q.isEmpty():
        current, directions, visited = q.pop()
        if problem.isGoalState(current):
            return directions
        for nextNode, nextDirection, previousNodes in problem.getSuccessors(current):
            if nextNode not in visited:
                q.push((nextNode, directions + [nextDirection], visited + [current]))

    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
