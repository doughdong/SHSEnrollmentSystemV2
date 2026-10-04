import sys
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QMainWindow,
    QMessageBox,
    QLabel,
    QWidget,
    QHBoxLayout,
    QPushButton
)

from database.database import Database
from features.authentication.service import AuthenticationService
from features.authentication.view import AuthenticationView
from features.enrollments.service import EnrollmentService
from features.enrollments.views.enrollment_view import EnrollmentView


def load_stylesheet(app):
    path = Path(__file__).with_name("style.qss")

    if path.exists():
        app.setStyleSheet(
            path.read_text(encoding="utf-8")
        )


class MainWindow(QMainWindow):

    def __init__(self, database, username, logout_callback):
        super().__init__()

        self.database = database
        self.username = username
        self.logout_callback = logout_callback

        self.setWindowTitle("SHS Enrollment System")
        self.setMinimumSize(900, 600)
        self.resize(1150, 750)

        service = EnrollmentService(database)

        self.enrollment_view = EnrollmentView(service)
        self.setCentralWidget(self.enrollment_view)

        self.create_header()

    def create_header(self):
        header = QWidget()

        layout = QHBoxLayout(header)
        layout.setContentsMargins(15, 5, 15, 5)
        layout.setSpacing(10)

        title = QLabel("SHS Enrollment System")
        title.setStyleSheet(
            "font-size: 16px; font-weight: 600;"
        )

        logged_in = QLabel(
            f"Logged in: {self.username}"
        )
        logged_in.setStyleSheet(
            "font-size: 14px;"
        )

        logout_button = QPushButton("Logout")
        logout_button.clicked.connect(
            self.logout
        )

        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(logged_in)
        layout.addWidget(logout_button)

        self.setMenuWidget(header)

    def logout(self):
        answer = QMessageBox.question(
            self,
            "Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No
        )

        if answer == QMessageBox.StandardButton.Yes:
            self.logout_callback()


class ApplicationController:

    def __init__(self, app, database):
        self.app = app
        self.database = database
        self.authentication_service = (
            AuthenticationService(database)
        )
        self.main_window = None

    def start(self):
        self.show_login()
        self.app.exec()

    def show_login(self):
        login = AuthenticationView(
            self.authentication_service
        )

        result = login.exec()

        if result != QDialog.DialogCode.Accepted:
            self.app.quit()
            return

        self.show_main_window(
            login.logged_in_username
        )

    def show_main_window(self, username):
        self.main_window = MainWindow(
            self.database,
            username,
            self.logout
        )

        self.main_window.show()
        self.main_window.raise_()
        self.main_window.activateWindow()

    def logout(self):
        if self.main_window:
            self.main_window.close()
            self.main_window.deleteLater()
            self.main_window = None

        self.show_login()


def main():
    app = QApplication(sys.argv)

    app.setQuitOnLastWindowClosed(False)

    load_stylesheet(app)

    database = Database(
        Path(__file__).with_name("school.db")
    )

    database.create_tables()

    controller = ApplicationController(
        app,
        database
    )

    controller.start()

    sys.exit(0)


if __name__ == "__main__":
    main()