
import sqlite3
from pathlib import Path


class Database:

    def __init__(self, database_path="school.db"):
        self.database_path = Path(database_path)

    def connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def create_tables(self):
        with self.connect() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            """)

            connection.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT UNIQUE NOT NULL,
                    first_name TEXT NOT NULL,
                    middle_name TEXT,
                    last_name TEXT NOT NULL,
                    age INTEGER,
                    gender TEXT,
                    contact TEXT,
                    address TEXT,
                    guardian TEXT
                )
            """)

            connection.execute("""
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
                )
            """)

            connection.execute("""
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
                )
            """)

            connection.execute("""
                CREATE TABLE IF NOT EXISTS enrollment_subjects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    enrollment_id INTEGER NOT NULL,
                    subject_name TEXT NOT NULL,
                    FOREIGN KEY (enrollment_id)
                        REFERENCES enrollments(id)
                        ON DELETE CASCADE
                )
            """)

            connection.execute("""
                INSERT OR IGNORE INTO users (username, password)
                VALUES (?, ?)
            """, ("admin", "admin123"))

        self.seed_subjects()

    def seed_subjects(self):
        subject_lists = {
            # ACADEMIC TRACK - STEM
            "STEM": {
                "Grade 11": {
                    "1st Semester": [
                        "General Mathematics",
                        "Oral Communication",
                        "Earth Science",
                        "Introduction to Calculus",
                    ],
                    "2nd Semester": [
                        "Statistics and Probability",
                        "Reading and Writing",
                        "General Biology",
                        "Pre-Calculus",
                    ],
                },
                "Grade 12": {
                    "1st Semester": [
                        "General Physics",
                        "General Chemistry",
                        "Research Project",
                        "Basic Calculus",
                    ],
                    "2nd Semester": [
                        "Work Immersion",
                        "Research Presentation",
                        "Practical Research",
                        "Applied Science",
                    ],
                },
            },

            # ACADEMIC TRACK - ABM
            "ABM": {
                "Grade 11": {
                    "1st Semester": [
                        "Business Mathematics",
                        "Organization and Management",
                        "Fundamentals of Accountancy",
                        "Oral Communication",
                    ],
                    "2nd Semester": [
                        "Principles of Marketing",
                        "Business Finance",
                        "Applied Economics",
                        "Reading and Writing",
                    ],
                },
                "Grade 12": {
                    "1st Semester": [
                        "Fundamentals of Accountancy 2",
                        "Business Ethics",
                        "Business Enterprise Simulation",
                        "Research Project",
                    ],
                    "2nd Semester": [
                        "Work Immersion",
                        "Business Plan Development",
                        "Applied Economics Project",
                        "Business Presentation",
                    ],
                },
            },

            # ACADEMIC TRACK - HUMSS
            "HUMSS": {
                "Grade 11": {
                    "1st Semester": [
                        "Introduction to World Religions",
                        "Creative Writing",
                        "Oral Communication",
                        "Disciplines and Ideas in Social Sciences",
                    ],
                    "2nd Semester": [
                        "Philippine Politics and Governance",
                        "Creative Nonfiction",
                        "Community Engagement",
                        "Reading and Writing",
                    ],
                },
                "Grade 12": {
                    "1st Semester": [
                        "Trends, Networks, and Critical Thinking",
                        "Disciplines and Ideas in Applied Social Sciences",
                        "Research Project",
                        "Social Science Research",
                    ],
                    "2nd Semester": [
                        "Work Immersion",
                        "Community Research",
                        "Communication Skills",
                        "Research Presentation",
                    ],
                },
            },

            # ACADEMIC TRACK - GAS
            "GAS": {
                "Grade 11": {
                    "1st Semester": [
                        "General Mathematics",
                        "Oral Communication",
                        "Understanding Culture and Society",
                        "Earth Science",
                    ],
                    "2nd Semester": [
                        "Statistics and Probability",
                        "Reading and Writing",
                        "Applied Economics",
                        "Creative Writing",
                    ],
                },
                "Grade 12": {
                    "1st Semester": [
                        "Research Project",
                        "Contemporary Philippine Arts",
                        "Social Science Studies",
                        "Practical Research",
                    ],
                    "2nd Semester": [
                        "Work Immersion",
                        "Research Presentation",
                        "Community Engagement",
                        "Applied Learning Project",
                    ],
                },
            },

            # TVL - ICT PROGRAMMING
            "ICT - Programming": {
                "Grade 11": {
                    "1st Semester": [
                        "Computer Programming Fundamentals",
                        "Computer Systems Servicing Basics",
                        "Introduction to Algorithms",
                        "Workplace Communication",
                    ],
                    "2nd Semester": [
                        "Object-Oriented Programming",
                        "Database Fundamentals",
                        "Web Development Basics",
                        "Programming Logic",
                    ],
                },
                "Grade 12": {
                    "1st Semester": [
                        "Advanced Programming",
                        "Database Application Development",
                        "Web Application Development",
                        "Software Testing",
                    ],
                    "2nd Semester": [
                        "Application Development Project",
                        "Programming Portfolio",
                        "Technical Documentation",
                        "Work Immersion",
                    ],
                },
            },

            # TVL - ICT CSS
            "ICT - CSS": {
                "Grade 11": {
                    "1st Semester": [
                        "Computer Hardware Basics",
                        "Computer Systems Servicing Fundamentals",
                        "Occupational Health and Safety",
                        "Workplace Communication",
                    ],
                    "2nd Semester": [
                        "Install and Configure Computer Systems",
                        "Set Up Computer Networks",
                        "Configure Computer Systems",
                        "Troubleshooting Fundamentals",
                    ],
                },
                "Grade 12": {
                    "1st Semester": [
                        "Maintain and Repair Computer Systems",
                        "Network Configuration",
                        "Computer System Diagnostics",
                        "Technical Support",
                    ],
                    "2nd Semester": [
                        "Computer Maintenance Project",
                        "Network Troubleshooting",
                        "Technical Documentation",
                        "Work Immersion",
                    ],
                },
            },

            # TVL - HOME ECONOMICS
            "Home Economics (HE)": {
                "Grade 11": {
                    "1st Semester": [
                        "Personal Entrepreneurial Competencies",
                        "Environment and Market",
                        "Use of Kitchen Tools, Equipment, and Paraphernalia",
                        "Bread and Pastry Production",
                    ],
                    "2nd Semester": [
                        "Occupational Health and Safety Procedures",
                        "Prepare and Present Bakery Products",
                        "Food and Beverage Services",
                        "Workplace Communication",
                    ],
                },
                "Grade 12": {
                    "1st Semester": [
                        "Cookery",
                        "Prepare Appetizers, Salads, and Sandwiches",
                        "Prepare and Cook Meat, Poultry, and Seafood",
                        "Food Processing Basics",
                    ],
                    "2nd Semester": [
                        "Housekeeping Fundamentals",
                        "Customer Service",
                        "Front Office Services",
                        "Work Immersion",
                    ],
                },
            },

            # TVL - SHIELDED METAL ARC WELDING
            "Shielded Metal Arc Welding (SMAW)": {
                "Grade 11": {
                    "1st Semester": [
                        "Personal Entrepreneurial Competencies",
                        "Environment and Market",
                        "Prepare Weld Materials",
                        "Set Up Welding Equipment",
                    ],
                    "2nd Semester": [
                        "Lay Out Beads on Carbon Steel Plates",
                        "Fit Up Weld Materials",
                        "Repair Welds",
                        "Welding Safety Procedures",
                    ],
                },
                "Grade 12": {
                    "1st Semester": [
                        "Perform Fillet Weld on Carbon Steel Plates",
                        "Perform Groove Weld on Carbon Steel Plates",
                        "Welding Drawing Interpretation",
                        "Welding Quality Control",
                    ],
                    "2nd Semester": [
                        "Welding Quality Inspection",
                        "Welding Equipment Maintenance",
                        "Workplace Safety and Health",
                        "Work Immersion",
                    ],
                },
            },

            # TVL - AGRI-FISHERY ARTS
            "Agri-Fishery Arts (AFA)": {
                "Grade 11": {
                    "1st Semester": [
                        "Personal Entrepreneurial Competencies",
                        "Environment and Market",
                        "Apply Safety Measures in Farm Operations",
                        "Use Farm Tools and Equipment",
                        "Perform Estimation and Basic Calculation",
                    ],
                    "2nd Semester": [
                        "Prepare Land for Crop Production",
                        "Plant and Maintain Horticultural Crops",
                        "Control Weeds and Manage Pests",
                        "Apply Plant Nutrition",
                    ],
                },
                "Grade 12": {
                    "1st Semester": [
                        "Coordinate Crop Maintenance",
                        "Harvest Horticultural Crops",
                        "Implement a Post-Harvest Program",
                        "Maintain Farm Records",
                    ],
                    "2nd Semester": [
                        "Agricultural Product Handling",
                        "Farm Business Management",
                        "Basic Irrigation Management",
                        "Work Immersion",
                    ],
                },
            },

            # ARTS AND DESIGN - VISUAL ARTS
            "Visual Arts": {
                "Grade 11": {
                    "1st Semester": [
                        "Introduction to Visual Arts",
                        "Drawing Fundamentals",
                        "Color Theory",
                        "Art Appreciation",
                    ],
                    "2nd Semester": [
                        "Painting Fundamentals",
                        "Design Principles",
                        "Art History",
                        "Visual Composition",
                    ],
                },
                "Grade 12": {
                    "1st Semester": [
                        "Advanced Drawing",
                        "Digital Art Fundamentals",
                        "Portfolio Development",
                        "Creative Research",
                    ],
                    "2nd Semester": [
                        "Visual Arts Portfolio",
                        "Exhibition Planning",
                        "Art Criticism",
                        "Work Immersion",
                    ],
                },
            },

            # ARTS AND DESIGN - MUSIC
            "Music": {
                "Grade 11": {
                    "1st Semester": [
                        "Music Theory",
                        "Basic Music Reading",
                        "Introduction to Instruments",
                        "Music Appreciation",
                    ],
                    "2nd Semester": [
                        "Rhythm and Harmony",
                        "Vocal Techniques",
                        "Instrumental Practice",
                        "Music History",
                    ],
                },
                "Grade 12": {
                    "1st Semester": [
                        "Advanced Music Theory",
                        "Ensemble Performance",
                        "Music Arrangement",
                        "Performance Preparation",
                    ],
                    "2nd Semester": [
                        "Music Portfolio",
                        "Performance Project",
                        "Music Production Basics",
                        "Work Immersion",
                    ],
                },
            },

            # ARTS AND DESIGN - DANCE
            "Dance": {
                "Grade 11": {
                    "1st Semester": [
                        "Introduction to Dance",
                        "Dance Fundamentals",
                        "Body Movement and Coordination",
                        "Dance Appreciation",
                    ],
                    "2nd Semester": [
                        "Dance Techniques",
                        "Choreography Basics",
                        "Cultural Dance",
                        "Performance Practice",
                    ],
                },
                "Grade 12": {
                    "1st Semester": [
                        "Advanced Dance Techniques",
                        "Dance Production",
                        "Choreography Development",
                        "Performance Preparation",
                    ],
                    "2nd Semester": [
                        "Dance Portfolio",
                        "Stage Performance",
                        "Dance Production Project",
                        "Work Immersion",
                    ],
                },
            },

            # ARTS AND DESIGN - THEATER
            "Theater": {
                "Grade 11": {
                    "1st Semester": [
                        "Introduction to Theater",
                        "Acting Fundamentals",
                        "Voice and Movement",
                        "Theater Appreciation",
                    ],
                    "2nd Semester": [
                        "Stagecraft Basics",
                        "Script Analysis",
                        "Character Development",
                        "Performance Practice",
                    ],
                },
                "Grade 12": {
                    "1st Semester": [
                        "Advanced Acting",
                        "Theater Production",
                        "Stage Management",
                        "Production Planning",
                    ],
                    "2nd Semester": [
                        "Theater Portfolio",
                        "Stage Performance",
                        "Production Project",
                        "Work Immersion",
                    ],
                },
            },

            # ARTS AND DESIGN - MEDIA ARTS
            "Media Arts": {
                "Grade 11": {
                    "1st Semester": [
                        "Introduction to Media Arts",
                        "Digital Design Fundamentals",
                        "Photography Basics",
                        "Visual Communication",
                    ],
                    "2nd Semester": [
                        "Video Production Basics",
                        "Digital Editing",
                        "Graphic Design",
                        "Media Appreciation",
                    ],
                },
                "Grade 12": {
                    "1st Semester": [
                        "Advanced Digital Design",
                        "Video Production",
                        "Multimedia Storytelling",
                        "Creative Research",
                    ],
                    "2nd Semester": [
                        "Media Arts Portfolio",
                        "Multimedia Project",
                        "Digital Presentation",
                        "Work Immersion",
                    ],
                },
            },

            # ARTS AND DESIGN - LITERARY ARTS
            "Literary Arts": {
                "Grade 11": {
                    "1st Semester": [
                        "Introduction to Literature",
                        "Creative Writing",
                        "Reading and Writing",
                        "Literary Appreciation",
                    ],
                    "2nd Semester": [
                        "Poetry Writing",
                        "Fiction Writing",
                        "Essay Writing",
                        "Literary Analysis",
                    ],
                },
                "Grade 12": {
                    "1st Semester": [
                        "Advanced Creative Writing",
                        "Literary Criticism",
                        "Editing and Revision",
                        "Research Writing",
                    ],
                    "2nd Semester": [
                        "Literary Portfolio",
                        "Publication Project",
                        "Writing Workshop",
                        "Work Immersion",
                    ],
                },
            },

            # SPORTS - COACHING
            "Sports Coaching": {
                "Grade 11": {
                    "1st Semester": [
                        "Introduction to Sports Coaching",
                        "Sports Rules and Regulations",
                        "Physical Fitness Fundamentals",
                        "Sports Safety",
                    ],
                    "2nd Semester": [
                        "Coaching Techniques",
                        "Training Principles",
                        "Sports Psychology Basics",
                        "Team Management",
                    ],
                },
                "Grade 12": {
                    "1st Semester": [
                        "Advanced Coaching Techniques",
                        "Sports Program Planning",
                        "Performance Evaluation",
                        "Athlete Development",
                    ],
                    "2nd Semester": [
                        "Coaching Portfolio",
                        "Sports Event Management",
                        "Practical Coaching",
                        "Work Immersion",
                    ],
                },
            },

            # SPORTS - OFFICIATING
            "Sports Officiating": {
                "Grade 11": {
                    "1st Semester": [
                        "Introduction to Sports Officiating",
                        "Sports Rules and Regulations",
                        "Sports Safety",
                        "Physical Fitness Fundamentals",
                    ],
                    "2nd Semester": [
                        "Officiating Techniques",
                        "Game Management",
                        "Sports Ethics",
                        "Decision-Making in Sports",
                    ],
                },
                "Grade 12": {
                    "1st Semester": [
                        "Advanced Sports Officiating",
                        "Competition Management",
                        "Rules Interpretation",
                        "Performance Evaluation",
                    ],
                    "2nd Semester": [
                        "Officiating Portfolio",
                        "Sports Event Management",
                        "Practical Officiating",
                        "Work Immersion",
                    ],
                },
            },
        }

        academic_strands = ["STEM", "ABM", "HUMSS", "GAS"]

        tvl_strands = [
            "ICT - Programming",
            "ICT - CSS",
            "Home Economics (HE)",
            "Shielded Metal Arc Welding (SMAW)",
            "Agri-Fishery Arts (AFA)",
        ]

        arts_strands = [
            "Visual Arts",
            "Music",
            "Dance",
            "Theater",
            "Media Arts",
            "Literary Arts",
        ]

        subjects = []

        for strand, grade_levels in subject_lists.items():

            if strand in academic_strands:
                track = "Academic"
            elif strand in tvl_strands:
                track = "TVL"
            elif strand in arts_strands:
                track = "Arts and Design"
            else:
                track = "Sports"

            for grade_level, semesters in grade_levels.items():
                for semester, subject_names in semesters.items():
                    for subject_name in subject_names:
                        subjects.append((
                            grade_level,
                            track,
                            strand,
                            semester,
                            subject_name,
                        ))

        with self.connect() as connection:
            connection.executemany("""
                INSERT OR IGNORE INTO subjects (
                    grade_level,
                    track,
                    strand,
                    semester,
                    subject_name
                )
                VALUES (?, ?, ?, ?, ?)
            """, subjects)

    def get_subjects(self, grade_level, track, strand, semester):
        with self.connect() as connection:
            rows = connection.execute("""
                SELECT subject_name
                FROM subjects
                WHERE grade_level = ?
                  AND track = ?
                  AND strand = ?
                  AND semester = ?
                ORDER BY id
            """, (
                grade_level,
                track,
                strand,
                semester
            )).fetchall()

        return [row["subject_name"] for row in rows]
