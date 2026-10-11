
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QDialog
)

from features.enrollments.views.student_dialog import StudentInformationDialog
from features.enrollments.views.subject_dialog import SubjectSelectionDialog
from features.enrollments.views.summary_dialog import EnrollmentSummaryDialog
from features.enrollments.views.student_view import StudentViewDialog


class EnrollmentView(QWidget):

    def __init__(self, service):
        super().__init__()

        self.service = service
        self.enrollments = []

        self.setup_ui()

        self.installEventFilter(self)
        self.table.installEventFilter(self)

        self.load_enrollments()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("Enrolled Students")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(8)

        # Search field
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search by Student ID or student name"
        )
        self.search_input.textChanged.connect(self.filter_table)

        # Track filter
        self.track_filter = QComboBox()
        self.track_filter.setMinimumWidth(120)
        self.track_filter.addItem("All Tracks")
        self.track_filter.currentTextChanged.connect(
            self.update_strand_filter
        )

        # Strand filter
        self.strand_filter = QComboBox()
        self.strand_filter.setMinimumWidth(130)
        self.strand_filter.addItem("All Strands")
        self.strand_filter.currentTextChanged.connect(
            self.filter_table
        )

        # Buttons
        enroll_button = QPushButton("Enroll Student")
        enroll_button.setObjectName("primaryButton")
        enroll_button.clicked.connect(self.enroll_student)

        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(self.edit_selected)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_selected)

        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_search)

        # Add controls to toolbar
        toolbar.addWidget(self.search_input, 1)
        toolbar.addWidget(self.track_filter)
        toolbar.addWidget(self.strand_filter)
        toolbar.addWidget(enroll_button)
        toolbar.addWidget(edit_button)
        toolbar.addWidget(delete_button)
        toolbar.addWidget(clear_button)

        layout.addLayout(toolbar)

        # Student records table
        self.table = QTableWidget(0, 9)

        self.table.setHorizontalHeaderLabels([
            "Student ID",
            "Name",
            "Age",
            "Gender",
            "Grade",
            "Track",
            "Strand",
            "Semester",
            "Subjects"
        ])

        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )

        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.table.cellDoubleClicked.connect(self.view_selected)

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.table.verticalHeader().setVisible(False)

        layout.addWidget(self.table, 1)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            if obj is not self.table:
                self.table.clearSelection()
                self.table.setCurrentItem(None)

        return super().eventFilter(obj, event)

    def load_enrollments(self):
        try:
            self.enrollments = self.service.get_enrollments()

            self.update_track_filter()
            self.update_strand_filter()

            self.filter_table()

            self.table.clearSelection()
            self.table.setCurrentItem(None)

        except Exception as error:
            QMessageBox.critical(
                self,
                "Database Error",
                str(error)
            )

    def update_track_filter(self):
        # Keep the previous selection if it still exists.
        previous_track = self.track_filter.currentText()

        tracks = sorted({
            str(enrollment["track"])
            for enrollment in self.enrollments
            if enrollment.get("track")
        })

        self.track_filter.blockSignals(True)
        self.track_filter.clear()
        self.track_filter.addItem("All Tracks")

        for track in tracks:
            self.track_filter.addItem(track)

        index = self.track_filter.findText(previous_track)

        if index >= 0:
            self.track_filter.setCurrentIndex(index)

        self.track_filter.blockSignals(False)

    def update_strand_filter(self, *args):
        # Show only strands belonging to the selected track.
        selected_track = self.track_filter.currentText()
        previous_strand = self.strand_filter.currentText()

        strands = set()

        for enrollment in self.enrollments:
            track = str(enrollment.get("track", ""))
            strand = str(enrollment.get("strand", ""))

            if not strand:
                continue

            if (
                selected_track == "All Tracks"
                or track == selected_track
            ):
                strands.add(strand)

        self.strand_filter.blockSignals(True)
        self.strand_filter.clear()
        self.strand_filter.addItem("All Strands")

        for strand in sorted(strands):
            self.strand_filter.addItem(strand)

        # Restore the strand if it is available for this track.
        index = self.strand_filter.findText(previous_strand)

        if index >= 0:
            self.strand_filter.setCurrentIndex(index)

        self.strand_filter.blockSignals(False)

        self.filter_table()

    def filter_table(self, *args):
        search = self.search_input.text().strip().lower()

        selected_track = self.track_filter.currentText()
        selected_strand = self.strand_filter.currentText()

        filtered = []

        for enrollment in self.enrollments:
            full_name = " ".join(
                str(part)
                for part in [
                    enrollment.get("first_name", ""),
                    enrollment.get("middle_name", ""),
                    enrollment.get("last_name", "")
                ]
                if part
            )

            student_id = str(enrollment.get("student_id", ""))
            track = str(enrollment.get("track", ""))
            strand = str(enrollment.get("strand", ""))

            # Search by student ID or name.
            matches_search = (
                not search
                or search in student_id.lower()
                or search in full_name.lower()
            )

            # Filter by track.
            matches_track = (
                selected_track == "All Tracks"
                or track == selected_track
            )

            # Filter by strand.
            matches_strand = (
                selected_strand == "All Strands"
                or strand == selected_strand
            )

            if matches_search and matches_track and matches_strand:
                filtered.append(enrollment)

        self.table.setRowCount(len(filtered))

        for row, enrollment in enumerate(filtered):
            full_name = " ".join(
                str(part)
                for part in [
                    enrollment.get("first_name", ""),
                    enrollment.get("middle_name", ""),
                    enrollment.get("last_name", "")
                ]
                if part
            )

            subjects = enrollment.get("subjects", [])

            if isinstance(subjects, (list, tuple)):
                subjects_text = ", ".join(str(subject) for subject in subjects)
            else:
                subjects_text = str(subjects or "")

            values = [
                str(enrollment.get("student_id", "")),
                full_name,
                str(enrollment.get("age", "")),
                str(enrollment.get("gender", "")),
                str(enrollment.get("grade_level", "")),
                str(enrollment.get("track", "")),
                str(enrollment.get("strand", "")),
                str(enrollment.get("semester", "")),
                subjects_text
            ]

            for column, value in enumerate(values):
                item = QTableWidgetItem(value)

                item.setData(
                    Qt.ItemDataRole.UserRole,
                    enrollment["id"]
                )

                self.table.setItem(row, column, item)

        self.table.clearSelection()
        self.table.setCurrentItem(None)

    def clear_search(self):
        self.search_input.clear()

        self.track_filter.setCurrentIndex(0)
        self.update_strand_filter()
        self.strand_filter.setCurrentIndex(0)

        self.table.clearSelection()
        self.table.setCurrentItem(None)

    def get_selected_enrollment(self):
        selected_rows = self.table.selectionModel().selectedRows()

        if not selected_rows:
            return None

        row = selected_rows[0].row()
        item = self.table.item(row, 0)

        if item is None:
            return None

        enrollment_id = item.data(Qt.ItemDataRole.UserRole)

        for enrollment in self.enrollments:
            if enrollment["id"] == enrollment_id:
                return enrollment

        return None

    def view_selected(self, row=None, column=None):
        if row is not None and row >= 0:
            self.table.selectRow(row)

        enrollment = self.get_selected_enrollment()

        if not enrollment:
            return

        dialog = StudentViewDialog(enrollment, parent=self)
        dialog.exec()

        self.table.clearSelection()
        self.table.setCurrentItem(None)

    def enroll_student(self):
        student_dialog = StudentInformationDialog(
            self.service,
            parent=self
        )

        if student_dialog.exec() != QDialog.DialogCode.Accepted:
            return

        student = student_dialog.get_student()

        grade = student_dialog.grade
        track = student_dialog.track
        strand = student_dialog.strand

        subject_dialog = SubjectSelectionDialog(
            self.service,
            grade,
            track,
            strand,
            parent=self
        )

        if subject_dialog.exec() != QDialog.DialogCode.Accepted:
            return

        semester = subject_dialog.semester
        subjects = subject_dialog.get_selected_subjects()

        summary = EnrollmentSummaryDialog(
            student,
            grade,
            track,
            strand,
            semester,
            subjects,
            parent=self
        )

        if summary.exec() != QDialog.DialogCode.Accepted:
            return

        try:
            self.service.save_enrollment(
                student,
                grade,
                track,
                strand,
                semester,
                subjects
            )

        except Exception as error:
            QMessageBox.warning(
                self,
                "Enrollment Failed",
                str(error)
            )
            return

        QMessageBox.information(
            self,
            "Enrollment Successful",
            "Student enrollment has been saved successfully."
        )

        self.load_enrollments()

    def edit_selected(self):
        enrollment = self.get_selected_enrollment()

        if not enrollment:
            QMessageBox.warning(
                self,
                "Edit Student",
                "Please select an enrolled student first."
            )
            return

        student_dialog = StudentInformationDialog(
            self.service,
            enrollment=enrollment,
            parent=self
        )

        if student_dialog.exec() != QDialog.DialogCode.Accepted:
            return

        student = student_dialog.get_student()

        grade = student_dialog.grade
        track = student_dialog.track
        strand = student_dialog.strand

        subject_dialog = SubjectSelectionDialog(
            self.service,
            grade,
            track,
            strand,
            semester=enrollment["semester"],
            selected_subjects=enrollment["subjects"],
            parent=self
        )

        if subject_dialog.exec() != QDialog.DialogCode.Accepted:
            return

        semester = subject_dialog.semester
        subjects = subject_dialog.get_selected_subjects()

        summary = EnrollmentSummaryDialog(
            student,
            grade,
            track,
            strand,
            semester,
            subjects,
            parent=self
        )

        if summary.exec() != QDialog.DialogCode.Accepted:
            return

        try:
            self.service.update_enrollment(
                enrollment["id"],
                student,
                grade,
                track,
                strand,
                semester,
                subjects
            )

        except Exception as error:
            QMessageBox.warning(
                self,
                "Update Failed",
                str(error)
            )
            return

        QMessageBox.information(
            self,
            "Updated",
            "Student enrollment has been updated successfully."
        )

        self.load_enrollments()

    def delete_selected(self):
        enrollment = self.get_selected_enrollment()

        if not enrollment:
            QMessageBox.warning(
                self,
                "Delete Student",
                "Please select an enrolled student first."
            )
            return

        full_name = " ".join(
            str(part)
            for part in [
                enrollment.get("first_name", ""),
                enrollment.get("middle_name", ""),
                enrollment.get("last_name", "")
            ]
            if part
        )

        answer = QMessageBox.question(
            self,
            "Delete Student",
            f"Delete the enrollment record of {full_name}?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        try:
            self.service.delete_enrollment(enrollment["id"])

        except Exception as error:
            QMessageBox.warning(
                self,
                "Delete Failed",
                str(error)
            )
            return

        QMessageBox.information(
            self,
            "Deleted",
            "Student enrollment has been deleted successfully."
        )

        self.load_enrollments()
