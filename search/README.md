def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    from util import Stack
    frontier = Stack()
    frontier.push(problem.getStartState())                          # getting the start state into frontier
    explored = []                                                   # list to store the explored nodes
    actionList = []                                                 # book keeping the path from start to the goal using a list
    path = Stack()                                                  # Stack to maintaing path from start to a state
    currentstate = frontier.pop()                                   # as we pushed 'problem.getStartState()' ie. start state into frontier
                                                                    # we now that start state and store it in currentstate to evaluate it.
    while not problem.isGoalState(currentstate):                    # evaluating currentstate (checking if it is not goal state)
        if currentstate not in explored:
            explored.append(currentstate)                           # basically we are removing current state from frontier and storing it in
                                                                    # explored if it is not already explored and is not goal state.
            successors = problem.getSuccessors(currentstate)
            for child in successors:
                frontier.push(child[0])                             # storing the child in frontier
                                                                    # these are actions to go from one atomic state to the next atomic state
                                                                    # the construction of the actual solution ( ie. the set of actions to get
                path.push(actionList + [child[1]])                  # from start to goal state )
        actionList = path.pop()
        currentstate = frontier.pop()
    return actionList
    #util.raiseNotDefined()

/////////////////////////////////////////////////////////////////////

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    from util import Queue
    frontier = Queue()
    frontier.push(problem.getStartState())                          # getting the start state into frontier
    explored = []                                                   # list to store the explored nodes
    actionList = []                                                 # book keeping the path from start to the goal using a list
    path = Queue()                                                  # fifo queue to maintaing path from start to a state
    currentstate = frontier.pop()                                   # as we pushed 'problem.getStartState()' ie. start state into frontier,
                                                                    # we now popping it and storing it in currentstate to evaluate it.
    while not problem.isGoalState(currentstate):                    # evaluating currentstate (checking if it is not goal state)
        if currentstate not in explored:
            explored.append(currentstate)                           # basically we are removing current state from frontier and storing it in
                                                                    # explored if it is not already explored and is not goal state.
            successors = problem.getSuccessors(currentstate)
            for child in successors:
                frontier.push(child[0])                             # storing the child in frontier
                                                                    # these are actions to go from one atomic state to the next atomic state
                                                                    # the construction of the actual solution ( ie. the set of actions to get
                path.push(actionList + [child[1]])                  # from start to goal state )
        actionList = path.pop()
        currentstate = frontier.pop()
    return actionList
    #util.raiseNotDefined()

/////////////////////////////////////////////////////////////////////

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    from util import PriorityQueue
    frontier = PriorityQueue()                                      # frontier to manage which states to expand
    frontier.push(problem.getStartState(),0)                        # getting the start state into frontier
    explored = []                                                   # list to check whether state has already been explored
    interm = []                                                     # temporary variable to get intermediate paths
    actionList = []                                                 # list to store sequence of directions/actions to goal from start state
    path = PriorityQueue()                                          # priorityqueue to store direction to child
    currentstate = frontier.pop()
    while not problem.isGoalState(currentstate):
        if currentstate not in explored:
            explored.append(currentstate)
            successors = problem.getSuccessors(currentstate)
            for successor in successors:
                child = {'state':successor[0],'direction':successor[1],'cost':successor[2]}
                interm = actionList + [child['direction']]
                cost = problem.getCostOfActions(interm)             # in UCS we check for the cost to perform the action
                if successor not in explored:
                    frontier.push((child['state']),cost)
                    path.push(interm,cost)
        currentstate = frontier.pop()
        actionList = path.pop()
    return actionList
    #util.raiseNotDefined()
