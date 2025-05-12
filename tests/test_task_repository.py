# import unittest
# from os import path, remove
# from task_cli.database import Database
# from task_cli.model import Status, Task, TaskDocument
# from task_cli.repository import TaskRepository

# DB_FILE = 'tests/data_testrun.json'


# class TestTaskRepository(unittest.TestCase):
#     def setUp(self):
#         db = Database(file_path=DB_FILE, document=TaskDocument)
#         repo = TaskRepository(db=db)
#         t1 = Task(status=Status.TODO, description='Task #1')
#         t2 = Task(status=Status.IN_PROGRESS, description='Task #2')
#         t3 = Task(status=Status.DONE, description='Task #3')
#         tasks = [t1, t2, t3]

#         for task in tasks:
#             repo.add(task)

#     def tearDown(self):
#         if path.exists(DB_FILE):
#             remove(DB_FILE)

#     def test_add(self):
#         db = Database(file_path=DB_FILE, document=TaskDocument)
#         repo = TaskRepository(db=db)
#         self.assertEqual(repo.size(), 3, 'Repository size mismatch.')

#         for task_id in [1, 2, 3]:
#             task = repo.find_by_id(task_id)
#             self.assertIsNotNone(
#                 task, f'Task with id {task_id} not found in repository.'
#             )
#             self.assertEqual(
#                 task.id,
#                 task_id,
#                 f'Task with id {task_id} not found in repository.',
#             )

#         self.assertEqual(repo.db.document.next_id, 4, 'Next ID mismatch.')

#     def test_find_by_id(self):
#         db = Database(file_path=DB_FILE, document=TaskDocument)
#         repo = TaskRepository(db=db)

#         t1 = repo.find_by_id(1)
#         t2 = repo.find_by_id(2)
#         t3 = repo.find_by_id(3)
#         t4 = repo.find_by_id(4)

#         self.assertIsNotNone(t1, 'Task with id 1 not found in repository.')
#         self.assertIsNotNone(t2, 'Task with id 2 not found in repository.')
#         self.assertIsNotNone(t3, 'Task with id 3 not found in repository.')
#         self.assertIsNone(t4, 'Task with id 4 found in repository.')

#     def test_find_by_status(self):
#         db = Database(file_path=DB_FILE, document=TaskDocument)
#         repo = TaskRepository(db=db)

#         tasks_all = repo.find_by_status()
#         tasks_todo = repo.find_by_status([Status.TODO])
#         tasks_in_progress = repo.find_by_status([Status.IN_PROGRESS])
#         tasks_done = repo.find_by_status([Status.DONE])
#         self.assertEqual(len(tasks_all), 3, 'Status filter mismatch.')
#         self.assertEqual(len(tasks_todo), 1, 'Status filter mismatch.')
#         self.assertEqual(len(tasks_in_progress), 1, 'Status filter mismatch.')
#         self.assertEqual(len(tasks_done), 1, 'Status filter mismatch.')

#     def test_update(self):
#         db = Database(file_path=DB_FILE, document=TaskDocument)
#         repo = TaskRepository(db=db)

#         task = repo.find_by_id(1)

#         self.assertEqual(task.status, Status.TODO, 'Initial status mismatch.')
#         repo.update(task, {'status': Status.IN_PROGRESS})
#         self.assertEqual(
#             repo.find_by_id(1).status, Status.IN_PROGRESS, 'Status mismatch.'
#         )

#     def test_delete(self):
#         db = Database(file_path=DB_FILE, document=TaskDocument)
#         repo = TaskRepository(db=db)

#         self.assertEqual(repo.size(), 3, 'Repository size mismatch.')

#         for task in repo.find_by_status():
#             repo.delete_by_id(task.id)

#         self.assertEqual(repo.size(), 0, 'Repository size mismatch.')


# if __name__ == '__main__':
#     unittest.main()
