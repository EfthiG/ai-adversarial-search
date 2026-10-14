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
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        pacmanPos = successorGameState.getPacmanPosition()
        food = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        ghostScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        score = successorGameState.getScore()

        foodList = food.asList()
        if foodList:
            closestFoodDist = min(manhattanDistance(pacmanPos, foodPos) for foodPos in foodList)
            score += 10 / closestFoodDist  # Closer food gives a higher score
        
        
        for ghostState in newGhostStates:
            ghostPos = ghostState.getPosition()
            ghostDist = manhattanDistance(pacmanPos, ghostPos)
            
            if ghostState.scaredTimer > 0: #If ghost is scared, the closer it is the higher is the score
                score += 200 / ghostDist
            else:
                if ghostDist > 0:  #If ghost is active, the closer it is the lower is the score
                    score -= 10 / ghostDist

        return score

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
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def minimax(state, agentIndex, depth):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            # Max->Pacman Min->Ghost

            if agentIndex == 0:  # Pacman(agentIndex->0) 
                return max(
                    minimax(state.generateSuccessor(agentIndex, action), 1, depth) for action in state.getLegalActions(agentIndex)
                )
            else:  # Any other agentIndex is ghost
                nextAgent = agentIndex + 1
                if nextAgent == state.getNumAgents():  # If we've gone through all the agents go back to pacman
                    nextAgent = 0
                    depth += 1
                return min(
                    minimax(state.generateSuccessor(agentIndex, action), nextAgent, depth) for action in state.getLegalActions(agentIndex)
                )

        bestAction = None
        bestScore = float('-inf')
        #find Pacman;s best possible action
        for action in gameState.getLegalActions(0):  # Pacman is agent 0
            score = minimax(gameState.generateSuccessor(0, action), 1, 0)  # Start with ghost agent 1
            if score > bestScore:
                bestScore = score
                bestAction = action

        return bestAction
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # Initialize alpha and beta values
        alpha = float('-inf')
        beta = float('inf')
        
        # Max -> Pacman
        def max_value(state, depth, alpha, beta):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            
            v = float('-inf')
            for action in state.getLegalActions(0):  # Pacman is agent index 0
                v = max(v, min_value(state.generateSuccessor(0, action), depth, 1, alpha, beta))
                if v > beta:  # Beta cutoff
                    return v
                alpha = max(alpha, v)
            return v

        # Min -> Ghost
        def min_value(state, depth, agentIndex, alpha, beta):
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            
            v = float('inf')
            for action in state.getLegalActions(agentIndex):
                if agentIndex == state.getNumAgents() - 1:
                    # If it's the last ghost, increase depth and call max_value for Pacman's turn
                    v = min(v, max_value(state.generateSuccessor(agentIndex, action), depth + 1, alpha, beta))
                else:
                    # Otherwise, call min_value for the next ghost
                    v = min(v, min_value(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1, alpha, beta))
                if v < alpha:  # Alpha cutoff
                    return v
                beta = min(beta, v)
            return v

        best_score = float('-inf')
        best_action = None
        for action in gameState.getLegalActions(0):  # Pacman is agent index 0
            score = min_value(gameState.generateSuccessor(0, action), 0, 1, alpha, beta)
            if score > best_score:
                best_score = score
                best_action = action
            alpha = max(alpha, best_score)

        return best_action

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectimax(state, agentIndex, depth):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            
            # Max -> Pacman
            if agentIndex == 0:
                return max(
                    expectimax(state.generateSuccessor(agentIndex, action), 1, depth) for action in state.getLegalActions(agentIndex) 
                )
            
            # Expected Value -> Ghost
            else:
                nextAgent = agentIndex + 1
                if nextAgent == state.getNumAgents():  # If we've gone through all the agents go back to pacman and increase the depth
                    nextAgent = 0
                    depth += 1  

                actions = state.getLegalActions(agentIndex)
                total = sum(expectimax(state.generateSuccessor(agentIndex, action), nextAgent, depth) for action in actions)
                return total / len(actions)
            
        best_action = None
        best_score = float('-inf')
        for action in gameState.getLegalActions(0):  # Pacman is agent index 0
            score = expectimax(gameState.generateSuccessor(0, action), 1, 0)
            if score > best_score:
                best_score = score
                best_action = action

        return best_action
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    score = currentGameState.getScore()
    
    pacmanPos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    
    foodList = food.asList()
    if foodList:
        closestFoodDist = min(manhattanDistance(pacmanPos, foodPos) for foodPos in foodList)
        score += 10 / closestFoodDist  # Closer food gives a higher score
    
    
    for ghostState in ghostStates:
        ghostPos = ghostState.getPosition()
        ghostDist = manhattanDistance(pacmanPos, ghostPos)
        
        if ghostState.scaredTimer > 0: #If ghost is scared, the closer it is the higher is the score
            score += 200 / ghostDist
        else:
            if ghostDist > 0:  #If ghost is active, the closer it is the lower is the score
                score -= 10 / ghostDist
    
    
    return score
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
