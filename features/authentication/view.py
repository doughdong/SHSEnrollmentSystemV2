from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QFormLayout,
    QHBoxLayout
)


class AuthenticationView(QDialog):

    def __init__(self, service, parent=None):
        super().__init__(parent)
        self.service = service
        self.logged_in_username = ""
        self.setWindowTitle("SHS Enrollment System")
        self.setMinimumSize(520, 560)
        self.resize(600, 620)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(55, 45, 55, 45)
        layout.setSpacing(20)

        title = QLabel("SHS Enrollment System")
        title.setObjectName("dialogTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Sign in to continue")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form_layout = QFormLayout()
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(18)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        form_layout.addRow(
            "Username",
            self.username_input
        )

        form_layout.addRow(
            "Password",
            self.password_input
        )

        login_button = QPushButton("Login")
        login_button.setObjectName("primaryButton")
        login_button.clicked.connect(self.login)

        signup_button = QPushButton("Create an Account")
        signup_button.clicked.connect(self.open_signup)

        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(12)
        buttons_layout.addWidget(login_button)
        buttons_layout.addWidget(signup_button)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(15)
        layout.addLayout(form_layout)
        layout.addSpacing(15)
        layout.addLayout(buttons_layout)
        layout.addStretch()

        self.username_input.returnPressed.connect(
            self.login
        )

        self.password_input.returnPressed.connect(
            self.login
        )

        self.username_input.setFocus()

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(
                self,
                "Login",
                "Please enter your username and password."
            )
            return

        if self.service.login(username, password):
            self.logged_in_username = username
            self.accept()
        else:
            QMessageBox.warning(
                self,
                "Login Failed",
                "Invalid username or password."
            )

            self.username_input.clear()
            self.password_input.clear()
            self.username_input.setFocus()

    def open_signup(self):
        dialog = SignupDialog(
            self.service,
            self
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:
            QMessageBox.information(
                self,
                "Account Created",
                "Your account has been created successfully."
            )


class SignupDialog(QDialog):

    def __init__(self, service, parent=None):
        super().__init__(parent)
        self.service = service
        self.setWindowTitle("Create an Account")
        self.setMinimumSize(500, 480)
        self.resize(560, 520)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(55, 45, 55, 45)
        layout.setSpacing(20)

        title = QLabel("Create an Account")
        title.setObjectName("dialogTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Enter your account details")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form_layout = QFormLayout()
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(18)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText(
            "Enter username"
        )

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText(
            "Enter password"
        )
        self.password_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText(
            "Confirm password"
        )
        self.confirm_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        form_layout.addRow(
            "Username",
            self.username_input
        )

        form_layout.addRow(
            "Password",
            self.password_input
        )

        form_layout.addRow(
            "Confirm Password",
            self.confirm_input
        )

        create_button = QPushButton(
            "Create Account"
        )

        create_button.setObjectName(
            "primaryButton"
        )

        create_button.clicked.connect(
            self.signup
        )

        cancel_button = QPushButton(
            "Cancel"
        )

        cancel_button.clicked.connect(
            self.reject
        )

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)
        buttons_layout.addWidget(
            create_button
        )
        buttons_layout.addWidget(
            cancel_button
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(10)
        layout.addLayout(form_layout)
        layout.addSpacing(10)
        layout.addLayout(buttons_layout)
        layout.addStretch()

    def signup(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        confirm = self.confirm_input.text()

        if not username or not password or not confirm:
            QMessageBox.warning(
                self,
                "Create Account",
                "Please complete all fields."
            )
            return

        if password != confirm:
            QMessageBox.warning(
                self,
                "Create Account",
                "Passwords do not match."
            )
            return

        try:
            self.service.signup(
                username,
                password
            )
        except ValueError as error:
            QMessageBox.warning(
                self,
                "Create Account",
                str(error)
            )
            return

        self.accept()