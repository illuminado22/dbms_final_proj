from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QDialog, QFormLayout, QComboBox, QDialogButtonBox, QMessageBox)
from config import get_conn
from helpers import make_table, fill_table, confirm_delete

class StudentsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self); layout.setContentsMargins(24,24,24,24)
        h = QHBoxLayout()
        t = QLabel("Students"); t.setObjectName("title")
        h.addWidget(t); h.addStretch()
        self.search = QLineEdit(); self.search.setPlaceholderText("Search name or email…"); self.search.setFixedWidth(240)
        self.search.textChanged.connect(self._load); h.addWidget(self.search)
        btn = QPushButton("+ Add Student"); btn.clicked.connect(lambda: self._open(None))
        h.addWidget(btn); layout.addLayout(h); layout.addSpacing(10)
        self.table = make_table(["ID","Name","Email","Course","Year","Actions"], stretch_cols=[1,2])
        layout.addWidget(self.table)

    def _load(self):
        q = self.search.text().strip()
        try:
            conn = get_conn(); cur = conn.cursor()
            if q: cur.execute("SELECT student_id,student_name,email,course,year_level FROM students WHERE student_name LIKE %s OR email LIKE %s",(f"%{q}%",f"%{q}%"))
            else:  cur.execute("SELECT student_id,student_name,email,course,year_level FROM students ORDER BY student_id DESC")
            rows = cur.fetchall(); conn.close()
            fill_table(self.table, rows, 5, self._open, self._delete)
        except Exception as e: QMessageBox.critical(self,"DB Error",str(e))

    def _open(self, sid):
        if StudentDialog(self, sid).exec(): self._load()

    def _delete(self, sid):
        if confirm_delete(self, "Delete this student?"):
            try:
                conn = get_conn(); cur = conn.cursor()
                cur.execute("DELETE FROM team_member WHERE student_id=%s",(sid,))
                cur.execute("DELETE FROM students WHERE student_id=%s",(sid,))
                conn.commit(); conn.close(); self._load()
            except Exception as e: QMessageBox.critical(self,"Error",str(e))

class StudentDialog(QDialog):
    def __init__(self, parent, sid=None):
        super().__init__(parent); self.sid = sid
        self.setWindowTitle("Edit Student" if sid else "Add Student"); self.setMinimumWidth(340)
        f = QFormLayout(self); f.setSpacing(12)
        self.name   = QLineEdit()
        self.email  = QLineEdit()
        self.course = QLineEdit(); self.course.setText("CPE")
        self.year   = QComboBox(); self.year.addItems(["1","2","3","4","Alumni"])
        f.addRow("Name *",    self.name);   f.addRow("Email", self.email)
        f.addRow("Course",    self.course); f.addRow("Year Level", self.year)
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(self._save); btns.rejected.connect(self.reject); f.addRow(btns)
        if sid: self._load()

    def _load(self):
        try:
            conn = get_conn(); cur = conn.cursor()
            cur.execute("SELECT student_name,email,course,year_level FROM students WHERE student_id=%s",(self.sid,))
            r = cur.fetchone(); conn.close()
            if r:
                self.name.setText(r[0] or ""); self.email.setText(r[1] or ""); self.course.setText(r[2] or "")
                idx = self.year.findText(str(r[3]))
                if idx >= 0: self.year.setCurrentIndex(idx)
        except Exception as e: QMessageBox.critical(self,"Error",str(e))

    def _save(self):
        n = self.name.text().strip()
        if not n: QMessageBox.warning(self,"Required","Name is required."); return
        try:
            conn = get_conn(); cur = conn.cursor()
            vals = (n, self.email.text().strip(), self.course.text().strip(), self.year.currentText())
            if self.sid: cur.execute("UPDATE students SET student_name=%s,email=%s,course=%s,year_level=%s WHERE student_id=%s",(*vals,self.sid))
            else:        cur.execute("INSERT INTO students (student_name,email,course,year_level) VALUES (%s,%s,%s,%s)",vals)
            conn.commit(); conn.close(); self.accept()
        except Exception as e: QMessageBox.critical(self,"Error",str(e))
