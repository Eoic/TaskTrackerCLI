from datetime import datetime
from itertools import tee
import unittest
from os import path, remove
from task_cli.database import init_db
from task_cli.model import CreateTask, Status, UpdateTask
from task_cli.repository import TaskRepository

DB_FILE = "tests/data_testrun.json"


class TestTaskRepository(unittest.TestCase):
    db_name = "tests/data_testrun.db"

    def setUp(self):
        init_db(self.db_name)
        repo = TaskRepository(db=self.db_name)
        t1 = CreateTask(status=Status.TODO, description="Task #1")
        t2 = CreateTask(status=Status.IN_PROGRESS, description="Task #2")
        t3 = CreateTask(status=Status.DONE, description="Task #3")
        tasks = [t1, t2, t3]

        for task in tasks:
            repo.add(task)

    def tearDown(self):
        if path.exists(self.db_name):
            remove(self.db_name)

    def test_add(self):
        repo = TaskRepository(db=self.db_name)
        self.assertEqual(repo.size(), 3, "Repository size mismatch.")

        for task_id in [1, 2, 3]:
            task = repo.find_by_id(task_id)

            self.assertIsNotNone(
                task, f"Task with id {task_id} not found in repository."
            )

            self.assertEqual(
                task.id if task is not None else None,
                task_id,
                f"Task with id {task_id} not found in repository.",
            )

    def test_find_by_id(self):
        repo = TaskRepository(db=self.db_name)

        t1 = repo.find_by_id(1)
        t2 = repo.find_by_id(2)
        t3 = repo.find_by_id(3)
        t4 = repo.find_by_id(4)

        self.assertIsNotNone(t1, "Task with id 1 not found in repository.")
        self.assertIsNotNone(t2, "Task with id 2 not found in repository.")
        self.assertIsNotNone(t3, "Task with id 3 not found in repository.")
        self.assertIsNone(t4, "Task with id 4 found in repository.")

    def test_find_by_status(self):
        repo = TaskRepository(db=self.db_name)
        tasks_all = repo.find_by_status()
        tasks_todo = repo.find_by_status([Status.TODO])
        tasks_in_progress = repo.find_by_status([Status.IN_PROGRESS])
        tasks_done = repo.find_by_status([Status.DONE])
        self.assertEqual(len(tasks_all), 3, "Status filter mismatch.")
        self.assertEqual(len(tasks_todo), 1, "Status filter mismatch.")
        self.assertEqual(len(tasks_in_progress), 1, "Status filter mismatch.")
        self.assertEqual(len(tasks_done), 1, "Status filter mismatch.")

    def test_due_date(self):
        repo = TaskRepository(db=self.db_name)
        task_no_due = repo.add(CreateTask(status=Status.TODO, description="Coding."))

        if not task_no_due:
            self.fail("Could not create new task.")

        self.assertIsNone(task_no_due.due_date)

        repo.update(
            task_no_due,
            UpdateTask(due_date=datetime.strptime("2025-05-17", "%Y-%m-%d").date()),
        )

        task_due = repo.find_by_id(task_no_due.id)

        if not task_due:
            self.fail("Could not find updated task.")

        self.assertIsNotNone(task_due.due_date)
        self.assertEqual(str(task_due.due_date), "2025-05-17")

    def test_update(self):
        repo = TaskRepository(db=self.db_name)
        task = repo.find_by_id(1)

        self.assertEqual(
            task.status if task is not None else None,
            Status.TODO,
            "Initial status mismatch.",
        )

        if task is None:
            self.fail("Task with id 1 not found in repository.")

        repo.update(task, UpdateTask(status=Status.IN_PROGRESS))

        updated_task = repo.find_by_id(1)

        if updated_task is None:
            self.fail("Task with id 1 not found in repository after update.")

        self.assertEqual(
            updated_task.status,
            Status.IN_PROGRESS,
            "Status value mismatch - did not update to expected value.",
        )

    def test_delete(self):
        repo = TaskRepository(db=self.db_name)
        self.assertEqual(repo.size(), 3, "Repository size mismatch.")

        for task in repo.find_by_status():
            repo.delete_by_id(task.id)

        self.assertEqual(repo.size(), 0, "Repository size mismatch.")


if __name__ == "__main__":
    unittest.main()
