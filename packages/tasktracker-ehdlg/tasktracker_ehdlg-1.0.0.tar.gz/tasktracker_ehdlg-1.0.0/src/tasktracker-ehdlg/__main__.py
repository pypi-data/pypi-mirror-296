from parser import parser

from actions import (
    add_task,
    delete_task,
    list_tasks,
    mark_done,
    mark_in_progress,
    mark_todo,
    update,
)

args = parser.parse_args()

ACTIONS = {
    "add": lambda args: add_task(args.description),
    "delete": lambda args: delete_task(args.id),
    "update": lambda args: update(args.id, description=args.description),
    "mark-in-progress": lambda args: mark_in_progress(args.id),
    "mark-done": lambda args: mark_done(args.id),
    "mark-todo": lambda args: mark_todo(args.id),
    "list": lambda args: list_tasks(args.filter),
}


if args.command is None:
    parser.print_help()

    exit()

ACTIONS[args.command](args)
