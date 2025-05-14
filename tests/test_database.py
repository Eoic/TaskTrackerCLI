import unittest
from os import path, remove
from task_cli.database import init_db


class TestDatabase(unittest.TestCase):
    db_name = "tests/data_testrun.db"

    def tearDown(self):
        if path.exists(self.db_name):
            remove(self.db_name)

    def test_init(self):
        init_db(self.db_name)
        self.assertTrue(path.exists(self.db_name), "File does not exist.")
