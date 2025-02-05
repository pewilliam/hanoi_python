from search import Problem, astar_search

class TowersOfHanoi(Problem):
    def __init__(self, num_disks, initial=None, goal=None):
        if initial is None:
            initial = (tuple(range(num_disks, 0, -1)), (), ())
        if goal is None:
            goal = ((), (), tuple(range(num_disks, 0, -1)))
        super().__init__(initial, goal)
        self.num_disks = num_disks
        
        # Pré-computar as ações possíveis
        self._all_actions = tuple((i, j) for i in range(3) for j in range(3) if i != j)

    def actions(self, state):
        """
        Retorna apenas ações válidas usando tuplas pré-computadas
        """
        return [(i, j) for i, j in self._all_actions 
                if state[i] and (not state[j] or state[j][-1] > state[i][-1])]

    def result(self, state, action):
        i, j = action
        new_state = [list(peg) for peg in state]  # Converte para lista mutável
        new_state[j].append(new_state[i].pop())  # Move o disco
        return tuple(map(tuple, new_state))  # Converte de volta para tupla

    def goal_test(self, state):
        return state == self.goal

    def h(self, node):
        """
        Heurística: Soma do peso dos discos multiplicado pelo peso da haste onde se encontram.
        """
        haste_pesos = [4, 2, 0]
        return sum(disco * haste_pesos[haste] for haste in range(3) for disco in node.state[haste])


def print_solution(solution):
    if solution is None:
        print("Nenhuma solução encontrada!")
        return
    
    path = solution.path()
    print("Número de movimentos: ", len(path) - 1)
    
    for i, node in enumerate(path):
        if i > 0:  # Evita verificar node.action para o primeiro nó
            print(f"Mover disco da haste {node.action[0] + 1} para a haste {node.action[1] + 1}")
        print("Estado: ", node.state)
    print("\nSolução completa.")

def main():
    num_disks = 7
    problem = TowersOfHanoi(num_disks)
    
    """
    Usando A* ao invés de breadth_first_tree_search, pois tentei com ela primeiro e o código demorava
    horrores pra finalizar com 4 discos e de 5 pra cima nem finalizava por estourar a memória.
    """
    solution = astar_search(problem)
    
    if solution:
        print_solution(solution)
    else:
        print("Solução não encontrada.")

if __name__ == '__main__':
    main()