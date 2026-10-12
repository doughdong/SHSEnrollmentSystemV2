# Senior High School Enrollment System

## Project Description

The **Senior High School Enrollment System** is a desktop application developed using Python, PyQt6, and SQLite to help organize the enrollment process for Senior High School students. It provides a graphical interface where student information, academic classification, and selected subjects can be recorded and managed in one place. The system supports Grade 11 and Grade 12 across four tracks: Academic, Technical-Vocational-Livelihood (TVL), Arts and Design, and Sports. Each track provides its corresponding strands or specializations and predefined subjects for the selected grade level and semester. It also allows enrollment records to be searched, viewed, edited, and deleted, helping make record management more organized and convenient than relying on manual records.

## Project Objectives

The main objective of this project is to **develop a desktop-based Senior High School Enrollment System that efficiently records, stores, and manages students' enrollment information and selected subjects in an organized database**.

## Features

### Student Enrollment
Records the student's personal information, including student ID, name, age, gender, contact number, address, and guardian, together with the student's academic enrollment details.

### Automatic Student ID Generation
Generates a unique student ID in the `STU-0001` format for new student records.

### Search and Enrollment Filters
Allows users to search by student ID or student name and filter enrollment records by track and strand. The strand filter updates according to the selected track, and a clear option resets the search and filters.

### Grade Level, Track, and Strand Selection
Supports Grade 11 and Grade 12 with four tracks and their corresponding strands or specializations:

| Track | Strands / Specializations |
|---|---|
| **Academic** | STEM, ABM, HUMSS, GAS |
| **Technical-Vocational-Livelihood (TVL)** | ICT - Programming, ICT - CSS, Home Economics (HE), Shielded Metal Arc Welding (SMAW), Agri-Fishery Arts (AFA) |
| **Arts and Design** | Visual Arts, Music, Dance, Theater, Media Arts, Literary Arts |
| **Sports** | Sports Coaching, Sports Officiating |

### Subject Selection
Displays the predefined subjects that match the selected grade level, track, strand or specialization, and semester. The subject lists are initialized in `database/database.py`, and the application retrieves the matching list when a student is enrolled or an existing enrollment is edited.

### Enrollment Summary
Shows a summary of the student's information, enrollment details, and selected subjects for review before saving.

### Enrollment Record Management
Allows users to search enrollment records by student ID or student name, view student details, edit existing records, and delete records after confirmation.

## Authentication Module

The application includes a separate authentication module for access control.

- **User Login:** Allows registered users to sign in with a username and password.
- **Account Registration:** Allows new users to create an account, with validation for required fields, minimum username and password lengths, and duplicate usernames.
- **Logout:** Ends the current session and returns the user to the login screen.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language used to develop the application's logic and functionality. |
| PyQt6 | Provides the desktop graphical user interface (GUI), including windows, forms, dialogs, and controls. |
| SQLite | Stores user accounts, student information, available subjects, enrollment records, and selected subjects in a local database. |
| Qt Style Sheets (QSS) | Defines the application's visual appearance and interface styling. |
| Git | Tracks changes to the source code through version control. |
| GitHub | Hosts the project repository and source code. |
| PyCharm | Integrated development environment used for developing and running the project. |

## Project Structure

```text
SHSEnrollmentSystemV2/
├── database/
│   ├── __init__.py
│   └── database.py
├── features/
│   ├── __init__.py
│   ├── authentication/
│   │   ├── __init__.py
│   │   ├── service.py
│   │   └── view.py
│   └── enrollments/
│       ├── __init__.py
│       ├── service.py
│       └── views/
│           ├── __init__.py
│           ├── enrollment_view.py
│           ├── student_dialog.py
│           ├── student_view.py
│           ├── subject_dialog.py
│           └── summary_dialog.py
├── README_screenshots/
│   ├── 01-login.png
│   ├── 02-create-account.png
│   ├── 03-enrolled-students-empty.png
│   ├── 04-student-information.png
│   ├── 05-subject-selection.png
│   ├── 06-enrollment-summary.png
│   └── 07-enrolled-students-record.png
├── main.py
├── school.db              # Created automatically when the application runs
├── style.qss
└── README.md
```

### Major Files and Folders

