from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox)
from config import get_conn
from helpers import make_table, fill_table, confirm_delete, reset_auto_increment

class PanelistsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self); layout.setContentsMargins(24,24,24,24)
        h = QHBoxLayout()
        t = QLabel("Panelists"); t.setObjectName("title")
        h.addWidget(t); h.addStretch()
        btn = QPushButton("+ Add Panelist"); btn.clicked.connect(lambda: self._open(None))
        h.addWidget(btn); layout.addLayout(h); layout.addSpacing(10)
        self.table = make_table(["ID","Name","Email","Actions"], stretch_cols=[1,2])
        layout.addWidget(self.table)

    def _load(self):
        try:
            conn = get_conn(); cur = conn.cursor()
            cur.execute("SELECT panelist_id,panelist_name,email FROM panelists ORDER BY panelist_id DESC")
            rows = cur.fetchall(); conn.close()
            fill_table(self.table, rows, 3, self._open, self._delete)
        except Exception as e: QMessageBox.critical(self,"DB Error",str(e))

    def _open(self, pid):
        if PanelistDialog(self, pid).exec(): self._load()

    def _delete(self, pid):
        if confirm_delete(self, "Delete this panelist?"):
            try:
                conn = get_conn(); cur = conn.cursor()
                cur.execute("DELETE FROM project_panelist WHERE panelist_id=%s",(pid,))
                cur.execute("DELETE FROM panelists WHERE panelist_id=%s",(pid,))
                conn.commit(); conn.close()
                reset_auto_increment('panelists', 'panelist_id', get_conn)
                self._load()
            except Exception as e: QMessageBox.critical(self,"Error",str(e))

class PanelistDialog(QDialog):
    def __init__(self, parent, pid=None):
        super().__init__(parent); self.pid = pid
        self.setWindowTitle("Edit Panelist" if pid else "Add Panelist"); self.setMinimumWidth(320)
        f = QFormLayout(self); f.setSpacing(12)
        self.name = QLineEdit(); self.email = QLineEdit()
        f.addRow("Name *", self.name); f.addRow("Email", self.email)
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(self._save); btns.rejected.connect(self.reject); f.addRow(btns)
        if pid: self._load()

    def _load(self):
        try:
            conn = get_conn(); cur = conn.cursor()
            cur.execute("SELECT panelist_name,email FROM panelists WHERE panelist_id=%s",(self.pid,))
            r = cur.fetchone(); conn.close()
            if r: self.name.setText(r[0] or ""); self.email.setText(r[1] or "")
        except Exception as e: QMessageBox.critical(self,"Error",str(e))

    def _save(self):
        n = self.name.text().strip()
        if not n: QMessageBox.warning(self,"Required","Name required."); return
        try:
            conn = get_conn(); cur = conn.cursor()
            vals = (n, self.email.text().strip())
            if self.pid: cur.execute("UPDATE panelists SET panelist_name=%s,email=%s WHERE panelist_id=%s",(*vals,self.pid))
            else:        cur.execute("INSERT INTO panelists (panelist_name,email) VALUES (%s,%s)",vals)
            conn.commit(); conn.close(); self.accept()
        except Exception as e: QMessageBox.critical(self,"Error",str(e))
