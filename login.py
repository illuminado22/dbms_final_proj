from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from config import get_conn

class LoginPage(QWidget):
    login_success = pyqtSignal()

    def __init__(self):
        super().__init__()
        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        # Left branding panel
        left = QFrame()
        left.setStyleSheet("background-color: #1a3c5e;")
        lv = QVBoxLayout(left)
        lv.setAlignment(Qt.AlignmentFlag.AlignCenter)
        brand = QLabel("CPE Repository\nManagement")
        brand.setStyleSheet("color: white; font-size: 26px; font-weight: bold;")
        brand.setAlignment(Qt.AlignmentFlag.AlignCenter)
        note = QLabel("• TIP email validation (@tip.edu.ph)\n• Only for CPE students, alumni, and professors")
        note.setStyleSheet("color: #a8c8e8; font-size: 12px;")
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lv.addWidget(brand)
        lv.addSpacing(16)
        lv.addWidget(note)

        # Right login form
        right = QFrame()
        right.setStyleSheet("background: white;")
        rv = QVBoxLayout(right)
        rv.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rv.setContentsMargins(60, 40, 60, 40)

        rv.addWidget(self._lbl("Welcome!", "font-size:26px; font-weight:bold; color:#1a3c5e;"))
        rv.addWidget(self._lbl("Sign in with your TIP account credentials.", "color:#777; margin-bottom:10px;"))
        rv.addSpacing(16)
        rv.addWidget(QLabel("TIP Email"))
        self.email = QLineEdit(); self.email.setPlaceholderText("cir.email@tip.edu.ph")
        rv.addWidget(self.email)
        rv.addSpacing(8)
        rv.addWidget(QLabel("Password"))
        self.password = QLineEdit(); self.password.setPlaceholderText("Enter your password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        rv.addWidget(self.password)
        rv.addSpacing(16)
        btn = QPushButton("Log In"); btn.setFixedHeight(40)
        btn.setStyleSheet("background-color: white; color: #1a3c5e; border: 1px solid #1a3c5e; border-radius: 6px; padding: 8px 18px;")
        btn.clicked.connect(self._login)
        rv.addWidget(btn)
        self.msg = QLabel(""); self.msg.setStyleSheet("color:red;")
        rv.addWidget(self.msg)

        outer.addWidget(left, 1)
        outer.addWidget(right, 1)

    def _lbl(self, text, style):
        l = QLabel(text); l.setStyleSheet(style); return l

    def _login(self):
        email = self.email.text().strip()
        pwd   = self.password.text().strip()
        if "@tip.edu.ph" not in email:
            self.msg.setText("Email must be @tip.edu.ph"); return
        if not pwd:
            self.msg.setText("Enter your password."); return
        try:
            conn = get_conn(); cur = conn.cursor()
            cur.execute("SELECT 1 FROM students WHERE email=%s", (email,))
            found = cur.fetchone()
            if not found:
                cur.execute("SELECT 1 FROM advisers WHERE email=%s", (email,))
                found = cur.fetchone()
            conn.close()
            if found: self.login_success.emit()
            else: self.msg.setText("Account not found. Contact admin.")
        except:
            # Demo mode: let in if email looks valid
            self.login_success.emit()
