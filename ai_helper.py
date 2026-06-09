import random

task_bug_counts = {}


def ask_ai(prompt: str) -> str:
    prompt_lower = prompt.lower()

    if "choose the best developer" in prompt_lower:
        if "dev1" in prompt_lower:
            return "Developer: Dev1\nReason: Dev1 is available and suitable."
        return "Developer: Dev2\nReason: Dev2 is available and suitable."

    if "daily progress update" in prompt_lower:
        return "I am making steady progress on the assigned task."

    if "pass or fail" in prompt_lower:
        task_name = "general_task"

        if "task:" in prompt_lower:
            try:
                after_task = prompt_lower.split("task:")[1]
                task_name = after_task.split("\n")[0].strip()
            except Exception:
                task_name = "general_task"

        if task_name not in task_bug_counts:
            task_bug_counts[task_name] = 0

        # Payment system can fail only 1 time, then must pass
        if "payment" in task_name:
            if task_bug_counts[task_name] < 1:
                task_bug_counts[task_name] += 1
                return "Result: FAIL\nReason: Payment validation needs improvement."
            return "Result: PASS\nReason: Issues resolved successfully."

        # Other tasks mostly pass
        if random.random() < 0.05:
            return "Result: FAIL\nReason: Minor issue found during testing."

        return "Result: PASS\nReason: Task meets requirements."

    if "client feedback" in prompt_lower:
        return "The feature looks good and meets expectations."

    return "Default AI response."