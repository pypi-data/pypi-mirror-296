import argparse

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command")

add_parser = subparsers.add_parser("add", help="Add a new task")
add_parser.add_argument("description", help="Task description", type=str)

delete_parser = subparsers.add_parser("delete", help="Delete an existing task")
delete_parser.add_argument("id", type=int, help="Task's ID")

update_parser = subparsers.add_parser("update", help="Update an existing task")
update_parser.add_argument("id", help="Task's ID", type=int)
update_parser.add_argument("description", help="New task description", type=str)


mark_in_progress = subparsers.add_parser(
    "mark-in-progress", help="Change the task status to 'in progress'"
)
mark_in_progress.add_argument("id", type=int, help="Task's ID")

mark_done = subparsers.add_parser("mark-done", help="Change the task status to 'done'")
mark_done.add_argument("id", type=int, help="Taks's ID")

mark_todo = subparsers.add_parser("mark-todo", help="Change the task status to 'todo'")
mark_todo.add_argument("id", type=int, help="Task's ID")

list_todos = subparsers.add_parser("list", help="List the task in a table")
list_todos.add_argument(
    "filter",
    type=str,
    help="Filter the tasks by their status",
    default=None,
    nargs="?",
    choices=("done", "todo", "in-progress"),
)
