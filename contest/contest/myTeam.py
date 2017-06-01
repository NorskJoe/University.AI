# myTeam.py
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


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game

#################
# Team creation #
#################

from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util, sys
from game import Directions
import game
from util import nearestPoint

DEBUG_SEED = random.randint(1, 5)

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'OffensiveReflexAgent', second = 'DefensiveReflexAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """
  print "SEED: " + str(DEBUG_SEED) + "\n"
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class ReflexCaptureAgent(CaptureAgent):
    """
    A base class for reflex agents that chooses score-maximizing actions
    """

    def registerInitialState(self, gameState):
        self.start = gameState.getAgentPosition(self.index)
        CaptureAgent.registerInitialState(self, gameState)

        self.invaderPresence = False
        self.invaderLocated = False
        self.snatchingFood = False
        self.distributions = util.Counter()
        # self.inisialiseDistrubutions(gameState)

    #######################
    ### ADDED FUNCTIONS ###
    #######################
    def inisialiseDistrubutions(self, gameState):

        for enemy in self.getOpponents(gameState):
            self.distributions[enemy] = util.Counter()
            for pos in self.getLegalPositions(gameState):
                self.distributions[enemy][pos] = 1

        # self.distributions[enemy].normalize()

    def updateDistributions(self, gameState):
        myPos = gameState.getAgentPosition(self.index)
        noisyDists = gameState.getAgentDistances()
        newDistributions = util.Counter()

        for enemy in self.getOpponents(gameState):
            if self.distributions[enemy].totalCount() == 0:
                self.inisialiseDistrubutions(gameState)
            distribution = util.Counter()

            for pos in self.getLegalPositions(gameState):
                manhattanDistance = util.manhattanDistance(myPos, pos)
                currentBelief = self.distributions[enemy][pos]
                probability = gameState.getDistanceProb(manhattanDistance, noisyDists[enemy])
                distribution[pos] = currentBelief * probability
            # distribution.normalize()
            newDistributions[enemy] = distribution
        self.distributions = newDistributions


    def getLegalPositions(self, gameState):
        """
        Gets all valid positions on the grid where a pacman could
        legally be
        """
        legalPositions = []
        walls = gameState.getWalls()

        for x in range(walls.width):
            for y in range(walls.height):
                if not walls[x][y]:
                    legalPositions.append((x,y))
        return legalPositions

    def getEnemyNoisyDistances(self, gameState):
        """
        Gets the 'raw' noisy distances to each enemy (+/- 6)
        """
        noisyEnemyDists = []
        noisyDistances = gameState.getAgentDistances()
        for agent in self.getOpponents(gameState):
            noisyEnemyDists.append(noisyDistances[agent])
        return noisyEnemyDists

    ##########################
    ### STANDARD FUNCTIONS ###
    ##########################
    def chooseAction(self, gameState):
        """
        Picks among the actions with the highest Q(s,a).
        """
        actions = gameState.getLegalActions(self.index)

        # You can profile your evaluation time by uncommenting these lines
        # start = time.time()
        values = [self.evaluate(gameState, a) for a in actions]
        # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

        maxValue = max(values)
        bestActions = [a for a, v in zip(actions, values) if v == maxValue]

        foodLeft = len(self.getFood(gameState).asList())

        if foodLeft <= 2:
            bestDist = 9999
            for action in actions:
                successor = self.getSuccessor(gameState, action)
                pos2 = successor.getAgentPosition(self.index)
                dist = self.getMazeDistance(self.start,pos2)
                if dist < bestDist:
                    bestAction = action
                    bestDist = dist
            return bestAction

        return random.choice(bestActions)

    def getSuccessor(self, gameState, action):
        """
        Finds the next successor which is a grid position (location tuple).
        """
        successor = gameState.generateSuccessor(self.index, action)
        pos = successor.getAgentState(self.index).getPosition()
        if pos != nearestPoint(pos):
            # Only half a grid position was covered
            return successor.generateSuccessor(self.index, action)
        else:
            return successor

    def evaluate(self, gameState, action):
        """
        Computes a linear combination of features and feature weights
        """
        features = self.getFeatures(gameState, action)
        weights = self.getWeights(gameState, action)

        return features * weights

    def getFeatures(self, gameState, action):
        """
        Returns a counter of features for the state
        """
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)
        features['successorScore'] = self.getScore(successor)
        return features

    def getWeights(self, gameState, action):
        """
        Normally, weights do not depend on the gamestate.  They can be either
        a counter or a dictionary.
        """
        weights={
            'successorScore':1.0,
        }

        for key, value in weights.iteritems():
            weights[key] = value * DEBUG_SEED

        return weights


