import sqlite3
from typing import List, Union
from datetime import date, datetime
from task_cli.model import CreateTask, Status, Task, UpdateTask


class TaskRepository:
    def __init__(self, db: str):
        self.db = db

    def __hydrate(self, row):
        return Task(
            id=row[0],
            description=row[1],
            status=Status(row[2]),
            due_date=datetime.fromisoformat(row[3]).date() if row[3] else None,
            created_at=datetime.fromisoformat(row[4]),
            updated_at=datetime.fromisoformat(row[5]) if row[5] else None,
        )

    def find_by_id(self, id: int) -> Union[Task, None]:
        with sqlite3.connect(self.db) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
            row = cursor.fetchone()

            if not row:
                return None

            return self.__hydrate(row)

    def find_by_status(self, status: List[Status] | None = None) -> List[Task]:
        if status is None:
            status = [Status.TODO, Status.IN_PROGRESS, Status.DONE]

        with sqlite3.connect(self.db) as connection:
            cursor = connection.cursor()
            placeholders = ", ".join("?" for _ in status)
            query = f"SELECT * FROM tasks WHERE status IN ({placeholders})"
            cursor.execute(query, [s.value for s in status])
            rows = cursor.fetchall()
            return [self.__hydrate(row) for row in rows]

    def add(self, task: CreateTask):
        with sqlite3.connect(self.db) as connection:
            cursor = connection.cursor()

            result = cursor.execute(
                "INSERT INTO tasks (description, status) VALUES (?, ?)",
                (task.description, task.status.value),
            )

            connection.commit()

            task_id = result.lastrowid

            if task_id is None:
                return None

            return self.find_by_id(task_id)

    def update(self, task: Task, data: UpdateTask):
        with sqlite3.connect(self.db) as connection:
            field_keys = []
            field_values = []
            cursor = connection.cursor()

            for field, value in data.items():
                if data.is_set(field):
                    field_keys.append(f"{field} = ?")

                    if type(value) is Status:
                        field_values.append(value.value)
                    elif type(value) is date:
                        field_values.append(value.isoformat())
                    else:
                        field_values.append(value)

            query = f"UPDATE tasks SET {', '.join(field_keys)} WHERE id = ?"
            result = cursor.execute(query, (*field_values, task.id))
            connection.commit()

            return result.rowcount > 0

    def delete_by_id(self, id: int) -> bool:
        with sqlite3.connect(self.db) as connection:
            cursor = connection.cursor()
            result = cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
            connection.commit()
            return result.rowcount > 0

    def size(self) -> int:
        with sqlite3.connect(self.db) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM tasks")
            count = cursor.fetchone()[0]
            return count
