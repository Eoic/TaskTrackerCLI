import sys
import argparse
from task_cli.database import Database
from task_cli.model import Status, Task, TaskDocument
from task_cli.repository import TaskRepository


def build_list_parser(subparsers):
    parser_list = subparsers.add_parser(
        'list',
        help='List tasks.',
        usage='%(prog)s [status]',
    )
    parser_list.add_argument(
        'status',
        nargs='?',
        help='Filter tasks by status.',
        default=None,
        type=str,
    )


def build_add_parser(subparsers):
    parser_add = subparsers.add_parser(
        'add',
        help='Add a new task.',
        usage='%(prog)s <description>',
    )
    parser_add.add_argument(
        'description',
        help='Description of the task.',
        nargs=1,
        type=str,
    )


def build_update_parser(subparsers):
    parser_update = subparsers.add_parser(
        'update',
        help='Update a task.',
        usage='%(prog)s <id> <description>',
    )
    parser_update.add_argument(
        'id',
        help='ID of the task.',
        nargs=1,
        type=int,
    )
    parser_update.add_argument(
        'description',
        help='Description of the task.',
        nargs=1,
        type=str,
    )


def build_delete_parser(subparsers):
    parser_delete = subparsers.add_parser(
        'delete',
        help='Delete a task.',
        usage='%(prog)s <id>',
    )

    parser_delete.add_argument(
        'id',
        help='ID of the task.',
        nargs=1,
        type=int,
    )


def build_mark_parser(subparsers):
    for status in Status:
        mark_parser = subparsers.add_parser(
            f'mark-{status.value.lower()}',
            help=f'Mark task as "{status.value}".',
            usage='%(prog)s <id>',
        )

        mark_parser.add_argument(
            'id',
            help='Set task status.',
            nargs=1,
            type=int,
        )


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='task-cli',
        description='A CLI tool for managing TODOs.',
    )

    subparsers = parser.add_subparsers(dest='command')
    build_list_parser(subparsers)
    build_add_parser(subparsers)
    build_update_parser(subparsers)
    build_delete_parser(subparsers)
    build_mark_parser(subparsers)

    return parser


def process_command(args: argparse.Namespace):
    repository = TaskRepository(
        db=Database(file_path='data.json', document=TaskDocument)
    )

    match args.command:
        case 'list':
            process_list_command(repository, args.status)
            return
        case 'add':
            process_add_command(repository, args.description[0])
            return
        case 'update':
            process_update_command(repository, args.id[0], args.description[0])
            return
        case 'delete':
            process_delete_command(repository, args.id[0])
            return

    if not args.command.startswith('mark-'):
        return

    _, _, new_status = args.command.rpartition('mark-')
    process_set_status(repository, args.id[0], new_status)


def process_list_command(repository: TaskRepository, status: str):
    filter_status = None

    for valid_status in Status:
        if valid_status.value == status:
            filter_status = valid_status
            break

    tasks = (
        repository.find_by_status([filter_status])
        if status
        else repository.find_by_status()
    )

    for task in tasks:
        print(task)

    if len(tasks) == 0:
        print("No tasks to show.")


def process_add_command(repository: TaskRepository, description: str):
    task = Task(description=description, status=Status.TODO)
    repository.add(task)
    print(task)


def process_update_command(repository: TaskRepository, id: int, description: str):
    task = repository.find_by_id(id)

    if task is None:
        print(f'Task with id {id} was not found.', file=sys.stderr)
        return

    if repository.update(task, {'description': description}):
        print(repository.find_by_id(id))
        return

    print('Could not update task.', file=sys.stderr)


def process_delete_command(repository: TaskRepository, id: int):
    if repository.delete_by_id(id):
        print('Task was deleted successfully.')
        return

    print('Could not delete task.', file=sys.stderr)


def process_set_status(repository: TaskRepository, id: int, status: str):
    for valid_status in Status:
        if valid_status.value == status:
            task = repository.find_by_id(id)

            if not task:
                print('Could not find task to update.', file=sys.stderr)
                return

            repository.update(task, {'status': valid_status})
            task = repository.find_by_id(task.id)
            print(task)
            return

    print('Could not set new task status.', file=sys.stderr)
