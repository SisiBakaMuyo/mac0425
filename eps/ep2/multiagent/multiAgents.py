# Ísis Ardisson Logullo Nusp: 7577410
#
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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction'):
        self.evaluationFunction = util.lookup(evalFn, globals())

    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        successors = [(gameState.generatePacmanSuccessor(action)) for action in legalMoves]
        scores = [self.evaluationFunction(succesor) for successors in successors]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        return legalMoves[chosenIndex]

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
        
        def minimax(state, depth, agentIndex):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            
            numAgents = state.getNumAgents()
            nextAgent = (agentIndex + 1) % numAgents
            nextDepth = depth - 1 if nextAgent == 0 else depth
            
            legalActions = state.getLegalActions(agentIndex)
            if not legalActions:
                return self.evaluationFunction(state)
            
            if agentIndex == 0:
                return max(minimax(state.generateSuccessor(agentIndex, action), nextDepth, nextAgent) 
                           for action in legalActions)
            else:
                return min(minimax(state.generateSuccessor(agentIndex, action), nextDepth, nextAgent) 
                           for action in legalActions)

        legalMoves = gameState.getLegalActions(0)
        bestAction = max(
            legalMoves,
            key=lambda action: minimax(gameState.generateSuccessor(0, action), self.depth, 1)
        )
        
        return bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):

    def getAction(self, gameState: GameState):
        
        def alphaBeta(state, depth, agentIndex, alpha, beta):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            
            numAgents = state.getNumAgents()
            nextAgent = (agentIndex + 1) % numAgents
            nextDepth = depth - 1 if nextAgent == 0 else depth
            
            legalActions = state.getLegalActions(agentIndex)
            if not legalActions:
                return self.evaluationFunction(state)
            
            if agentIndex == 0:
                v = float("-inf")
                for action in legalActions:
                    successor = state.generateSuccessor(agentIndex, action)
                    v = max(v, alphaBeta(successor, nextDepth, nextAgent, alpha, beta))
                    if v > beta:
                        return v
                    alpha = max(alpha, v)
                return v
            else:
                v = float("inf")
                for action in legalActions:
                    successor = state.generateSuccessor(agentIndex, action)
                    v = min(v, alphaBeta(successor, nextDepth, nextAgent, alpha, beta))
                    if v < alpha:
                        return v
                    beta = min(beta, v)
                return v

        alpha = float("-inf")
        beta = float("inf")
        bestAction = None
        v = float("-inf")
        legalMoves = gameState.getLegalActions(0)
        
        for action in legalMoves:
            successor = gameState.generateSuccessor(0, action)
            score = alphaBeta(successor, self.depth, 1, alpha, beta)
            
            if score > v:
                v = score
                bestAction = action

            alpha = max(alpha, v)
            
        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):

    def getAction(self, gameState: GameState):
        
        def expectimax(state, depth, agentIndex):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            
            numAgents = state.getNumAgents()
            nextAgent = (agentIndex + 1) % numAgents
            nextDepth = depth - 1 if nextAgent == 0 else depth
            
            legalActions = state.getLegalActions(agentIndex)
            if not legalActions:
                return self.evaluationFunction(state)
            
            if agentIndex == 0:
                return max(expectimax(state.generateSuccessor(agentIndex, action), nextDepth, nextAgent) 
                           for action in legalActions)            
            else:
                successorValues = [expectimax(state.generateSuccessor(agentIndex, action), nextDepth, nextAgent) 
                                   for action in legalActions]
                return sum(successorValues) / len(legalActions)

        legalMoves = gameState.getLegalActions(0)
        bestAction = max(
            legalMoves,
            key=lambda action: expectimax(gameState.generateSuccessor(0, action), self.depth, 1)
        )
        
        return bestAction

def betterEvaluationFunction(currentGameState: GameState):
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood().asList()
    ghosts = currentGameState.getGhostStates()
    score = currentGameState.getScore()
    # Incentive to get food
    if food:
        # Minimize distanace to closest food
        minFoodDist = min(manhattanDistance(pos, f) for f in food)
        score += 10.0 / (minFoodDist + 1)
        # Minimize remaining food
        score -= 4 * len(food)
    # Avoid ghosts
    for ghost in ghosts:
        ghostPos = ghost.getPosition()
        dist = manhattanDistance(pos, ghostPos)
        # Get closer to scared ghosts
        if ghost.scaredTimer > 0:
            score += 20.0 / (dist + 1)
        else:
            if dist <= 1:
                # Avoid immediate death
                score -= 500
            else:
                # Get away from ghosts
                score -= 2.0 / dist
    return score

# Abbreviation
better = betterEvaluationFunction
