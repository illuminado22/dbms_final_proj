from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox)
from config import get_conn
from helpers import make_table, fill_table, confirm_delete, reset_auto_increment

class AdvisersPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self); layout.setContentsMargins(24,24,24,24)
        h = QHBoxLayout()
        t = QLabel("Advisers"); t.setObjectName("title")
        h.addWidget(t); h.addStretch()
        btn = QPushButton("+ Add Adviser"); btn.clicked.connect(lambda: self._open(None))
        h.addWidget(btn); layout.addLayout(h); layout.addSpacing(10)
        self.table = make_table(["ID","Name","Email","Actions"], stretch_cols=[1,2])
        layout.addWidget(self.table)

    def _load(self):
        try:
            conn = get_conn(); cur = conn.cursor()
            cur.execute("SELECT adviser_id,adviser_name,email FROM advisers ORDER BY adviser_id DESC")
            rows = cur.fetchall(); conn.close()
            fill_table(self.table, rows, 3, self._open, self._delete)
        except Exception as e: QMessageBox.critical(self,"DB Error",str(e))

    def _open(self, aid):
        if AdviserDialog(self, aid).exec(): self._load()

    def _delete(self, aid):
        if confirm_delete(self, "Delete this adviser?"):
            try:
                conn = get_conn(); cur = conn.cursor()
                cur.execute("DELETE FROM project_adviser WHERE adviser_id=%s",(aid,))
                cur.execute("DELETE FROM advisers WHERE adviser_id=%s",(aid,))
                conn.commit(); conn.close()
                reset_auto_increment('advisers', 'adviser_id', get_conn)
                self._load()
            except Exception as e: QMessageBox.critical(self,"Error",str(e))

class AdviserDialog(QDialog):
    def __init__(self, parent, aid=None):
        super().__init__(parent); self.aid = aid
        self.setWindowTitle("Edit Adviser" if aid else "Add Adviser"); self.setMinimumWidth(320)
        f = QFormLayout(self); f.setSpacing(12)
        self.name  = QLineEdit(); self.email = QLineEdit()
        f.addRow("Name *", self.name); f.addRow("Email", self.email)
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(self._save); btns.rejected.connect(self.reject); f.addRow(btns)
        if aid: self._load()

    def _load(self):
        try:
            conn = get_conn(); cur = conn.cursor()
            cur.execute("SELECT adviser_name,email FROM advisers WHERE adviser_id=%s",(self.aid,))
            r = cur.fetchone(); conn.close()
            if r: self.name.setText(r[0] or ""); self.email.setText(r[1] or "")
        except Exception as e: QMessageBox.critical(self,"Error",str(e))

    def _save(self):
        n = self.name.text().strip()
        if not n: QMessageBox.warning(self,"Required","Name required."); return
        try:
            conn = get_conn(); cur = conn.cursor()
            vals = (n, self.email.text().strip())
            if self.aid: cur.execute("UPDATE advisers SET adviser_name=%s,email=%s WHERE adviser_id=%s",(*vals,self.aid))
            else:        cur.execute("INSERT INTO advisers (adviser_name,email) VALUES (%s,%s)",vals)
            conn.commit(); conn.close(); self.accept()
        except Exception as e: QMessageBox.critical(self,"Error",str(e))
