# import unittest
# from os import path, remove
# from task_cli.model import Task

# DB_FILE = 'tests/data_testrun.json'


# class TestTask(unittest.TestCase):
#     def tearDown(self):
#         if path.exists(DB_FILE):
#             remove(DB_FILE)

#     def test_init_task(self):
#         task = Task(status='TODO', description='Task #1')
#         self.assertEqual(task.id, None, 'Task status mismatch.')
#         self.assertEqual(task.status, 'TODO', 'Task status mismatch.')
#         self.assertEqual(task.description, 'Task #1', 'Task description mismatch.')
#         self.assertIsNone(task.id, 'Task id is not None.')
#         self.assertIsNone(task.updated_at, 'Task updated_at is not None.')
#         self.assertIsNotNone(task.created_at, 'Task created_at is None.')


# if __name__ == '__main__':
#     unittest.main()
