from ..interfaces.state_space_problem import StateSpaceProblem
from ..data_structures.priority_queue import PriorityQueue
import time

def branch_and_bound_search(problem: StateSpaceProblem, statistics=False):
    """
    Branch and Bound search algorithm.

    :param problem: An object representing the problem to be solved, which
                    must be inherited from the StateSpaceProblem interface.
    :param statistics: An optional function to return the 'time', 'inferences', and 'cost'. Default is false.
    :return: A tuple containing the solution.
    """
    start_time = time.time()
    visited = set()
    priority_queue = PriorityQueue()
    initial_state = problem.initial_state()
    priority_queue.push((initial_state, []), 0)
    inferences = 0
    best_solution = None
    best_cost = float("inf")

    while not priority_queue.is_empty():
        accumulated_cost, (state, path) = priority_queue.pop()
        inferences += 1

        if problem.goal_check(state):
            if accumulated_cost < best_cost:
                best_solution = path + [state]
                best_cost = accumulated_cost
                continue

        if state in visited:
            continue

        visited.add(state)

        for operator in problem.operators():
            successor = problem.apply_operator(operator, state)
            if successor is not None and successor not in visited:
                current_cost = problem.cost(state, successor)
                new_accumulated_cost = accumulated_cost + current_cost
                if new_accumulated_cost < best_cost:
                    priority_queue.push((successor, path + [state]), new_accumulated_cost)

    elapsed_time = time.time() - start_time
    full_path = best_solution
    if statistics:
        return {'path': full_path}, {'visited': visited}, {'time': elapsed_time, 'inferences': inferences, 'cost': best_cost} # Cost can be inf
    else:
        return full_path