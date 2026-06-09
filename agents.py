from ai_helper import ask_ai


class ProjectManager:
    def __init__(self, name="PM_Agent"):
        self.name = name

    def assign_tasks(self, board, developers, current_day):
        ready_tasks = board.get_ready_tasks()

        for task in ready_tasks:
            free_devs = [dev for dev in developers if dev.current_task is None]
            if not free_devs:
                break

            developer_names = [dev.name for dev in free_devs]

            prompt = f"""
You are a Project Manager agent.

Current day: {current_day}
Task: {task.name}
Description: {task.description}
Priority: {task.priority}
Deadline: Day {task.deadline}
Available developers: {developer_names}

Choose the best developer for this task.
Reply in this format:
Developer: <name>
Reason: <short reason>
"""

            decision = ask_ai(prompt)

            selected_dev = free_devs[0]
            for dev in free_devs:
                if f"Developer: {dev.name}" in decision:
                    selected_dev = dev
                    break

            task.assigned_to = selected_dev.name
            task.status = "In Progress"
            selected_dev.current_task = task

            board.log(f"{self.name} AI Decision -> {decision}")

    def review_progress(self, board, current_day):
        pending = sum(1 for t in board.tasks if t.status == "Pending")
        progress = sum(1 for t in board.tasks if t.status == "In Progress")
        testing = sum(1 for t in board.tasks if t.status == "Testing")
        done = sum(1 for t in board.tasks if t.status == "Done")

        board.log(
            f"{self.name}: Day {current_day} review -> "
            f"Pending: {pending}, In Progress: {progress}, Testing: {testing}, Done: {done}"
        )

        overdue_tasks = board.get_overdue_tasks(current_day)
        if overdue_tasks:
            overdue_names = ", ".join(task.name for task in overdue_tasks)
            board.log(f"{self.name}: Warning - overdue tasks detected: {overdue_names}")


class Developer:
    def __init__(self, name):
        self.name = name
        self.current_task = None

    def work(self, board, current_day):
        if self.current_task is None:
            board.log(f"{self.name}: No task assigned today.")
            return

        task = self.current_task
        task.days_worked += 1

        prompt = f"""
You are a Developer agent.

Developer name: {self.name}
Task: {task.name}
Description: {task.description}
Day worked: {task.days_worked}
Estimated days: {task.estimated_days}

Write a short daily progress update in one sentence.
"""
        progress_update = ask_ai(prompt)
        board.log(f"{self.name} AI Update -> {progress_update}")

        if current_day > task.deadline:
            board.log(f"{self.name}: '{task.name}' is past its deadline, prioritizing completion.")

        if task.days_worked >= task.estimated_days:
            task.status = "Testing"
            board.log(f"{self.name}: Development completed for '{task.name}'. Sending to testing.")
            self.current_task = None


class Tester:
    def __init__(self, name="Tester_Agent"):
        self.name = name

    def test(self, board, developers):
        testing_tasks = board.get_testing_tasks()

        for task in testing_tasks:
            prompt = f"""
You are a QA Tester agent.

Task: {task.name}
Description: {task.description}
Days worked: {task.days_worked}
Previous bugs found: {task.bugs_found}

Decide whether this task should PASS or FAIL in testing.
Reply in exactly this format:
Result: PASS or FAIL
Reason: <short reason>
"""

            result = ask_ai(prompt)
            board.log(f"{self.name} AI Review -> {result}")

            if "Result: FAIL" in result:
                task.bugs_found += 1
                task.status = "In Progress"
                task.comments.append(result)

                for dev in developers:
                    if dev.name == task.assigned_to and dev.current_task is None:
                        dev.current_task = task
                        break
            else:
                task.status = "Done"


class Client:
    def __init__(self, name="Client_Agent"):
        self.name = name

    def feedback(self, board):
        done_tasks = [t for t in board.tasks if t.status == "Done"]
        if done_tasks:
            task = done_tasks[-1]
            prompt = f"""
You are a Client agent.

Completed feature: {task.name}
Description: {task.description}

Give short client feedback in one sentence.
"""
            feedback = ask_ai(prompt)
            board.log(f"{self.name} AI Feedback -> {feedback}")