import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QPushButton, QStackedWidget
from styles import STYLE
from login import LoginPage
from dashboard import DashboardPage
from projects import ProjectsPage
from students import StudentsPage
from advisers import AdvisersPage
from teams import TeamsPage
from panelists import PanelistsPage

class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CPE Repository Management")
        self.resize(1100, 680)

        self.login = LoginPage()
        self.app   = AppShell()

        self.addWidget(self.login)
        self.addWidget(self.app)

        self.login.login_success.connect(lambda: self.setCurrentIndex(1))
        self.app.logout_clicked.connect(lambda: self.setCurrentIndex(0))

from PyQt6.QtCore import pyqtSignal

class AppShell(QWidget):
    logout_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        outer = QHBoxLayout(self); outer.setContentsMargins(0,0,0,0); outer.setSpacing(0)

        # Sidebar
        sidebar = QFrame(); sidebar.setObjectName("sidebar"); sidebar.setFixedWidth(200)
        sv = QVBoxLayout(sidebar); sv.setContentsMargins(12,20,12,20); sv.setSpacing(4)
        brand = QLabel("CPE Repository")
        brand.setStyleSheet("font-size:14px; font-weight:bold; color:#1a3c5e; padding:8px 8px 16px 8px;")
        sv.addWidget(brand)

        self.pages = {
            "dashboard": DashboardPage(),
            "projects":  ProjectsPage(),
            "students":  StudentsPage(),
            "advisers":  AdvisersPage(),
            "teams":     TeamsPage(),
            "panelists": PanelistsPage(),
        }
        nav_labels = [
            ("dashboard", "🏠  Dashboard"),
            ("projects",  "📁  Projects"),
            ("students",  "🎓  Students"),
            ("advisers",  "👨‍🏫  Advisers"),
            ("teams",     "👥  Teams"),
            ("panelists", "📋  Panelists"),
        ]
        self.nav_btns = {}
        for key, label in nav_labels:
            btn = QPushButton(label); btn.setObjectName("nav")
            btn.clicked.connect(lambda _, k=key: self._switch(k))
            sv.addWidget(btn); self.nav_btns[key] = btn

        sv.addStretch()
        logout = QPushButton("Logout"); logout.setObjectName("danger")
        logout.clicked.connect(self.logout_clicked); sv.addWidget(logout)

        # Page stack
        self.stack = QStackedWidget()
        for p in self.pages.values(): self.stack.addWidget(p)

        outer.addWidget(sidebar)
        outer.addWidget(self.stack)
        self._switch("dashboard")

    def _switch(self, key):
        self.stack.setCurrentWidget(self.pages[key])
        for k, btn in self.nav_btns.items():
            btn.setObjectName("nav_active" if k == key else "nav")
            btn.setStyleSheet("")
        self.setStyleSheet(STYLE)
        if hasattr(self.pages[key], "_load"):
            self.pages[key]._load()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
