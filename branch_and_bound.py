"""

    Branch and bound algorithm
    Author: Adam Novak
    License: MIT

"""


def branch_and_bound(scheduled_tasks: list, unscheduled_tasks: list, length: int, tasks: list[dict[str, int]], best_solution: dict) -> bool:

    """
        Branch-and-bound algorithm for task scheduling.

        Args:
        - scheduled_tasks (list): List of tasks already scheduled.
        - unscheduled_tasks (list): List of tasks yet to be scheduled.
        - length (int): Current time length of the schedule.
        - tasks (list[dict[str, int]]): List of tasks with release times, processing times, and deadlines.
        - best_solution (dict): Dictionary to store the best solution found with keys 'upper_bound' and 'schedule'.

        Returns:
        - bool: True if an optimal feasible solution is found, False otherwise.
    """

    # (1) make sure that all unassigned tasks will not miss their deadline if assigned
    for t in unscheduled_tasks:
        if max(length, tasks[t]['release_time']) + tasks[t]['processing_time'] > tasks[t]['deadline']:
            return False

    # (solution) there is nothing to schedule
    if len(unscheduled_tasks) == 0:
        if length < best_solution['upper_bound']:
            best_solution['upper_bound'] = length
            best_solution['schedule'] = scheduled_tasks
        return False

    # (2) find lower bound when tasks can be finished
    lower_bound = max(length, min(tasks[t]['release_time'] for t in unscheduled_tasks)) + sum(tasks[t]['processing_time'] for t in unscheduled_tasks)
    if lower_bound >= best_solution['upper_bound']:
        return False

    # (3) decomposition
    is_optimal_partial_solution = False
    if length <= min(tasks[t]['release_time'] for t in unscheduled_tasks):
        is_optimal_partial_solution = True

    # branch
    for i in range(len(unscheduled_tasks)):
        if branch_and_bound(scheduled_tasks + [unscheduled_tasks[i]], unscheduled_tasks[:i] + unscheduled_tasks[i + 1:], max(length, tasks[unscheduled_tasks[i]]['release_time']) + tasks[unscheduled_tasks[i]]['processing_time'], tasks, best_solution):
            return True

    return is_optimal_partial_solution


if __name__ == "__main__":

    # define tasks
    tasks = [
        {'processing_time': 2, 'release_time': 4, 'deadline': 7},
        {'processing_time': 1, 'release_time': 1, 'deadline': 5},
        {'processing_time': 2, 'release_time': 1, 'deadline': 6},
        {'processing_time': 2, 'release_time': 0, 'deadline': 4},
    ]

    # structure for best solution
    best_solution = {
        'schedule': [],
        'upper_bound': max(task['deadline'] + 1 for task in tasks)  # default upper bound as max deadline + 1
    }

    # split tasks to scheduled and unscheduled
    scheduled_tasks = []
    unscheduled_tasks = [i for i in range(len(tasks))]

    # branch and bound
    branch_and_bound(scheduled_tasks, unscheduled_tasks, 0, tasks, best_solution)

    # print solution
    if len(best_solution['schedule']) == 0:
        print('No solution :/')
    else:
        print('Schedule', best_solution['schedule'], 'with length', best_solution['upper_bound'])
        length = 0
        for task in best_solution['schedule']:
            print('task', task, 'starts at time', max(length, tasks[task]['release_time']))
            length = max(length, tasks[task]['release_time']) + tasks[task]['processing_time']
