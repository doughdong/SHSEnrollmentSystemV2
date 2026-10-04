from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QMessageBox,
    QDialogButtonBox,
    QScrollArea,
    QCheckBox,
    QWidget
)

class SubjectSelectionDialog(QDialog):

    def __init__(
        self,
        service,
        grade,
        track,
        strand,
        semester="1st Semester",
        selected_subjects=None,
        parent=None
    ):
        super().__init__(parent)
        self.service = service
        self.grade = grade
        self.track = track
        self.strand = strand
        self.semester = semester
        self.selected_subjects = selected_subjects or []
        self.checkboxes = []
        self.setWindowTitle("Subject Selection")
        self.setMinimumSize(560, 500)
        self.resize(650, 560)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        title = QLabel("Subject Selection")
        title.setObjectName("dialogTitle")
        layout.addWidget(title)

        info = QFormLayout()
        grade_label = QLineEdit(self.grade)
        track_label = QLineEdit(self.track)
        strand_label = QLineEdit(self.strand)
        grade_label.setReadOnly(True)
        track_label.setReadOnly(True)
        strand_label.setReadOnly(True)
        info.addRow("Grade Level", grade_label)
        info.addRow("Track", track_label)
        info.addRow("Strand", strand_label)

        self.semester_input = QComboBox()
        self.semester_input.addItems(["1st Semester", "2nd Semester"])
        self.semester_input.setCurrentText(self.semester)
        self.semester_input.currentTextChanged.connect(self.load_subjects)
        info.addRow("Semester", self.semester_input)
        layout.addLayout(info)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.subject_container = QWidget()
        self.subject_layout = QVBoxLayout(self.subject_container)
        self.subject_layout.setContentsMargins(15, 15, 15, 15)
        self.subject_layout.setSpacing(8)
        self.scroll.setWidget(self.subject_container)
        layout.addWidget(self.scroll, 1)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.load_subjects()

    def clear_subjects(self):
        self.checkboxes = []
        while self.subject_layout.count():
            item = self.subject_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def load_subjects(self):
        self.semester = self.semester_input.currentText()
        self.clear_subjects()

        subjects = self.service.get_subjects(
            self.grade,
            self.track,
            self.strand,
            self.semester
        )

        if not subjects:
            self.subject_layout.addWidget(
                QLabel("No subjects are available for this selection.")
            )
            self.subject_layout.addStretch()
            return

        for subject in subjects:
            checkbox = QCheckBox(subject)
            if self.semester == getattr(self, "initial_semester", self.semester) and subject in self.selected_subjects:
                checkbox.setChecked(True)
            self.checkboxes.append(checkbox)
            self.subject_layout.addWidget(checkbox)

        self.subject_layout.addStretch()
        self.initial_semester = self.semester

    def get_selected_subjects(self):
        return [
            checkbox.text()
            for checkbox in self.checkboxes
            if checkbox.isChecked()
        ]

    def validate_and_accept(self):
        subjects = self.get_selected_subjects()
        if not subjects:
            QMessageBox.warning(
                self,
                "Subject Selection",
                "Please select at least one subject."
            )
            return
        self.semester = self.semester_input.currentText()
        self.accept()

