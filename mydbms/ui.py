from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
import asyncio
import sys
import os
from styles import COLORS, MAIN_STYLESHEET

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CPE Repository Management")
        self.setGeometry(100, 100, 1200, 700)

    def _build_ui(self):
        #ui
        main_container = QWidget()
        main_container.setObjectName("mainContainer")
        
        #layouts
        main_layout = QHBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left panel 
        self._build_intro_panel(main_layout)
        
        # Right panel 
        self._build_auth_panel(main_layout)
        
        self.setCentralWidget(main_container)

    def _build_intro_panel(self, parent_layout: QHBoxLayout):
        #left 
        intro_panel = QWidget()
        intro_panel.setObjectName("introPanel")
        intro_panel.setStyleSheet(f"background-color: transparent;")
        
        intro_layout = QVBoxLayout(intro_panel)
        intro_layout.setSpacing(10)
        intro_layout.setContentsMargins(40, 40, 40, 40)
        intro_layout.addStretch(2)
        
        #title
        title = QLabel("CPE Repository\nManagement")
        title.setObjectName("titleLabel")
        title.setFont(QFont("Source Serif 4", 32, QFont.Weight.Bold))
        title.setWordWrap(True)
        intro_layout.addWidget(title)
        
        #guide
        intro_layout.addSpacing(20)
        points_text = "• TIP email validation (@tip.edu.ph)\n• Only for CPE student (alumni, prof, undergraduate)"
        points = QLabel(points_text)
        points.setObjectName("pointsLabel")
        points.setFont(QFont("Segoe UI", 12))
        points.setStyleSheet(f"color: {COLORS['ink_700']};")
        intro_layout.addWidget(points)
        
        intro_layout.addStretch(3)
        
        parent_layout.addWidget(intro_panel, 1)

    def _build_auth_panel(self, parent_layout: QHBoxLayout):
        #right
        auth_panel = QWidget()
        auth_layout = QVBoxLayout(auth_panel)
        auth_layout.setSpacing(0)
        auth_layout.setContentsMargins(20, 20, 20, 20)
        auth_layout.addStretch(1)
        
        # Auth card container
        auth_card = QWidget()
        auth_card.setObjectName("authCard")
        auth_card.setMaximumWidth(480)
        auth_card.setStyleSheet(f"""
            QWidget#authCard {{
                background-color: {COLORS['paper']};
                border: 1px solid {COLORS['border']};
                border-radius: 18px;
            }}
        """)
        
        card_layout = QVBoxLayout(auth_card)
        card_layout.setSpacing(12)
        card_layout.setContentsMargins(25, 20, 25, 20)
        
        #welcome
        self.auth_title = QLabel("Welcome!")
        self.auth_title.setObjectName("authTitle")
        self.auth_title.setFont(QFont("Source Serif 4", 24, QFont.Weight.Bold))
        card_layout.addWidget(self.auth_title)
        
        self.auth_subtitle = QLabel("Sign in with your TIP account credentials.")
        self.auth_subtitle.setObjectName("authSubtitle")
        self.auth_subtitle.setFont(QFont("Segoe UI", 12))
        card_layout.addWidget(self.auth_subtitle)
        
        # Login form container
        self.login_form_widget = QWidget()
        self._build_login_form(self.login_form_widget)
        card_layout.addWidget(self.login_form_widget)
        
        auth_panel_inner_layout = QVBoxLayout()
        auth_panel_inner_layout.addWidget(auth_card)
        auth_panel_inner_layout.addStretch(1)
        
        container = QWidget()
        container.setLayout(auth_panel_inner_layout)
        
        parent_layout.addWidget(container, 1)
    
    def _build_login_form(self, form_widget: QWidget):
        #login guides
        layout = QVBoxLayout(form_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)
        
        #Email 
        email_label = QLabel("TIP Email")
        email_label.setObjectName("fieldLabel")
        layout.addWidget(email_label)
        
        self.login_email = QLineEdit()
        self.login_email.setPlaceholderText("your.email@tip.edu.ph")
        layout.addWidget(self.login_email)
        
        self.login_email_error = QLabel()
        self.login_email_error.setObjectName("errorLabel")
        layout.addWidget(self.login_email_error)
        
        #Password
        password_label = QLabel("Password")
        password_label.setObjectName("fieldLabel")
        layout.addWidget(password_label)
        
        password_container = QHBoxLayout()
        password_container.setSpacing(6)
        
        self.login_password = QLineEdit()
        self.login_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_password.setPlaceholderText("Enter your password")
        password_container.addWidget(self.login_password)
        
        self.login_show_password = QPushButton("Show")
        self.login_show_password.setObjectName("toggleButton")
        self.login_show_password.setMaximumWidth(60)
        self.login_show_password.setMinimumHeight(32)
        self.login_show_password.clicked.connect(self._toggle_login_password)
        password_container.addWidget(self.login_show_password)
        
        password_widget = QWidget()
        password_widget.setLayout(password_container)
        layout.addWidget(password_widget)
        
        self.login_password_error = QLabel()
        self.login_password_error.setObjectName("errorLabel")
        layout.addWidget(self.login_password_error)
        
        #Submit 
        self.login_submit = QPushButton("Log In")
        self.login_submit.setObjectName("primaryButton")
        self.login_submit.setMinimumHeight(35)
        self.login_submit.clicked.connect(self._handle_login)
        layout.addWidget(self.login_submit)

    def _show_login_view(self):
        """Switch to login form view."""
        self.auth_title.setText("Welcome")
        self.auth_subtitle.setText("Sign in with your TIP account credentials.")
        self.login_form_widget.show()
        self.signup_form_widget.hide()
        self._clear_errors()
        self._reset_password_toggles()
        self.login_email.setFocus()

    def _clear_errors(self):
        """Clear all error messages."""
        self.login_email_error.setText("")
        self.login_password_error.setText("")



    def _toggle_login_password(self):
        """Toggle login password visibility."""
        if self.login_password.echoMode() == QLineEdit.EchoMode.Password:
            self.login_password.setEchoMode(QLineEdit.EchoMode.Normal)
            self.login_show_password.setText("Hide")
        else:
            self.login_password.setEchoMode(QLineEdit.EchoMode.Password)
            self.login_show_password.setText("Show")



    def _reset_password_toggles(self):
        """Reset password toggle button text."""
        self.login_show_password.setText("Show")

    def _handle_login(self):
        """Handle login form submission."""
        email = self.login_email.text()
        password = self.login_password.text()
        
        # Clear previous errors
        self.login_email_error.setText("")
        self.login_password_error.setText("")
        
        # Validation
        if not email:
            self.login_email_error.setText("Email is required")
            return
        if not password:
            self.login_password_error.setText("Password is required")
            return
        
        print(f"Login attempt: {email}")



    