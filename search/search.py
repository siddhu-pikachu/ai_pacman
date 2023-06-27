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
                cost = problem.getCostOfActions(interm)               # in UCS we check for the cost to perform the action
                if successor not in explored:
                    frontier.push((child['state']),cost)
                    path.push(interm,cost)
        currentstate = frontier.pop()
        actionList = path.pop()
    return actionList
    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

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


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
