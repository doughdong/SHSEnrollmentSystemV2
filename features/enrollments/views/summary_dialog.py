from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QDialogButtonBox,
    QGroupBox
)

class EnrollmentSummaryDialog(QDialog):

    def __init__(
        self,
        student,
        grade,
        track,
        strand,
        semester,
        subjects,
        parent=None
    ):
        super().__init__(parent)
        self.setWindowTitle("Enrollment Summary")
        self.setMinimumSize(600, 500)
        self.resize(700, 600)
        self.setup_ui(
            student,
            grade,
            track,
            strand,
            semester,
            subjects
        )

    def setup_ui(
        self,
        student,
        grade,
        track,
        strand,
        semester,
        subjects
    ):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(15)

        title = QLabel("Enrollment Summary")
        title.setObjectName("dialogTitle")
        layout.addWidget(title)

        student_group = QGroupBox("Student Information")
        student_layout = QFormLayout(student_group)

        full_name = " ".join(
            part for part in [
                student["first_name"],
                student["middle_name"],
                student["last_name"]
            ]
            if part
        )

        student_layout.addRow("Student ID", QLabel(student["student_id"]))
        student_layout.addRow("Name", QLabel(full_name))
        student_layout.addRow("Age", QLabel(str(student["age"])))
        student_layout.addRow("Gender", QLabel(student["gender"]))
        student_layout.addRow("Contact", QLabel(student["contact"]))
        student_layout.addRow("Address", QLabel(student["address"]))
        student_layout.addRow("Guardian", QLabel(student["guardian"]))

        layout.addWidget(student_group)

        enrollment_group = QGroupBox("Enrollment Information")
        enrollment_layout = QFormLayout(enrollment_group)
        enrollment_layout.addRow("Grade Level", QLabel(grade))
        enrollment_layout.addRow("Track", QLabel(track))
        enrollment_layout.addRow("Strand", QLabel(strand))
        enrollment_layout.addRow("Semester", QLabel(semester))

        subjects_text = "\n".join(
            f"{index}. {subject}"
            for index, subject in enumerate(subjects, start=1)
        )
        subjects_label = QLabel(subjects_text)
        subjects_label.setWordWrap(True)
        enrollment_layout.addRow("Subjects", subjects_label)

        layout.addWidget(enrollment_group)
        layout.addStretch()

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
