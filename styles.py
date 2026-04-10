STYLE = """
QMainWindow, QWidget {
    background-color: #f0f4f8;
    font-family: Segoe UI, Arial;
    font-size: 13px;
}
QLabel#title {
    font-size: 22px;
    font-weight: bold;
    color: #1a3c5e;
}
QPushButton {
    background-color: #1a3c5e;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 18px;
}
QPushButton:hover { background-color: #2a5480; }
QPushButton#danger { background-color: #c0392b; }
QPushButton#danger:hover { background-color: #e74c3c; }
QPushButton#secondary { background-color: #6c757d; }
QPushButton#secondary:hover { background-color: #5a6268; }
QPushButton#nav {
    background-color: transparent;
    color: #1a3c5e;
    text-align: left;
    padding: 10px 16px;
    border-radius: 8px;
}
QPushButton#nav:hover { background-color: #d0e4f7; }
QPushButton#nav_active {
    background-color: #1a3c5e;
    color: white;
    text-align: left;
    padding: 10px 16px;
    border-radius: 8px;
}
QLineEdit, QTextEdit, QComboBox {
    border: 1px solid #ccd6e0;
    border-radius: 6px;
    padding: 7px 10px;
    background: white;
}
QLineEdit:focus, QTextEdit:focus { border: 1.5px solid #1a3c5e; }
QTableWidget {
    background: white;
    border: 1px solid #dce3ea;
    border-radius: 8px;
    gridline-color: #eef1f4;
}
QTableWidget::item:selected { background-color: #d0e4f7; color: #1a3c5e; }
QHeaderView::section {
    background-color: #1a3c5e;
    color: white;
    padding: 8px;
    font-weight: bold;
    border: none;
}
QFrame#card { background: white; border-radius: 10px; border: 1px solid #dce3ea; }
QFrame#sidebar { background: white; border-right: 1px solid #dce3ea; }
"""
