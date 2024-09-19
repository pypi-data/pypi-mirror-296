from datetime import datetime

from colorama import Fore
from tabulate import tabulate

from tasktracker_ehdlg.data_service import add, get, get_id, save


def add_task(description: str):
    new_task = {
        "id": get_id(),
        "description": description,
        "status": "todo",
        "created_at": str(datetime.now()),
        "updated_at": None,
    }

    add(new_task)

    print(f"{Fore.GREEN}Task added succesfully (ID: {new_task.get('id')})")


def delete_task(id: int):
    tasks = get()

    for index, task in enumerate(tasks):
        task_id = task.get("id", None)

        if task_id == id:
            del tasks[index]
            save(tasks)

            print(f"{Fore.GREEN}Task {id} deleted")
            exit()

    return task_not_found(id)


def update(id: int, **new_data):
    tasks = get()

    for task in tasks:
        task_id = task.get("id", None)

        if task_id == id:
            task.update(new_data)

            save(tasks)

            print(f"{Fore.GREEN}Task {id} suffessfully updated")
            exit()

    return task_not_found(id)


def update_description(id: int, new_description: str):
    return update(id, description=new_description)


def mark_done(id: int):
    return update(id, status="done")


def mark_in_progress(id: int):
    return update(id, status="in-progress")


def mark_todo(id: int):
    return update(id, status="todo")


def list_tasks(filter: str):
    tasks = get()

    if len(tasks) == 0:
        print(f"{Fore.YELLOW}There are no tasks yet. Add a new task with <add>")

        exit()

    headers = [["ID", "Description", "Created", "Status"]]

    tasks_values = [
        [
            task.get("id"),
            task.get("description"),
            datetime.strftime(
                datetime.fromisoformat(task.get("created_at")), "%Y-%m-%d"
            ),
            task.get("status"),
        ]
        for task in tasks
        if filter is None or task.get("status") == filter
    ]

    if len(tasks_values) == 0:
        print(f"{Fore.YELLOW}No tasks with the current filter")

        exit()

    data = headers + tasks_values

    return print(tabulate(data, tablefmt="grid"))


def task_not_found(id: int):
    print(f"{Fore.YELLOW}Task {id} not found")

    exit()
