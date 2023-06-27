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
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()

        "*** YOUR CODE HERE ***"
        from util import manhattanDistance
        food = newFood.asList()
        foodheusteric = []
        ghostheusteric = []
        reward = 0.0
        for pellet in food:
            foodheusteric.append(manhattanDistance(newPos,pellet))
        for fh in foodheusteric:
            if fh <= 4:
                reward += 1.0#for food closer than 4 we reward 1 point
            elif fh > 4 and fh <= 10:
                reward += 0.3#for food between 4 and 10 we reward 0.3 point
            elif fh > 10 and fh<=16 :
                reward += 0.2#for food between 10 and 16 we reward 0.2 point
            else:
                reward += 0.15#for food farther than 16 we reward 0.15 point
        for ghost in successorGameState.getGhostPositions():
            if manhattanDistance(ghost,newPos) <= 2:
                reward =  -reward#we the action gets us very close to the ghost we multiply it with -1 (worst action possible)
        return successorGameState.getScore()-currentGameState.getScore() + reward
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
        # returns best action
        def minimax(depth,agentIndex,gameState):
            #minimax agent which returns the best score and action
            i=0
            #returning when the depth is 0 or not legal actions
            if not gameState.getLegalActions(agentIndex) or depth==self.depth:
                return self.evaluationFunction(gameState),0
            #if agent index is number of agents -1, we start next ply by increasing depth and chnaging index to 0
            if agentIndex== gameState.getNumAgents()-1:
                depth+=1
                nextIndex=self.index
            #else add index
            else:
                nextIndex=agentIndex+1
            #for every action in legal actions of gamestate, do
            for action in gameState.getLegalActions(agentIndex):
                #if it is the first legal state, give its result of minimax as bestscore and the first action as bestaction
                if i==0:
                    successorState=gameState.generateSuccessor(agentIndex, action)
                    bestScore,best=minimax(depth,nextIndex,successorState)
                    bestAction=action
                    i=1
                else:
                                    
                    successorState=gameState.generateSuccessor(agentIndex, action)
                                        
                    score,Action=minimax(depth,nextIndex,successorState)
                    #if agent is max player update max(bestscore,score) into bestscore
                    if agentIndex==self.index:
                        if bestScore<score:
                            bestScore=score
                            bestAction=action
                    #update min(bestscore,score) for bestscore of min player
                    else:
                        if score<bestScore:
                            bestScore=score
                            bestAction=action
            return bestScore,bestAction
        #returning the action
        return minimax(0,self.index,gameState)[1]
            
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
        #alphabeta functions which return actions after pruning
        def alphabeta(depth,agentIndex,gameState,a,b):
            i=0
            if not gameState.getLegalActions(agentIndex) or depth==self.depth:
                return self.evaluationFunction(gameState),0
            #updating depth and index accordingly
            if agentIndex== gameState.getNumAgents()-1:
                depth+=1
                nextIndex=self.index
            else:
                nextIndex=agentIndex+1
            for action in gameState.getLegalActions(agentIndex):
                #initial
                if i==0:
                    successorState=gameState.generateSuccessor(agentIndex, action)
                    bestScore,best=alphabeta(depth,nextIndex,successorState,a,b)
                    bestAction=action
                    i=1
                    if agentIndex==self.index:
                        a=max(bestScore,a)
                    else:
                        b=min(bestScore,b)
                    #pruning when a>b
                    if a>b:
                        return bestScore,bestAction
                else:
                         
                    successorState=gameState.generateSuccessor(agentIndex, action)
                                        
                    score,Action=alphabeta(depth,nextIndex,successorState,a,b)
                    #updating best score and action and pruning
                    # max player
                    if agentIndex==self.index:
                        if bestScore<score:
                            bestScore=score
                            bestAction=action
                            if a<score:
                                a=score
                            if a>b:
                                return bestScore,bestAction
                    #min player
                    else:
                        if score<bestScore:
                            bestScore=score
                            bestAction=action
                            if b>score:
                                b=score
                            if a>b:
                                return bestScore,bestAction
            return bestScore,bestAction
        #initial value of a is given as negative infinity and b as infinity
        #returning best action using alphabeta function
        return alphabeta(0,self.index,gameState,-float('inf'),float('inf'))[1]
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
        #expectimax , which returns action. Involves chances with min player(ghost)
        def expectimax(depth,agentIndex,gameState):
            i=0
            if not gameState.getLegalActions(agentIndex) or depth==self.depth:
                return self.evaluationFunction(gameState),0
            #p is probability
            p=1.0/len(gameState.getLegalActions(agentIndex))
            #updating depths and index
            if agentIndex== gameState.getNumAgents()-1:
                depth+=1
                nextIndex=self.index
            else:
                nextIndex=agentIndex+1
            for action in gameState.getLegalActions(agentIndex):
                if i==0:
                    successorState=gameState.generateSuccessor(agentIndex, action)
                    best=expectimax(depth,nextIndex,successorState)
                    bestAction=action
                    #for max player no chances involved
                    if agentIndex==self.index:
                        bestScore=best[0]
                    #min player, chances involved
                    else:
                        bestScore=p*best[0]
                    i=1
                else:
                                    
                    successorState=gameState.generateSuccessor(agentIndex, action)
                                        
                    score,Action=expectimax(depth,nextIndex,successorState)
                                        
                    if agentIndex==self.index:
                        if bestScore<score:
                            bestScore=score
                            bestAction=action
                    #updating best score using p
                    else:
                        bestScore+=p*score
                        bestAction=action
            return bestScore,bestAction
        #returning best action
        return expectimax(0,self.index,gameState)[1]
        util.raiseNotDefined()
        

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    
    food = currentGameState.getFood().asList()
    pacmanPosition = currentGameState.getPacmanPosition()
    activeGhosts = []
    scaredGhosts = []
    capsuleCount = len(currentGameState.getCapsules())
    pelletCount = len(food)
    reward = 0.0
    reward += -200*capsuleCount#we want pacman to eat capules(higher priority than eating pellets, hence lesser the number of capsules pacman has to eat the better
    for ghost in currentGameState.getGhostStates():
    #dividing the ghosts into 2 sets, scared and not scared
        if ghost.scaredTimer:
        #these ghosts cant do anything, pacman can earn points by eating it
            scaredGhosts.append(ghost)
        else:
        #these ghosts can eat pacman
            activeGhosts.append(ghost)
    foodDistances = []
    activeGhostsDistances = []
    scaredGhostsDistances = []
    for pellet in food:
    #has the manhattan distances to food pellets
        foodDistances.append(manhattanDistance(pacmanPosition,pellet))

    for ghost in activeGhosts:
    #has the manhattan distances to active ghosts
        scaredGhostsDistances.append(manhattanDistance(pacmanPosition,ghost.getPosition()))

    for ghost in scaredGhosts:
    #has the manhattan distances to scared ghosts
        scaredGhostsDistances.append(manhattanDistance(pacmanPosition,ghost.getPosition()))

#where ever the distances become 0 we write seperate cases as reciprocal of zero is not valid
    for pellet in foodDistances:
        if pellet == 0:
            reward += 0
        else:
            reward += 5 / pellet**pellet#the closer the pellet the better it is hence we use reciprocal of the pellet
    for ghost in scaredGhostsDistances:
        if ghost == 0:
            reward += 0
        elif ghost >0 and ghost <=2:
            reward+= 150/ ghost**ghost#the closer we get to the scared ghost and eat it the better hence we use the reciprocal
        else:
            reward += 40 / ghost**ghost
    for ghost in activeGhostsDistances:
        if ghost == 0:
            reward += 0
        else:
            reward += -200 / ghost**ghost#the farther we stay away from the un scared ghosts the better hence we used negative of the reciprocal

    return currentGameState.getScore() + reward
    #util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

