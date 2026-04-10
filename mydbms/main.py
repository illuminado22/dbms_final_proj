import sys
from PyQt6.QtWidgets import QApplication
from ui import LoginWindow
from styles import MAIN_STYLESHEET

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(MAIN_STYLESHEET)
    window = LoginWindow()
    window._build_ui()
    window.show()
    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()