class OffensiveReflexAgent(ReflexCaptureAgent):
  """
  An offensive agent for use in the RMIT pacman AI competition
  @Author Liam - s3372913
  """
  def chooseAction(self, gameState):
    """
    NOTE: Modified from the original function provided in ReflexCaptureAgent.
    Would have liked to call super to prevent copying the code, but super calls in python aren't a good idea apparently.
    """
    actions = gameState.getLegalActions(self.index)

    # Track food held
    # We review our observation history to see changes in food over time.
    myPos = gameState.getAgentState(self.index).getPosition()
    prevGameState = self.getPreviousObservation()
    if myPos == self.start:
      self.foodHeld = 0
    elif len(self.getFood(prevGameState).asList()) - len(self.getFood(gameState).asList()) > 0:
      self.foodHeld += 1

    # If our score increases, we know we banked some enemy pellets, so reset foodHeld
    if prevGameState != None and self.getScore(gameState) > self.getScore(prevGameState):
      self.foodHeld = 0

    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    values = [self.evaluate(gameState, a) for a in actions]
    # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

    # If we have multiple actions of the same maximum value, pick a random one.
    return random.choice(bestActions)

  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    foodList = self.getFood(successor).asList()
    myPos = successor.getAgentState(self.index).getPosition()

    visibleEnemies = [successor.getAgentState(i).getPosition() for i in self.getOpponents(successor)]
    noisyEnemies = [successor.getAgentDistances()[i] for i in self.getOpponents(gameState)]

    features['successorScore'] = -len(foodList)

    # Code modified from project 1 search tasks
    # @Author Liam - s3372913
    # A modified DFS for finding potential dead ends.
    # Catches plenty of cases, but not all of them.

    # @JOSH FIX ME
    # The function seems to work ok. As most deadends are 2-3 tiles in depth
    # The agent just stops on the entrance to the deadend however or ignores it entirely and walks in.
    # Note that 'deadEndAvoidance': -90 is commented out in getWeights function further below.
    def DeadEndCheck(currentState, thisAction):
        from game import Directions
        from game import Actions
        from util import Stack

        PROBABLY_SAFE = 0
        UNSAFE = 2

        if thisAction == Directions.STOP or currentState == None:
            return PROBABLY_SAFE

        frontier = Stack()
        frontier.push((currentState, thisAction))
        depth = 0

        while not frontier.isEmpty():
            # We're going fairly deep, it's likely this isn't a dead end. No promises though!
            if depth >= 3:
                return PROBABLY_SAFE

            # Evaluate available children. We ignore stop actions and actions that would take us backwards.
            (state, action) = frontier.pop()
            for legalAction in state.getLegalActions(self.index):
                if (legalAction != Directions.STOP and legalAction != Actions.reverseDirection(action)):
                    newState = state.generateSuccessor(self.index, legalAction)
                    frontier.push((newState, legalAction))
            depth += 1

        # We couldn't go very deep at all, it's likely this is a dead end!
        return UNSAFE

    # Dead end evaluation
    if len(visibleEnemies) > 0 and not all(enemy is None for enemy in visibleEnemies):
        features['deadEndAvoidance'] = DeadEndCheck(gameState, action)

    # Compute distance to the nearest food
    if len(foodList) > 0:
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      features['distanceToFood'] = minDistance

    # Track close enemies, avoid when in danger.
    # We focus on when we're holding food.
    features['enemyAvoidance'] = 0
    if len(visibleEnemies) > 0 and not all(enemy is None for enemy in visibleEnemies):
      closestEnemy = min([self.getMazeDistance(myPos, visibleEnemy) for visibleEnemy in visibleEnemies if visibleEnemy != None])
      if closestEnemy <= 4: # and self.foodHeld > 0:
        features['enemyAvoidance'] = closestEnemy

    # Track noisy enemy positions
    #TODO Think of a good way to handle noisy positions.

    # Desire to return (related to amount of food currently held)
    if self.foodHeld >= 3:
      features['desireToReturn'] = self.getMazeDistance(myPos, self.start)
      self.snatchingFood = False
    else:
      features['desireToReturn'] = 0
      self.snatchingFood = True

    # Look for potential capsules to grab
    capsules = self.getCapsules(successor)
    if capsules:
        closestCapsule = min([self.getMazeDistance(myPos, capsule) for capsule in capsules])
        if closestCapsule <= 3:
            features['powerCapsule'] = closestCapsule

    return features

  def getWeights(self, gameState, action):
    weights={
      'successorScore'  : 100,
      'distanceToFood'  : -5,
      'desireToReturn'  : -50,
      'enemyAvoidance'  : -200,
      'deadEndAvoidance': -50,
      #'noisyDist': 1,
      'powerCapsule': -1
    }

    for key, value in weights.iteritems():
      weights[key] = value * DEBUG_SEED

    return weights

