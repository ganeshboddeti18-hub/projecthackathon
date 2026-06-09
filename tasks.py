from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    name: str
    priority: int
    description: str = ""
    deadline: int = 5
    status: str = "Pending"
    assigned_to: Optional[str] = None
    days_worked: int = 0
    estimated_days: int = 2
    bugs_found: int = 0
    dependencies: List[str] = field(default_factory=list)
    comments: List[str] = field(default_factory=list)

    def can_start(self, board) -> bool:
        done_tasks = [t.name.strip().lower() for t in board.tasks if t.status == "Done"]
        for dep in self.dependencies:
            if dep.strip().lower() not in done_tasks:
                return False
        return True


class ProjectBoard:
    def __init__(self, tasks: List[Task]):
        self.tasks = tasks
        self.logs: List[str] = []

    def log(self, message: str) -> None:
        self.logs.append(message)
        print(message)

    def get_completed(self) -> List[str]:
        return [t.name for t in self.tasks if t.status == "Done"]

    def all_done(self) -> bool:
        return all(t.status == "Done" for t in self.tasks)

    def get_ready_tasks(self) -> List[Task]:
        ready = [
            t for t in self.tasks
            if t.status == "Pending" and t.can_start(self)
        ]
        return sorted(ready, key=lambda x: x.priority)

    def get_testing_tasks(self) -> List[Task]:
        return [t for t in self.tasks if t.status == "Testing"]

    def get_in_progress_tasks(self) -> List[Task]:
        return [t for t in self.tasks if t.status == "In Progress"]

    def get_overdue_tasks(self, current_day: int) -> List[Task]:
        return [
            t for t in self.tasks
            if t.status != "Done" and current_day > t.deadline
        ]