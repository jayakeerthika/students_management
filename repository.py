from contextlib import closing
from database import get_connection


class StudentRepository:

    def add(self, name, email, age, course):
        with closing(get_connection()) as conn:
            cursor = conn.execute(
                "INSERT INTO students (name, email, age, course) VALUES (?, ?, ?, ?)",
                (name, email, age, course),
            )
            conn.commit()
            return cursor.lastrowid

    def get_all(self):
        with closing(get_connection()) as conn:
            rows = conn.execute("SELECT * FROM students").fetchall()
            return [dict(row) for row in rows]

    def get_by_id(self, student_id):
        with closing(get_connection()) as conn:
            row = conn.execute(
                "SELECT * FROM students WHERE id = ?", (student_id,)
            ).fetchone()
            return dict(row) if row else None

    def update(self, student_id, name, email, age, course):
        with closing(get_connection()) as conn:
            cursor = conn.execute(
                "UPDATE students SET name = ?, email = ?, age = ?, course = ? WHERE id = ?",
                (name, email, age, course, student_id),
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete(self, student_id):
        with closing(get_connection()) as conn:
            cursor = conn.execute(
                "DELETE FROM students WHERE id = ?", (student_id,)
            )
            conn.commit()
            return cursor.rowcount > 0