class DefensiveReflexAgent(ReflexCaptureAgent):
    """
    An offensive agent for use in the RMIT pacman AI competition.
    Modified from baselineTeam.
    @Author Joseph Johnson - s3542413
    """
    def chooseAction(self, gameState):
        actions = gameState.getLegalActions(self.index)
        values = [self.evaluate(gameState,a) for a in actions]
        maxValue = max(values)
        bestActions = [a for a, v in zip(actions,values) if v == maxValue]
        return random.choice(bestActions)

    def getFeatures(self, gameState, action):
        # first update distributions FIXME
        # self.updateDistributions(gameState)

        features = util.Counter()
        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()
        initialPos = successor.getInitialAgentPosition(self.index)
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
        centreOfBoard = (gameState.getWalls().width/2, gameState.getWalls().height/2)

        # Check centre is valid
        if centreOfBoard not in self.getLegalPositions(gameState):
            centreOfBoard = self.getClosestValidPosition(gameState, centreOfBoard)

        # Check if we just killed an invader (or we lost them)
        if self.invaderLocated == True and len(invaders) == 0:
            self.invaderPresence = False
            self.invaderLocated = False


        # Computes distance to closest invader, within 5 tiles
        if len(invaders) > 0:
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
            features['invaderDistance'] = min(dists)
            self.invaderPresence = True
            self.invaderLocated = True


        # Compute location of invader based on where food has been eaten
        if len(invaders) == 0:
            prevState = self.getPreviousObservation()
            currentState = self.getCurrentObservation()
            if prevState != None:
                previousFoodList = self.getFoodYouAreDefending(prevState).asList()
                currentFoodList = self.getFoodYouAreDefending(currentState).asList()

                if len(previousFoodList) > len(currentFoodList):
                    # Some food has been eaten. Find location where food has
                    # disappeared
                    self.invaderPresence = True
                    difference = list(set(previousFoodList) - set(currentFoodList))
                    pos = difference[0] # difference could have more than one item if several invaders at once eating food
                    distance = self.getMazeDistance(myPos, pos)
                    features['searchForInvader'] = distance





        # Calulating if we can snatch food.  No enemies are present
        if not self.invaderPresence:
            actualEnemyDists = [self.getMazeDistance(myPos, a.getPosition()) for a in enemies if a.getPosition() != None]
            if actualEnemyDists:
                self.snatchingFood = False
            # Calculate if there is any food nearby
            else:
                GET_FOOD_THRESHOLD = 7
                foodList = self.getFood(successor).asList()
                closestFood = min([self.getMazeDistance(myPos, food) for food in foodList])
                if closestFood < GET_FOOD_THRESHOLD:
                    self.snatchingFood = True
                    features['snatchFood'] = closestFood
                else:
                    self.snatchFood = False

        prevGameState = self.getPreviousObservation()
        if self.snatchingFood:
            # check if food is adjacent to current position
            adjPositions = self.getAdjacentPositions(myPos, gameState)
            for pos in adjPositions:
                if pos in self.getFood(successor).asList():
                    features['eatFood'] = 1

        # If there is an unknown invader, move to middle of 'zone'
        if self.invaderPresence:
            x,y = centreOfBoard
            centreOfZone = x/2,y/2
            # Check the value is valid
            if centreOfZone not in self.getLegalPositions(gameState):
                centreOfZone = self.getClosestValidPosition(gameState, centreOfZone)

            distanceFromMiddle = self.getMazeDistance(myPos, centreOfZone)
            features['midZoneDistance'] = distanceFromMiddle

        # Computes most likely position of invader
        # if self.invaderPresence:
        #     for enemy in self.getOpponents(gameState):
        #         x,y = self.distributions[enemy].argMax()
        #         walls = gameState.getWalls()
        #         onRedTeam = gameState.isOnRedTeam(self.index)
        #
        #         if onRedTeam: # 'Home' is left hand side of board
        #             if x < walls.width/2:
        #                 distance = self.getMazeDistance(myPos, (x,y))
        #                 features['noisyDistance'] = distance
        #         else: # Home is right hand side
        #             if x > walls.width/2:
        #                 distance = self.getMazeDistance(myPos, (x,y))
        #                 features['noisyDistance'] = distance


        if self.invaderPresence:
            # First get 'raw' noisy distances
            noisyEnemyDists = self.getEnemyNoisyDistances(gameState)
            noisyDistances = gameState.getAgentDistances()
            features['noisyDistance'] = min(noisyEnemyDists)




        # Computes whether we're on defense (1) or offense (0)
        features['onDefense'] = 1
        if myState.isPacman:
             features['onDefense'] = 0

        # Computes number of current invaders we can see
        features['numInvaders'] = len(invaders)


        if action == Directions.STOP:
            features['stop'] = 1

        rev = Directions.REVERSE \
            [gameState.getAgentState(self.index).configuration.direction]
        if action == rev:
            features['reverse'] = 1

        # Compute if currently scared or not
        if myState.scaredTimer > 0:
            features['invaderDistance'] = -features['invaderDistance']



        # Favour staying in the centre of the board, only if no invaders
        if not self.invaderPresence and not self.snatchingFood:
            distanceFromCentre = self.getMazeDistance(myPos, centreOfBoard)
            features['centreDistance'] = distanceFromCentre

        return features

    def evaluate(self, gameState, action):
        """
        Computes a linear combination of features and feature weights
        """
        features = self.getFeatures(gameState, action)
        weights = self.getWeights(gameState, action)
        # print "features: ", features
        # print "weights: ", weights
        # print "action: ", action
        # print "features * weights: ", features*weights
        # print "\n"
        return features * weights

    def getWeights(self, gameState, action):
        weights={
            'numInvaders': -600,
            'onDefense': 1.5, # cross over score
            'invaderDistance': -10000, # go towards invaders (closest)
            'noisyDistance': -500, # go towards probable location (closest)
            'snatchFood': -200, # go towards food when no enemies
            'stop': -100,
            'reverse': -2,
            'scared': -100,
            'searchForInvader': -100,
            'centreDistance': -1, # go towards centre
            'midZoneDistance': -1, # go towards middle of zone
            'eatFood': -10
        }

        # for key, value in weights.iteritems():
        #    weights[key] = value * DEBUG_SEED

        return weights

    #######################################
    #### HELPER FUNCTIONS FOR DEFENDER ####
    #######################################
    def getClosestValidPosition(self, gameState, currPosition):
        distances = []
        for newPosition in self.getLegalPositions(gameState):
            distance = util.manhattanDistance(currPosition,newPosition)
            distances.append((distance,newPosition))
        closest = min(distances, key=lambda x: x[0])
        return closest[1]

    def getAdjacentPositions(self, currPosition, gameState):
        validPositions = []
        x,y = currPosition
        for newX,newY in [(x+i,y+j) for i in (-1,0,1) for j in (-1,0,1) if i != 0 or j != 0]:
            if (newX,newY) in self.getLegalPositions(gameState):
                validPositions.append((newX,newY))
        return validPositions
