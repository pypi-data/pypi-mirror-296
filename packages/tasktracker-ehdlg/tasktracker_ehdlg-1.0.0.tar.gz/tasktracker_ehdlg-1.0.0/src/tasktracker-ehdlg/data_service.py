import json

DEFAULT_FILE_VALUE: list = []


def get() -> list:
    try:
        with open("../data.json", "r") as tasks_file:
            raw_data = tasks_file.read()
            data = json.loads(raw_data)

            return data
    except Exception:
        save(DEFAULT_FILE_VALUE)

        return DEFAULT_FILE_VALUE


def add(new_task):
    tasks = get()

    tasks.append(new_task)

    save(tasks)


def save(new_tasks: list) -> None:
    with open("../data.json", "w+") as f:
        json.dump(new_tasks, f)


def get_id():
    tasks = get()

    if not tasks:
        return 1

    tasks_sorted = sorted(tasks, key=lambda x: x.get("id", float("inf")))

    last_id = 0
    for task in tasks_sorted:
        task_id = task.get("id", None)

        if task_id is not None:
            if task_id - last_id > 1:
                return last_id + 1

            last_id = task_id

    return last_id + 1
