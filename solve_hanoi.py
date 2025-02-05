from search import Problem, astar_search

class TowersOfHanoi(Problem):
    def __init__(self, num_disks, initial=None, goal=None):
        if initial is None:
            initial = (tuple(range(num_disks, 0, -1)), (), ())
        if goal is None:
            goal = ((), (), tuple(range(num_disks, 0, -1)))
        super().__init__(initial, goal)
        self.num_disks = num_disks
        
        # Pre-compute all valid actions
        self._all_actions = tuple((i, j) for i in range(3) for j in range(3) if i != j)

    def actions(self, state):
        """
        Return the list of valid moves from the current state.
        """
        return [(i, j) for i, j in self._all_actions 
                if state[i] and (not state[j] or state[j][-1] > state[i][-1])]

    def result(self, state, action):
        i, j = action
        new_state = [list(peg) for peg in state]  # Converts to list to modify
        new_state[j].append(new_state[i].pop())  # Move disk from i to j
        return tuple(map(tuple, new_state))  # Convert back to tuple of tuples

    def goal_test(self, state):
        return state == self.goal
    
    def h(self, node):
        """
        Heuristic function: Calculates a weighted sum based on
            how far disks are from their goal position.
        """
        peg_weights = [4, 2, 0]
        return sum(disk * peg_weights[peg] for peg in range(3) for disk in node.state[peg])

def show_solution(solution):
    """ Prints the solution steps if found. """
    if not solution:
        print("No solution found.")
        return

    steps = solution.path()
    print(f"Moves required: {len(steps) - 1}")

    for step in steps:
        if step.action:
            src, dest = step.action
            print(f"Move top disk from peg {src + 1} to peg {dest + 1}")
        print("State:", step.state)

def main():
    num_disks = 7
    problem = TowersOfHanoi(num_disks)

    """
    I tried running the search with breadth_first_search (with and without the heuristic to check the results), but it was too slow when setting num_disk to 4
        and almost reaching 100% memory usage when setting num_disk to 5 or higher.
    So the A* search was used instead (as suggested on class), providing a much faster solution with good memory usage.
    Of course, don't abuse the number of disks, as the problem complexity grows exponentially.
    """
    solution = astar_search(problem)

    if solution:
        show_solution(solution)
    else:
        print("Solution not found.")

if __name__ == "__main__":
    main()
