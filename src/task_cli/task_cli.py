from task_cli.database import Database
from task_cli.model import Task, TaskDocument
from task_cli.repository import TaskRepository
from task_cli.utils import serialize, deserialize


def main():
    database = Database(file_path='data.json', document=TaskDocument)
    repository = TaskRepository(database)
    # t1 = Task(status='todo', description='Task 1')
    # t2 = Task(status='todo', description='Task 2')
    # t3 = Task(status='todo', description='Task 3')
    # repository.add(t1)
    # repository.add(t2)
    # repository.add(t3)
    repository.delete(1)