| File/Folder | Description |
|---|---|
| `main.py` | Starts the application and coordinates the authentication and main-window flow. |
| `database/` | Contains the database connection and initialization code. |
| `database/database.py` | Creates the SQLite tables and inserts the initial user and subject data. |
| `features/authentication/` | Contains the login and account-registration service and interface. |
| `features/authentication/service.py` | Handles login validation and account registration operations. |
| `features/authentication/view.py` | Provides the login interface and account-registration dialog. |
| `features/enrollments/service.py` | Handles student enrollment database operations, subject retrieval, and record management. |
| `features/enrollments/views/` | Contains the graphical interfaces used in the enrollment process. |
| `enrollment_view.py` | Displays the enrollment records and provides record-management actions. |
| `student_dialog.py` | Collects student information and academic enrollment details. |
| `subject_dialog.py` | Displays and handles subject selection. |
| `summary_dialog.py` | Displays the enrollment summary before saving. |
| `student_view.py` | Displays the details of a saved student enrollment. |
| `style.qss` | Contains the application's Qt Style Sheet rules. |
| `README_screenshots/` | Contains screenshots used to document the application interface and workflow. |

## Installation and Setup

### Requirements

- Python 3
- PyQt6
- SQLite (included with standard Python distributions)
- Git (optional, if cloning the repository)
- PyCharm or another Python-compatible IDE (optional)

### Step 1: Clone the Repository

```bash
git clone https://github.com/doughdong/SHSEnrollmentSystemV2.git
cd SHSEnrollmentSystemV2
```

If you have already downloaded the project, open a terminal in the project folder and continue to Step 2.

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 3: Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If activation is restricted by your system's execution policy, you can run the application using the virtual environment's Python executable directly.

### Step 4: Install PyQt6

```bash
python -m pip install PyQt6
```

### Step 5: Run the Application

```bash
python main.py
```

The application initializes the SQLite database and creates the required tables and initial subject data when it starts. The `school.db` file is generated in the project root if it does not already exist.

## How to Use the System

1. Run the application using `python main.py`.
2. Sign in using an existing account, or choose the account-registration option to create one.
3. From the main window, choose the option to enroll a student.
4. Enter the student's personal information.
5. Select the student's grade level, track, and strand.
6. Choose the semester and select at least one available subject.
7. Review the information and selected subjects in the enrollment summary.
8. Confirm and save the enrollment.
9. Use the enrollment table to search by student ID or name, filter by track and strand, view student details, edit an enrollment, or delete a record.
10. Use **Logout** to return to the login screen.

### Default Demonstration Account

The database initialization code creates the following default account:

| Username | Password |
|---|---|
| `admin` | `admin123` |

This account is intended for demonstration and testing. Change or remove the default credentials before using the application with real student information.

## Object-Oriented Programming (OOP) Implementation

The application organizes related data and behavior into classes. The following examples show how OOP is used in the project.

### Important Classes

| Class | Purpose |
|---|---|
| `Database` | Manages SQLite connections, table creation, and initial data. |
| `AuthenticationService` | Handles login validation and account registration. |
| `AuthenticationView` | Provides the login interface. |
| `SignupDialog` | Provides the account-registration interface. |
| `EnrollmentService` | Handles enrollment data operations and retrieves available subjects. |
| `EnrollmentView` | Displays and manages enrollment records. |
| `StudentInformationDialog` | Collects student information and enrollment classification. |
| `SubjectSelectionDialog` | Handles the selection of subjects. |
| `EnrollmentSummaryDialog` | Displays the enrollment details for review. |
| `StudentViewDialog` | Displays the details of a saved enrollment. |
| `MainWindow` | Provides the main application window and navigation to enrollment management. |
| `ApplicationController` | Coordinates the login screen, main window, and logout flow. |

### Encapsulation
Related operations are grouped into classes. For example, `AuthenticationService` handles authentication operations, while `EnrollmentService` handles enrollment-related database operations.

### Inheritance
The application uses inheritance through PyQt6 classes. For example, `MainWindow` inherits from `QMainWindow`, while the login interface and dialogs inherit from `QDialog`. The enrollment interface inherits from `QWidget`.

### Polymorphism
The application's custom GUI classes use inherited PyQt6 behavior while providing their own implementations for application-specific interactions and event handling.

## Database

