import sqlite3
from pathlib import Path


class Database:

    def __init__(self, database_path):
        self.database_path = Path(database_path)

    def connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def create_tables(self):
        connection = self.connect()
        try:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT UNIQUE NOT NULL,
                    first_name TEXT NOT NULL,
                    middle_name TEXT,
                    last_name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    gender TEXT NOT NULL,
                    contact TEXT NOT NULL,
                    address TEXT NOT NULL,
                    guardian TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS subjects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    grade_level TEXT NOT NULL,
                    track TEXT NOT NULL,
                    strand TEXT NOT NULL,
                    semester TEXT NOT NULL,
                    subject_name TEXT NOT NULL,
                    UNIQUE (
                        grade_level,
                        track,
                        strand,
                        semester,
                        subject_name
                    )
                );

                CREATE TABLE IF NOT EXISTS enrollments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    grade_level TEXT NOT NULL,
                    track TEXT NOT NULL,
                    strand TEXT NOT NULL,
                    semester TEXT NOT NULL,
                    FOREIGN KEY (student_id)
                        REFERENCES students(student_id)
                        ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS enrollment_subjects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    enrollment_id INTEGER NOT NULL,
                    subject_name TEXT NOT NULL,
                    FOREIGN KEY (enrollment_id)
                        REFERENCES enrollments(id)
                        ON DELETE CASCADE
                );
                """
            )
            self.seed_users(connection)
            self.seed_subjects(connection)
            connection.commit()
        finally:
            connection.close()

    def seed_users(self, connection):
        connection.execute(
            """
            INSERT OR IGNORE INTO users (username, password)
            VALUES (?, ?)
            """,
            ("admin", "admin123")
        )

    def seed_subjects(self, connection):
        subjects = [
            ("Grade 11", "Academic", "STEM", "1st Semester", "Pre-Calculus"),
            ("Grade 11", "Academic", "STEM", "1st Semester", "General Biology 1"),
            ("Grade 11", "Academic", "STEM", "1st Semester", "General Chemistry 1"),
            ("Grade 11", "Academic", "STEM", "1st Semester", "Oral Communication"),
            ("Grade 11", "Academic", "STEM", "2nd Semester", "Basic Calculus"),
            ("Grade 11", "Academic", "STEM", "2nd Semester", "General Biology 2"),
            ("Grade 11", "Academic", "STEM", "2nd Semester", "General Chemistry 2"),
            ("Grade 11", "Academic", "STEM", "2nd Semester", "Reading and Writing"),
            ("Grade 11", "Academic", "ABM", "1st Semester", "Business Mathematics"),
            ("Grade 11", "Academic", "ABM", "1st Semester", "Applied Economics"),
            ("Grade 11", "Academic", "ABM", "1st Semester", "Organization and Management"),
            ("Grade 11", "Academic", "ABM", "2nd Semester", "Fundamentals of Accountancy"),
            ("Grade 11", "Academic", "ABM", "2nd Semester", "Business Management 1"),
            ("Grade 11", "Academic", "ABM", "2nd Semester", "Principles of Marketing"),
            ("Grade 11", "Academic", "ABM", "2nd Semester", "Business Ethics"),
            ("Grade 11", "Academic", "HUMSS", "1st Semester", "Creative Writing"),
            ("Grade 11", "Academic", "HUMSS", "1st Semester", "Introduction to World Religions"),
            ("Grade 11", "Academic", "HUMSS", "1st Semester", "Disciplines and Ideas in the Social Sciences"),
            ("Grade 11", "Academic", "HUMSS", "2nd Semester", "Creative Nonfiction"),
            ("Grade 11", "Academic", "HUMSS", "2nd Semester", "Disciplines and Ideas in the Applied Social Sciences"),
            ("Grade 11", "Academic", "HUMSS", "2nd Semester", "Philippine Politics and Governance"),
            ("Grade 11", "Academic", "GAS", "1st Semester", "Humanities 1"),
            ("Grade 11", "Academic", "GAS", "1st Semester", "Social Science 1"),
            ("Grade 11", "Academic", "GAS", "1st Semester", "Applied Economics"),
            ("Grade 11", "Academic", "GAS", "2nd Semester", "Humanities 2"),
            ("Grade 11", "Academic", "GAS", "2nd Semester", "Social Science 2"),
            ("Grade 11", "Academic", "GAS", "2nd Semester", "Research Project"),
            ("Grade 12", "Academic", "STEM", "1st Semester", "General Physics 1"),
            ("Grade 12", "Academic", "STEM", "1st Semester", "General Chemistry 2"),
            ("Grade 12", "Academic", "STEM", "1st Semester", "Research in Daily Life 1"),
            ("Grade 12", "Academic", "STEM", "2nd Semester", "General Physics 2"),
            ("Grade 12", "Academic", "STEM", "2nd Semester", "Basic Calculus"),
            ("Grade 12", "Academic", "STEM", "2nd Semester", "Research in Daily Life 2"),
            ("Grade 12", "Academic", "ABM", "1st Semester", "Business Finance"),
            ("Grade 12", "Academic", "ABM", "1st Semester", "Business Research 1"),
            ("Grade 12", "Academic", "ABM", "1st Semester", "Fundamentals of Accountancy"),
            ("Grade 12", "Academic", "ABM", "2nd Semester", "Work Immersion"),
            ("Grade 12", "Academic", "ABM", "2nd Semester", "Business Research 2"),
            ("Grade 12", "Academic", "ABM", "2nd Semester", "Entrepreneurship"),
            ("Grade 12", "Academic", "HUMSS", "1st Semester", "Trends, Networks, and Critical Thinking"),
            ("Grade 12", "Academic", "HUMSS", "1st Semester", "Community Engagement"),
            ("Grade 12", "Academic", "HUMSS", "1st Semester", "Creative Writing"),
            ("Grade 12", "Academic", "HUMSS", "2nd Semester", "Work Immersion"),
            ("Grade 12", "Academic", "HUMSS", "2nd Semester", "Culminating Activity"),
            ("Grade 12", "Academic", "HUMSS", "2nd Semester", "Research Project"),
            ("Grade 12", "Academic", "GAS", "1st Semester", "Applied Economics"),
            ("Grade 12", "Academic", "GAS", "1st Semester", "Research in Daily Life 1"),
            ("Grade 12", "Academic", "GAS", "1st Semester", "Elective 1"),
            ("Grade 12", "Academic", "GAS", "2nd Semester", "Research in Daily Life 2"),
            ("Grade 12", "Academic", "GAS", "2nd Semester", "Work Immersion"),
            ("Grade 12", "Academic", "GAS", "2nd Semester", "Elective 2"),
            ("Grade 11", "TVL", "ICT - Programming", "1st Semester", "Computer Programming"),
            ("Grade 11", "TVL", "ICT - Programming", "1st Semester", "Introduction to ICT"),
            ("Grade 11", "TVL", "ICT - Programming", "2nd Semester", "Web Development"),
            ("Grade 11", "TVL", "ICT - Programming", "2nd Semester", "Programming Fundamentals"),
            ("Grade 11", "TVL", "ICT - CSS", "1st Semester", "Computer Systems Servicing 1"),
            ("Grade 11", "TVL", "ICT - CSS", "1st Semester", "Installation and Configuration"),
            ("Grade 11", "TVL", "ICT - CSS", "2nd Semester", "Computer Systems Servicing 2"),
            ("Grade 11", "TVL", "ICT - CSS", "2nd Semester", "Networking Fundamentals"),
            ("Grade 12", "TVL", "ICT - Programming", "1st Semester", "Programming Java"),
            ("Grade 12", "TVL", "ICT - Programming", "1st Semester", "Database Management"),
            ("Grade 12", "TVL", "ICT - Programming", "2nd Semester", "Programming .NET Technology"),
            ("Grade 12", "TVL", "ICT - Programming", "2nd Semester", "Work Immersion"),
            ("Grade 12", "TVL", "ICT - CSS", "1st Semester", "Computer Systems Servicing 3"),
            ("Grade 12", "TVL", "ICT - CSS", "1st Semester", "Server Administration"),
            ("Grade 12", "TVL", "ICT - CSS", "2nd Semester", "Computer Systems Servicing 4"),
            ("Grade 12", "TVL", "ICT - CSS", "2nd Semester", "Work Immersion")
        ]
        connection.executemany(
            """
            INSERT OR IGNORE INTO subjects
            (grade_level, track, strand, semester, subject_name)
            VALUES (?, ?, ?, ?, ?)
            """,
            subjects
        )
