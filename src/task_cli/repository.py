import sqlite3
from typing import List, Union
from datetime import datetime
from task_cli.model import CreateTask, Status, Task, UpdateTask


class TaskRepository:
    def __init__(self, db: str):
        self.db = db

    def find_by_id(self, id: int) -> Union[Task, None]:
        with sqlite3.connect(self.db) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
            row = cursor.fetchone()

            if not row:
                return None

            return Task(
                id=row[0],
                description=row[1],
                status=Status(row[2]),
                created_at=datetime.fromisoformat(row[3]),
                updated_at=datetime.fromisoformat(row[4]) if row[4] else None,
            )

    def find_by_status(self, status: List[Status] | None = None) -> List[Task]:
        if status is None:
            status = [Status.TODO, Status.IN_PROGRESS, Status.DONE]

        with sqlite3.connect(self.db) as connection:
            cursor = connection.cursor()
            placeholders = ", ".join("?" for _ in status)
            query = f"SELECT * FROM tasks WHERE status IN ({placeholders})"
            cursor.execute(query, [s.value for s in status])
            rows = cursor.fetchall()

            tasks = [
                Task(
                    id=row[0],
                    description=row[1],
                    status=Status(row[2]),
                    created_at=datetime.fromisoformat(row[3]),
                    updated_at=datetime.fromisoformat(row[4]) if row[4] else None,
                )
                for row in rows
            ]

            return tasks

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

            for field, value in data.__dict__.items():
                if value is not None:
                    field_keys.append(f"{field} = ?")

                    if type(value) is Status:
                        field_values.append(value.value)
                    else:
                        field_values.append(value)

            result = cursor.execute(
                f"UPDATE tasks SET {', '.join(field_keys)} WHERE id = ?",
                (*field_values, task.id),
            )

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