The system uses **SQLite**, a local relational database, to store and manage the application's data. Database connections, table creation, and initial data setup are handled by `database/database.py`. The database is initialized automatically when the application starts.

### Database Tables

| Table | Purpose | Key Information |
|---|---|---|
| `users` | Stores accounts used to access the application. | `id`, `username`, `password` |
| `students` | Stores each student's personal information. | `id`, `student_id`, `first_name`, `middle_name`, `last_name`, `age`, `gender`, `contact`, `address`, `guardian` |
| `subjects` | Stores the available subjects for each academic classification and semester. | `id`, `grade_level`, `track`, `strand`, `semester`, `subject_name` |
| `enrollments` | Stores the academic enrollment details associated with a student. | `id`, `student_id`, `grade_level`, `track`, `strand`, `semester` |
| `enrollment_subjects` | Stores the subjects selected for a specific enrollment record. | `id`, `enrollment_id`, `subject_name` |

### Database Relationships

- A student record is connected to an enrollment through `student_id`.
- An enrollment can contain multiple selected subjects through `enrollment_subjects`.
- The `enrollments` and `enrollment_subjects` tables use foreign keys to maintain their relationships. Cascading deletion is configured for these relationships.
- The database uses uniqueness constraints for usernames, student IDs, and combinations of subject classification fields to help prevent duplicate records.

### Database Operations

| Operation | How It Is Used |
|---|---|
| **Create** | Adds user accounts, student records, enrollment records, and selected-subject records. |
| **Read** | Retrieves account information for login validation, available subjects, enrollment records, and selected subjects. |
| **Update** | Updates student details, enrollment classification, semester, and selected subjects. |
| **Delete** | Removes enrollment records and their associated student and subject records through the application's delete operation. |
| **Search** | Finds enrollment records using a student ID or student name. |
| **Filter** | Filters displayed enrollment records by track and strand/specialization. |

## Screenshots

### 1. Login Screen

The login screen allows a registered user to sign in to the application.

![Login Screen](README_screenshots/01-login.png)

### 2. Create an Account

The account-registration dialog allows a new user to create an account.

![Create Account](README_screenshots/02-create-account.png)

### 3. Enrolled Students

The main enrollment window displays the enrollment table and available record-management actions.

![Enrolled Students](README_screenshots/03-enrolled-students-empty.png)

### 4. Student Information

This form collects personal information and the student's academic enrollment classification.

![Student Information](README_screenshots/04-student-information.png)

### 5. Subject Selection

The subject-selection dialog displays the predefined subjects for the selected grade level, track, strand or specialization, and semester. The database includes subject lists for Academic, TVL, Arts and Design, and Sports strands/specializations.

![Subject Selection](README_screenshots/05-subject-selection.png)

### 6. Enrollment Summary

The summary allows the user to review student information, enrollment details, and selected subjects before saving.

![Enrollment Summary](README_screenshots/06-enrollment-summary.png)

### 7. Enrolled Student Record

The main table displays a saved enrollment record.

![Saved Enrollment](README_screenshots/07-enrolled-students-record.png)

## Testing

The following application flow can be checked during testing:

| Test | Expected Result |
|---|---|
| Launch the application | The database is initialized and the login screen appears. |
| Log in with valid credentials | The main enrollment window opens. |
| Register a new account | A valid, unique account is saved. |
| Start a student enrollment | The student-information form opens. |
| Select academic details | Available subjects match the selected grade level, track, strand, and semester. |
| Review the enrollment | The summary displays the entered information and selected subjects. |
| Save the enrollment | The saved record appears in the enrollment table. |
| Search for a record | Matching records are displayed. |
| Filter by track or strand | The table displays records matching the selected filter. |
| View, edit, or delete a record | The selected record can be viewed or managed through the available actions. |
| Log out | The application returns to the login screen. |

## Known Limitations

1. The application is a local desktop program and uses a local SQLite database.
2. Available tracks, strands/specializations, and subjects are predefined in the database initialization code; there is no separate subject-catalog management interface.
3. The application does not currently provide a separate interface for managing the subject catalog.
4. The current authentication implementation stores passwords as plain text. It is suitable only as a classroom demonstration and should be improved with secure password hashing before real-world use.
5. The application does not currently implement advanced user roles and permissions.

## Author

**Name:** Eljen Armilla  
**Program/Year:** BSCS, 2nd Year
