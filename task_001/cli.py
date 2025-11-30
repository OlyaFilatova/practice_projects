import argparse
from .lib.cli_controller import (
    list_tasks,
    add_task,
    change_task_status,
    update_task,
    delete_task,
)

parser = argparse.ArgumentParser(
    prog="Task manager.",
    description="A simple TODO list.",
)

subparsers = parser.add_subparsers(help="Task actions.")

list_subparser = subparsers.add_parser("list", help="List tasks.")
list_subparser.add_argument(
    "status", choices=["done", "todo", "in-progress"], nargs="?", default=None
)
list_subparser.set_defaults(func=list_tasks)

create_subparser = subparsers.add_parser("add", help="Create task.")
create_subparser.add_argument("description")
create_subparser.set_defaults(func=add_task)

update_subparser = subparsers.add_parser("update", help="Update task.")
update_subparser.add_argument("index")
update_subparser.add_argument("description")
update_subparser.set_defaults(func=update_task)

status_subparser = subparsers.add_parser("mark-todo", help="Change task status.")
status_subparser.add_argument("index")
status_subparser.set_defaults(status="todo")
status_subparser.set_defaults(func=change_task_status)

status_subparser = subparsers.add_parser("mark-in-progress", help="Change task status.")
status_subparser.add_argument("in-progress")
status_subparser.set_defaults(status="in-progress")
status_subparser.set_defaults(func=change_task_status)

status_subparser = subparsers.add_parser("mark-done", help="Change task status.")
status_subparser.add_argument("index")
status_subparser.set_defaults(status="done")
status_subparser.set_defaults(func=change_task_status)

delete_subparser = subparsers.add_parser("delete", help="Delete task.")
delete_subparser.add_argument("index")
delete_subparser.set_defaults(func=delete_task)

args = parser.parse_args()
if "func" in args:
    args.func(**args.__dict__)
else:
    parser.print_help()
