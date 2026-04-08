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
# ---------
# Isis Ardisson Logullo
# nUSP 7577410


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

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    # funcao que foi criada
    from util import Stack

    pilha = Stack()
    visitados = set()
    pilha.push((problem.getStartState(), None, None))

    while not pilha.isEmpty():
        no_atual = pilha.pop()
        estado, pai, acao = no_atual

        if problem.isGoalState(estado):
            return reconstruir_caminho(problem.getStartState(), no_atual)

        if estado not in visitados:
            visitados.add(estado)

            sucessores = problem.getSuccessors(estado)
            for proximo_estado, acao_sucessora, custo in sucessores:
                novo_no = (proximo_estado, no_atual, acao_sucessora)
                pilha.push(novo_no)

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    # funcao que foi criada
    from util import Queue

    fila = Queue()
    visitados = {}

    estado_inicial = problem.getStartState()
    fila.push((estado_inicial, None, None))
    visitados[estado_inicial] = True

    while not fila.isEmpty():
        no_atual = fila.pop()
        estado, pai, acao = no_atual

        if problem.isGoalState(estado):
            return reconstruir_caminho(estado_inicial, no_atual)

        sucessores = problem.getSuccessors(estado)
        for proximo_estado, acao_sucessora, custo in sucessores:
            if proximo_estado not in visitados:
                visitados[proximo_estado] = True
                novo_no = (proximo_estado, no_atual, acao_sucessora)
                fila.push(novo_no)

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    # funcao que foi criada
    from util import PriorityQueue

    fila_prioridade = PriorityQueue()
    visitados = {}

    estado_inicial = problem.getStartState()
    no_inicial = (estado_inicial, None, None, 0)
    fila_prioridade.push(no_inicial, 0)

    while not fila_prioridade.isEmpty():
        no_atual = fila_prioridade.pop()
        estado, pai, acao, custo_atual = no_atual

        if problem.isGoalState(estado):
            return reconstruir_caminho(estado_inicial, no_atual)

        if estado in visitados and visitados[estado] <= custo_atual:
            continue

        visitados[estado] = custo_atual

        sucessores = problem.getSuccessors(estado)
        for proximo_estado, acao_sucessora, custo_passo in sucessores:
            custo_total = custo_atual + custo_passo
            novo_no = (proximo_estado, no_atual, acao_sucessora, custo_total)

            if proximo_estado not in visitados or visitados[proximo_estado] > custo_total:
                fila_prioridade.push(novo_no, custo_total)

def nullHeuristic(state, problem: SearchProblem = None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    # funcao que foi criada
    from util import PriorityQueue

    fila_prioridade = PriorityQueue()
    visitados = {}

    estado_inicial = problem.getStartState()
    no_inicial = (estado_inicial, None, None, 0)

    # f(n) = g(n) + h(n)
    prioridade_inicial = 0 + heuristic(estado_inicial, problem)
    fila_prioridade.push(no_inicial, prioridade_inicial)

    while not fila_prioridade.isEmpty():
        no_atual = fila_prioridade.pop()
        estado, pai, acao, custo_g_atual = no_atual

        if problem.isGoalState(estado):
            return reconstruir_caminho(estado_inicial, no_atual)

        if estado in visitados and visitados[estado] <= custo_g_atual:
            continue

        visitados[estado] = custo_g_atual

        sucessores = problem.getSuccessors(estado)
        for proximo_estado, acao_sucessora, custo_passo in sucessores:
            custo_g_novo = custo_g_atual + custo_passo
            novo_no = (proximo_estado, no_atual, acao_sucessora, custo_g_novo)

            # f(n) = g(n) + h(n)
            valor_f = custo_g_novo + heuristic(proximo_estado, problem)

            if proximo_estado not in visitados or visitados[proximo_estado] > custo_g_novo:
                fila_prioridade.push(novo_no, valor_f)


# Código obrigatórios para a pós-graduação:

def iddfsSearch(problem: SearchProblem):
    """Search the deepest nodes in the search tree first, limited by an iteratively increasing depth.
    Create an additional function if needed.
    """
    # funcao que foi criada
    profundidade = 0
    while True:
        resultado = buscaProfundidadeLimitada(problem, profundidade)
        if resultado is not None:
            return resultado
        profundidade += 1

def buscaProfundidadeLimitada(problem, limit):
    """
    Função auxiliar que executa DFS até um limite específico.
    """
    from util import Stack

    pilha = Stack()
    estado_inicial = problem.getStartState()
    pilha.push((estado_inicial, None, None, 0))
    visitados = {}

    while not pilha.isEmpty():
        no_atual = pilha.pop()
        estado, pai, acao, profundidade = no_atual

        if problem.isGoalState(estado):
            return reconstruir_caminho(estado_inicial, no_atual)

        if profundidade < limit:
            if estado not in visitados or visitados[estado] > profundidade:
                visitados[estado] = profundidade

                sucessores = problem.getSuccessors(estado)
                for proximo_estado, acao_sucessora, custo in sucessores:
                    novo_no = (proximo_estado, no_atual, acao_sucessora, profundidade + 1)
                    pilha.push(novo_no)

    return None


def policyToPlan(problem: SearchProblem, policy):
    """Convert policy (state-to-action map) to plan (sequence of actions)."""
    plan = []
    state = problem.getStartState()
    while not problem.isGoalState(state):
        action, state = policy[state]
        plan.append(action)
    return plan

def lrtaStarTrial(problem: SearchProblem, H, state, heuristic=nullHeuristic):
    """Simulate an execution from the given state to a goal state and return the traced path."""
    policy = {}
    while not problem.isGoalState(state):
        successors = problem.getSuccessors(state)
        if not successors:
            return None  # dead end
        # Select child with smaller f = H + cost
        best_child = None
        best_action = None
        best_f = float('inf')
        for (child, action, cost) in successors:
            if child not in H:
                H[child] = heuristic(child, problem)
            f = cost + H[child]
            if f < best_f:
                best_child = child
                best_action = action
                best_f = f
        # Update H[state]
        H[state] = best_f
        # Update policy
        policy[state] = (best_action, best_child)
        # Move to next state
        state = best_child
    return policyToPlan(problem, policy)

def lrtaStarSearch(problem: SearchProblem, heuristic=nullHeuristic, trials=5):
    """Execute a number of trials of LRTA* and return the best plan found."""
    s0 = problem.getStartState()
    H = {}
    H[s0] = heuristic(s0, problem)
    for _ in range(trials):
        plan = lrtaStarTrial(problem, H, s0, heuristic)
    print("Final H-value of the initial state: %s" % H[s0])
    return plan

# funcao que foi criada
def reconstruir_caminho(inicio, objetivo):
    no_pai = objetivo
    solucao = []
    while no_pai[0] != inicio:
        solucao.append(no_pai[2])
        no_pai = no_pai[1]
    return solucao[::-1]


# Abbreviations
# *** DO NOT CHANGE THESE ***
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
iddfs = iddfsSearch
lrta = lrtaStarSearch
