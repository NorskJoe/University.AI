# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        """
        using manhattan distance on potential new position:
            if ghost within 1 tiles: score -100, else score +100
            if food within 5 tiles: score + 100
            get reciprocal of each score
            return gScore/fScore + next move score
        """
        # foodScore = 0.0
        # ghostScore = 0.0
        # for ghost in newGhostStates:
        #     distance = manhattanDistance(ghost.getPosition(), newPos)
        #     if(distance <= 1):
        #         ghostScore -= 100
        #     else: # distance is greater score + 100
        #         ghostScore += 100
        #
        # for food in newFood.asList():
        #     distance = manhattanDistance(food, newPos)
        #     if(distance <= 5):
        #         foodScore += 100
        #     else: # calculate score based on 100 / distance to food
        #         foodScore += 100.0/distance
        #
        # # ghostScore = 1/ghostScore
        # # foodScore = 1/foodScore
        # return (foodScore/ghostScore) + successorGameState.getScore()

        # food score
        closestFood = 10000
        # get the manhattan distance to the closest food
        for food in newFood.asList():
            distance = manhattanDistance(newPos, food)
            if distance < closestFood:
                closestFood = distance
        # foodScore is the reciprocal of manhattan distance os closest food
        foodScore = 1.0 / closestFood

        # ghost score
        # get the ghost score in the same way of getting the food score
        closestGhost = 10000
        for ghost in newGhostStates:
            # if closest ghost is 'scared' and within 3 tiles return a high (good) score
            if ghost.scaredTimer > 0 and distance <= 3:
                return 10000
            distance = manhattanDistance(newPos, ghost.getPosition())
            if distance < closestGhost:
                closestGhost = distance
        # if the ghost is within 1 tile, return a low (bad) score
        if closestGhost <= 1:
            return -10000
        # ghostScore is the reciprocal of manhattan distance to closest ghost
        ghostScore = 1.0 / closestGhost

        totalScaredTime = sum(newScaredTimes)

        return successorGameState.getScore() + foodScore/ghostScore + totalScaredTime


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agent):
            Returns a list of legal actions for an agent
            agent=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agent, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        # call control function starting at depth 0 and agent=pacman (0)
        bestMove = self.minimaxControl(gameState, 0, 0)
        return bestMove[0]
    """
    Control function is called, checks max/min player and depth calls
    appropriate function.  Also has terminal check for ending recursion.
    """
    def minimaxControl(self, gameState, depth, agent):
        if agent >= gameState.getNumAgents():
            agent = 0 # go back to pacman for next depth
            depth += 1

        # terminal state Check
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        if agent == 0: # pacman (max-player)
            return self.maxFunction(gameState, depth, agent)
        else: # ghost (min-player)
            return self.minFunction(gameState, depth, agent)

    """
    maxFunction called when checking pacman's move.  Returns the move
    that will maximise score of all possible legal pacman actions.
    Return value is a tuple of [action, score] for easy access
    """
    def maxFunction(self, gameState, depth, agent):
        legalActions = gameState.getLegalActions(agent)
        bestMove = [None, -10000]

        for action in legalActions:
            score = self.minimaxControl(gameState.generateSuccessor
                (agent, action), depth, agent+1)
            if isinstance(score, list):
                if score[1] > bestMove[1]:
                    bestMove = [action, score[1]]
            else:
                if score > bestMove[1]:
                    bestMove = [action, score]
        return bestMove

    """
    Works the same as maxFunction, called when checking ghost's move.
    """
    def minFunction(self, gameState, depth, agent):
        legalActions = gameState.getLegalActions(agent)
        bestMove = [None, 10000]

        for action in legalActions:
            score = self.minimaxControl(gameState.generateSuccessor
                (agent, action), depth, agent+1)
            if isinstance(score, list):
                if score[1] < bestMove[1]:
                    bestMove = [action, score[1]]
            else:
                if score < bestMove[1]:
                    bestMove = [action, score]
        return bestMove
    """
    First attempt.  Changed to make it more readable and separated into
        functions
    """
    # """
    # Recursive function:
    # Builds the tree from bottom to top.
    # """
    # def miniMaxFunction(self, gameState, depth, agent):
    #     # check if at terminal node/state. Return the score/utility for this
    #     # node
    #     if depth > self.depth or gameState.isWin() or gameState.isLose():
    #         return self.evaluationFunction(gameState)
    #
    #     # get legal actions
    #     actions = gameState.getLegalActions(agent)
    #
    #     # update next iteration values
    #     # first go through all agents for given depth
    #     # then move onto next depth and start at agent 0 (pacman)
    #     nextAgent = agent + 1
    #     nextDepth = depth
    #     if nextAgent >= gameState.getNumAgents():
    #         nextAgent = 0
    #         nextDepth += 1
    #
    #     # get the score/utility for each state by recursively calling function
    #     # for each successor of current agent-depth state
    #     scores = []
    #     for action in actions:
    #         scores.append(self.miniMaxFunction
    #             (gameState.generateSuccessor(agent, action),
    #                 nextDepth, nextAgent))
    #
    #     # first move for pacman, does not occur until tree is built
    #     if agent == 0 and depth == 1:
    #         bestAction = max(scores)
    #         indices = []
    #         for index in range(len(scores)):
    #             if scores[index] == bestAction:
    #                 indices.append(index)
    #         return actions[random.choice(indices)]
    #
    #     if agent == 0: # pacman
    #         return max(scores)
    #     else: # ghost
    #         return min(scores)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
