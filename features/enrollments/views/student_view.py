from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QDialogButtonBox,
    QGroupBox,
    QListWidget
)


class StudentViewDialog(QDialog):

    def __init__(self, enrollment, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Student Details")
        self.setMinimumSize(600, 650)
        self.resize(700, 700)

        self.setup_ui(enrollment)

    def setup_ui(self, enrollment):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(15)

        title = QLabel("Student Details")
        title.setObjectName("dialogTitle")
        layout.addWidget(title)

        student_group = QGroupBox("Student Information")

        student_layout = QGridLayout(student_group)
        student_layout.setContentsMargins(20, 15, 20, 15)
        student_layout.setHorizontalSpacing(10)
        student_layout.setVerticalSpacing(8)

        full_name = " ".join(
            part for part in [
                enrollment["first_name"],
                enrollment["middle_name"],
                enrollment["last_name"]
            ]
            if part
        )

        self.add_info_row(
            student_layout,
            0,
            "Student ID",
            enrollment["student_id"]
        )

        self.add_info_row(
            student_layout,
            1,
            "Name",
            full_name
        )

        self.add_info_row(
            student_layout,
            2,
            "Age",
            enrollment["age"]
        )

        self.add_info_row(
            student_layout,
            3,
            "Gender",
            enrollment["gender"]
        )

        self.add_info_row(
            student_layout,
            4,
            "Contact Number",
            enrollment["contact"]
        )

        self.add_info_row(
            student_layout,
            5,
            "Address",
            enrollment["address"]
        )

        self.add_info_row(
            student_layout,
            6,
            "Guardian Name",
            enrollment["guardian"]
        )

        layout.addWidget(student_group)

        enrollment_group = QGroupBox(
            "Enrollment Information"
        )

        enrollment_layout = QGridLayout(
            enrollment_group
        )

        enrollment_layout.setContentsMargins(
            20,
            15,
            20,
            15
        )

        enrollment_layout.setHorizontalSpacing(10)
        enrollment_layout.setVerticalSpacing(8)

        self.add_info_row(
            enrollment_layout,
            0,
            "Grade Level",
            enrollment["grade_level"]
        )

        self.add_info_row(
            enrollment_layout,
            1,
            "Track",
            enrollment["track"]
        )

        self.add_info_row(
            enrollment_layout,
            2,
            "Strand",
            enrollment["strand"]
        )

        self.add_info_row(
            enrollment_layout,
            3,
            "Semester",
            enrollment["semester"]
        )

        layout.addWidget(enrollment_group)

        subjects_group = QGroupBox(
            "Enrolled Subjects"
        )

        subjects_layout = QVBoxLayout(
            subjects_group
        )

        subjects_layout.setContentsMargins(
            15,
            15,
            15,
            15
        )

        subjects_list = QListWidget()

        subjects_list.setSelectionMode(
            QListWidget.SelectionMode.NoSelection
        )

        for subject in enrollment["subjects"]:
            subjects_list.addItem(subject)

        subjects_layout.addWidget(subjects_list)

        layout.addWidget(
            subjects_group,
            1
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Close
        )

        buttons.rejected.connect(
            self.reject
        )

        buttons.accepted.connect(
            self.accept
        )

        layout.addWidget(buttons)

    def add_info_row(
        self,
        grid,
        row,
        label_text,
        value
    ):
        label = QLabel(label_text)
        colon = QLabel(":")
        value_label = QLabel(str(value))

        label.setMinimumHeight(22)
        colon.setMinimumHeight(22)
        value_label.setMinimumHeight(22)

        label.setMinimumWidth(130)
        colon.setFixedWidth(15)

        value_label.setWordWrap(True)

        grid.addWidget(
            label,
            row,
            0
        )

        grid.addWidget(
            colon,
            row,
            1
        )

        grid.addWidget(
            value_label,
            row,
            2
        )

        grid.setColumnStretch(
            2,
            1
        )