import unittest
from os import path, remove
from task_cli.database import Database
from task_cli.model import TaskDocument

DB_FILE = 'tests/data_testrun.json'


class TestDatabase(unittest.TestCase):
    def tearDown(self):
        if path.exists(DB_FILE):
            remove(DB_FILE)

    def test_init(self):
        db = Database(file_path=DB_FILE, document=TaskDocument)

        self.assertTrue(path.exists(DB_FILE), 'File does not exist.')
        self.assertEqual(db.file_path, DB_FILE, 'File path is not set correctly.')
        self.assertIsInstance(
            db.document, TaskDocument, 'Document is not an instance of TaskDocument.'
        )


if __name__ == '__main__':
    unittest.main()
