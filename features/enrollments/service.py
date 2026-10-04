class EnrollmentService:

    def __init__(self, database):
        self.database = database

    def next_student_id(self):
        connection = self.database.connect()
        try:
            row = connection.execute(
                """
                SELECT student_id
                FROM students
                WHERE student_id LIKE 'STU-%'
                ORDER BY CAST(SUBSTR(student_id, 5) AS INTEGER) DESC
                LIMIT 1
                """
            ).fetchone()
            if not row:
                return "STU-0001"
            try:
                number = int(row["student_id"][4:]) + 1
            except (ValueError, TypeError):
                number = 1
            return f"STU-{number:04d}"
        finally:
            connection.close()

    def get_subjects(self, grade, track, strand, semester):
        connection = self.database.connect()
        try:
            rows = connection.execute(
                """
                SELECT subject_name
                FROM subjects
                WHERE grade_level = ?
                AND track = ?
                AND strand = ?
                AND semester = ?
                ORDER BY id
                """,
                (grade, track, strand, semester)
            ).fetchall()
            return [row["subject_name"] for row in rows]
        finally:
            connection.close()

    def save_enrollment(self, student, grade, track, strand, semester, subjects):
        if not subjects:
            raise ValueError("Please select at least one subject.")

        connection = self.database.connect()
        try:
            existing = connection.execute(
                "SELECT id FROM students WHERE student_id = ?",
                (student["student_id"],)
            ).fetchone()
            if existing:
                raise ValueError("Student ID already exists.")

            connection.execute(
                """
                INSERT INTO students
                (student_id, first_name, middle_name, last_name, age, gender, contact, address, guardian)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    student["student_id"],
                    student["first_name"],
                    student["middle_name"],
                    student["last_name"],
                    student["age"],
                    student["gender"],
                    student["contact"],
                    student["address"],
                    student["guardian"]
                )
            )

            cursor = connection.execute(
                """
                INSERT INTO enrollments
                (student_id, grade_level, track, strand, semester)
                VALUES (?, ?, ?, ?, ?)
                """,
                (student["student_id"], grade, track, strand, semester)
            )

            enrollment_id = cursor.lastrowid

            connection.executemany(
                """
                INSERT INTO enrollment_subjects (enrollment_id, subject_name)
                VALUES (?, ?)
                """,
                [(enrollment_id, subject) for subject in subjects]
            )

            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def update_enrollment(self, enrollment_id, student, grade, track, strand, semester, subjects):
        if not subjects:
            raise ValueError("Please select at least one subject.")

        connection = self.database.connect()
        try:
            enrollment = connection.execute(
                "SELECT student_id FROM enrollments WHERE id = ?",
                (enrollment_id,)
            ).fetchone()
            if not enrollment:
                raise ValueError("Enrollment record not found.")

            student_id = enrollment["student_id"]

            connection.execute(
                """
                UPDATE students
                SET first_name = ?, middle_name = ?, last_name = ?, age = ?,
                    gender = ?, contact = ?, address = ?, guardian = ?
                WHERE student_id = ?
                """,
                (
                    student["first_name"],
                    student["middle_name"],
                    student["last_name"],
                    student["age"],
                    student["gender"],
                    student["contact"],
                    student["address"],
                    student["guardian"],
                    student_id
                )
            )

            connection.execute(
                """
                UPDATE enrollments
                SET grade_level = ?, track = ?, strand = ?, semester = ?
                WHERE id = ?
                """,
                (grade, track, strand, semester, enrollment_id)
            )

            connection.execute(
                "DELETE FROM enrollment_subjects WHERE enrollment_id = ?",
                (enrollment_id,)
            )

            connection.executemany(
                """
                INSERT INTO enrollment_subjects (enrollment_id, subject_name)
                VALUES (?, ?)
                """,
                [(enrollment_id, subject) for subject in subjects]
            )

            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def delete_enrollment(self, enrollment_id):
        connection = self.database.connect()
        try:
            enrollment = connection.execute(
                "SELECT student_id FROM enrollments WHERE id = ?",
                (enrollment_id,)
            ).fetchone()
            if not enrollment:
                raise ValueError("Enrollment record not found.")

            student_id = enrollment["student_id"]
            connection.execute(
                "DELETE FROM enrollment_subjects WHERE enrollment_id = ?",
                (enrollment_id,)
            )
            connection.execute(
                "DELETE FROM enrollments WHERE id = ?",
                (enrollment_id,)
            )
            connection.execute(
                "DELETE FROM students WHERE student_id = ?",
                (student_id,)
            )
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def get_enrollments(self):
        connection = self.database.connect()
        try:
            rows = connection.execute(
                """
                SELECT e.id, s.student_id, s.first_name, s.middle_name, s.last_name,
                       s.age, s.gender, s.contact, s.address, s.guardian,
                       e.grade_level, e.track, e.strand, e.semester
                FROM enrollments e
                JOIN students s ON s.student_id = e.student_id
                ORDER BY e.id DESC
                """
            ).fetchall()

            result = []
            for row in rows:
                item = dict(row)
                subject_rows = connection.execute(
                    """
                    SELECT subject_name
                    FROM enrollment_subjects
                    WHERE enrollment_id = ?
                    ORDER BY id
                    """,
                    (row["id"],)
                ).fetchall()
                item["subjects"] = [subject["subject_name"] for subject in subject_rows]
                result.append(item)
            return result
        finally:
            connection.close()