/////////////////////////////////////////////////////////////////////

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    from util import PriorityQueue
    frontier = PriorityQueue()                                      # frontier to manage which states to expand
    frontier.push(problem.getStartState(),0)                        # getting the start state into frontier
    explored = []                                                   # list to check whether state has already been explored
    interm = []                                                     # temporary variable to get intermediate paths
    actionList = []                                                 # list to store sequence of directions/actions to goal from start state
    path = PriorityQueue()                                          # priorityqueue to store direction to child
    currentstate = frontier.pop()
    while not problem.isGoalState(currentstate):                    # evaluating nodes from frontier and goal test the current node
        if currentstate not in explored:
            explored.append(currentstate)                           # adding current node from frontier to explared if it has not been explored
            successors = problem.getSuccessors(currentstate)        # expanding current node
            for successor in successors:
                child = {'state':successor[0],'direction':successor[1],'cost':successor[2]}
                interm = actionList + [child['direction']]
                cost = problem.getCostOfActions(interm) + heuristic((child['state']),problem)# in a* search cost is f(n)=g(n)+h(n) hence we add heuristic cost
                if successor not in explored:
                    frontier.push((child['state']),cost)
                    path.push(interm,cost)
        currentstate = frontier.pop()
        actionList = path.pop()
    return actionList
    #util.raiseNotDefined()
/////////////////////////////////////////////////////////////////////

class FoodSearchProblem:
    """
    A search problem associated with finding the a path that collects all of the
    food (dots) in a Pacman game.

    A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
      pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
      foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food
    """
    def __init__(self, startingGameState):
        self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0 # DO NOT CHANGE
        self.heuristicInfo = {} # A dictionary for the heuristic to store information

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state[1].count() == 0

    def getSuccessors(self, state):
        "Returns successor states, the actions they require, and a cost of 1."
        successors = []
        self._expanded += 1 # DO NOT CHANGE
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state[0]
            dx, dy = Actions.directionToVector(direction)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextFood = state[1].copy()
                nextFood[nextx][nexty] = False
                successors.append( ( ((nextx, nexty), nextFood), direction, 1) )
        return successors

    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999"""
        x,y= self.getStartState()[0]
        cost = 0
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1
        return cost
//////////////////////////////////////////////////////////////////////

def cornersHeuristic(state, problem):
    """
    A heuristic for the CornersProblem that you defined.
      state:   The current search state
               (a data structure you chose in your search problem)
      problem: The CornersProblem instance for this layout.
    This function should always return a number that is a lower bound on the
    shortest path from the state to a goal of the problem; i.e.  it should be
    admissible (as well as consistent).
    """
    corners = problem.corners # These are the corner coordinates
    walls = problem.walls # These are the walls of the maze, as a Grid (game.py)
    corner = state[0]
    exploredcorner = state[1]
    #Finding out the not visited corners
    unexploredcorners = []
    for cornernode in corners:
        if not (cornernode) in exploredcorner:
            unexploredcorners.append(cornernode)
    heuristicvalue=[0]
    for cornernode in unexploredcorners:
        heuristicvalue.append(mazeDistance(corner,cornernode,problem.startingGameState))
    return max(heuristicvalue)
    
    
/////////////////////////////////////////////////////////////////////////

class AStarFoodSearchAgent(SearchAgent):
    "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, foodHeuristic)
        self.searchType = FoodSearchProblem

def foodHeuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come
    up with an admissible heuristic; almost all admissible heuristics will be
    consistent as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the
    other hand, inadmissible or inconsistent heuristics may find optimal
    solutions, so be careful.

    The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a Grid
    (see game.py) of either True or False. You can call foodGrid.asList() to get
    a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the
    problem.  For example, problem.walls gives you a Grid of where the walls
    are.

    If you want to *store* information to be reused in other calls to the
    heuristic, there is a dictionary called problem.heuristicInfo that you can
    use. For example, if you only want to count the walls once and store that
    value, try: problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access
    problem.heuristicInfo['wallCount']
    """
    pacmanposition, foodGrid = state
    foodposition = foodGrid.asList()
    heuristic = [0]
    for pos in foodposition:
        heuristic.append(mazeDistance(pacmanposition,pos,problem.startingGameState))
    return max(heuristic)
    return 0

