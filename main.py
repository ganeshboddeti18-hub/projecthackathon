from tasks import Task, ProjectBoard
from agents import ProjectManager, Developer, Tester, Client


def calculate_smart_deadlines(task_inputs):
    """
    Calculate smarter deadlines based on:
    - estimated_days
    - dependencies
    - priority
    - small safety buffer
    """

    deadline_map = {}
    unresolved = task_inputs[:]

    # Keep assigning until all deadlines are resolved
    while unresolved:
        progress_made = False

        for item in unresolved[:]:
            name = item["name"].strip()
            dependencies = [dep.strip() for dep in item["dependencies"] if dep.strip()]
            estimated_days = int(item["estimated_days"])
            priority = int(item["priority"])

            # Can calculate only if all dependency deadlines are known
            if all(dep in deadline_map for dep in dependencies):
                if dependencies:
                    dependency_finish = max(deadline_map[dep] for dep in dependencies)
                else:
                    dependency_finish = 0

                # Priority effect:
                # higher priority number = less urgent
                # smaller priority number = more urgent
                priority_buffer = max(1, priority)

                # Safety buffer for testing/rework
                testing_buffer = 1

                # Smart deadline formula
                deadline = dependency_finish + estimated_days + testing_buffer + priority_buffer

                deadline_map[name] = deadline
                unresolved.remove(item)
                progress_made = True

        if not progress_made:
            # fallback in case of circular / invalid dependencies
            for item in unresolved:
                name = item["name"].strip()
                estimated_days = int(item["estimated_days"])
                priority = int(item["priority"])
                deadline_map[name] = estimated_days + priority + 2
            break

    return deadline_map


def run_simulation(task_inputs, developer_count=2, max_days=20):
    tasks = []

    # Calculate smart deadlines first
    smart_deadlines = calculate_smart_deadlines(task_inputs)

    for item in task_inputs:
        clean_name = item["name"].strip()
        clean_description = item["description"].strip()
        clean_dependencies = [dep.strip() for dep in item["dependencies"] if dep.strip()]

        task = Task(
            name=clean_name,
            priority=int(item["priority"]),
            description=clean_description,
            deadline=smart_deadlines[clean_name],
            estimated_days=int(item["estimated_days"]),
            dependencies=clean_dependencies,
        )
        tasks.append(task)

    board = ProjectBoard(tasks)

    pm = ProjectManager("PM_Agent")
    developers = [Developer(f"Dev{i+1}") for i in range(developer_count)]
    tester = Tester("Tester_Agent")
    client = Client("Client_Agent")

    current_day = 1

    while not board.all_done() and current_day <= max_days:
        board.log(f"========== DAY {current_day} ==========")

        pm.review_progress(board, current_day)
        pm.assign_tasks(board, developers, current_day)

        for developer in developers:
            developer.work(board, current_day)

        tester.test(board, developers)

        if current_day % 2 == 0:
            client.feedback(board)

        current_day += 1

    if board.all_done():
        board.log("Project completed successfully.")
    else:
        board.log("Project was not fully completed within the maximum allowed days.")

    return board, current_day - 1