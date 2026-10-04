from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QSpinBox,
    QAbstractSpinBox,
    QMessageBox,
    QDialogButtonBox
)


class StudentInformationDialog(QDialog):

    def __init__(self, service, enrollment=None, parent=None):
        super().__init__(parent)
        self.service = service
        self.enrollment = enrollment
        self.grade = ""
        self.track = ""
        self.strand = ""

        self.setWindowTitle(
            "Edit Student Information" if enrollment else "Student Information"
        )
        self.setMinimumSize(650, 650)
        self.resize(760, 700)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(15)

        title = QLabel("Student Information")
        title.setObjectName("dialogTitle")
        layout.addWidget(title)

        form = QFormLayout()
        form.setHorizontalSpacing(20)
        form.setVerticalSpacing(12)

        self.student_id_input = QLineEdit()
        self.student_id_input.setReadOnly(True)
        self.student_id_input.setText(
            self.enrollment["student_id"]
            if self.enrollment
            else self.service.next_student_id()
        )

        self.first_name_input = QLineEdit()
        self.middle_name_input = QLineEdit()
        self.last_name_input = QLineEdit()

        self.age_input = QSpinBox()
        self.age_input.setRange(1, 100)
        self.age_input.setButtonSymbols(
            QAbstractSpinBox.ButtonSymbols.NoButtons
        )

        self.gender_input = QComboBox()
        self.gender_input.addItems(["Male", "Female"])

        self.contact_input = QLineEdit()
        self.address_input = QLineEdit()
        self.guardian_input = QLineEdit()

        self.grade_input = QComboBox()
        self.grade_input.addItems(["Grade 11", "Grade 12"])

        self.track_input = QComboBox()
        self.track_input.addItems(["Academic", "TVL"])
        self.track_input.currentTextChanged.connect(self.update_strands)

        self.strand_input = QComboBox()

        form.addRow("Student ID", self.student_id_input)
        form.addRow("First Name", self.first_name_input)
        form.addRow("Middle Name", self.middle_name_input)
        form.addRow("Last Name", self.last_name_input)
        form.addRow("Age", self.age_input)
        form.addRow("Gender", self.gender_input)
        form.addRow("Contact Number", self.contact_input)
        form.addRow("Address", self.address_input)
        form.addRow("Guardian Name", self.guardian_input)
        form.addRow("Grade Level", self.grade_input)
        form.addRow("Track", self.track_input)
        form.addRow("Strand", self.strand_input)

        layout.addLayout(form)

        layout.addSpacing(25)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.button(
            QDialogButtonBox.StandardButton.Ok
        ).setText("Next")

        buttons.accepted.connect(self.validate_and_accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

        layout.addStretch()

        if self.enrollment:
            self.first_name_input.setText(
                self.enrollment["first_name"]
            )
            self.middle_name_input.setText(
                self.enrollment["middle_name"] or ""
            )
            self.last_name_input.setText(
                self.enrollment["last_name"]
            )
            self.age_input.setValue(
                int(self.enrollment["age"])
            )
            self.gender_input.setCurrentText(
                self.enrollment["gender"]
            )
            self.contact_input.setText(
                self.enrollment["contact"]
            )
            self.address_input.setText(
                self.enrollment["address"]
            )
            self.guardian_input.setText(
                self.enrollment["guardian"]
            )
            self.grade_input.setCurrentText(
                self.enrollment["grade_level"]
            )
            self.track_input.setCurrentText(
                self.enrollment["track"]
            )
            self.update_strands()
            self.strand_input.setCurrentText(
                self.enrollment["strand"]
            )
        else:
            self.update_strands()

    def update_strands(self):
        current = self.strand_input.currentText()

        self.strand_input.blockSignals(True)
        self.strand_input.clear()

        if self.track_input.currentText() == "Academic":
            self.strand_input.addItems(
                ["STEM", "ABM", "HUMSS", "GAS"]
            )
        else:
            self.strand_input.addItems(
                ["ICT - Programming", "ICT - CSS"]
            )

        if current:
            index = self.strand_input.findText(current)
            if index >= 0:
                self.strand_input.setCurrentIndex(index)

        self.strand_input.blockSignals(False)

    def validate_and_accept(self):
        required = [
            (self.first_name_input.text(), "First Name"),
            (self.last_name_input.text(), "Last Name"),
            (self.contact_input.text(), "Contact Number"),
            (self.address_input.text(), "Address"),
            (self.guardian_input.text(), "Guardian Name")
        ]

        for value, label in required:
            if not value.strip():
                QMessageBox.warning(
                    self,
                    "Required Field",
                    f"{label} is required."
                )
                return

        self.grade = self.grade_input.currentText()
        self.track = self.track_input.currentText()
        self.strand = self.strand_input.currentText()

        self.accept()

    def get_student(self):
        return {
            "student_id": self.student_id_input.text().strip(),
            "first_name": self.first_name_input.text().strip(),
            "middle_name": self.middle_name_input.text().strip(),
            "last_name": self.last_name_input.text().strip(),
            "age": self.age_input.value(),
            "gender": self.gender_input.currentText(),
            "contact": self.contact_input.text().strip(),
            "address": self.address_input.text().strip(),
            "guardian": self.guardian_input.text().strip()
        }