from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox)
from config import get_conn
from helpers import make_table, fill_table, confirm_delete

class TeamsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self); layout.setContentsMargins(24,24,24,24)
        h = QHBoxLayout()
        t = QLabel("Teams"); t.setObjectName("title")
        h.addWidget(t); h.addStretch()
        btn = QPushButton("+ Add Team"); btn.clicked.connect(lambda: self._open(None))
        h.addWidget(btn); layout.addLayout(h); layout.addSpacing(10)
        self.table = make_table(["ID","Team Name","Actions"], stretch_cols=[1])
        layout.addWidget(self.table)

    def _load(self):
        try:
            conn = get_conn(); cur = conn.cursor()
            cur.execute("SELECT team_id,team_name FROM team ORDER BY team_id DESC")
            rows = cur.fetchall(); conn.close()
            fill_table(self.table, rows, 2, self._open, self._delete)
        except Exception as e: QMessageBox.critical(self,"DB Error",str(e))

    def _open(self, tid):
        if TeamDialog(self, tid).exec(): self._load()

    def _delete(self, tid):
        if confirm_delete(self, "Delete this team?"):
            try:
                conn = get_conn(); cur = conn.cursor()
                cur.execute("DELETE FROM team_member WHERE team_id=%s",(tid,))
                cur.execute("DELETE FROM team WHERE team_id=%s",(tid,))
                conn.commit(); conn.close(); self._load()
            except Exception as e: QMessageBox.critical(self,"Error",str(e))

class TeamDialog(QDialog):
    def __init__(self, parent, tid=None):
        super().__init__(parent); self.tid = tid
        self.setWindowTitle("Edit Team" if tid else "Add Team"); self.setMinimumWidth(300)
        f = QFormLayout(self); f.setSpacing(12)
        self.name = QLineEdit()
        f.addRow("Team Name *", self.name)
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(self._save); btns.rejected.connect(self.reject); f.addRow(btns)
        if tid: self._load()

    def _load(self):
        try:
            conn = get_conn(); cur = conn.cursor()
            cur.execute("SELECT team_name FROM team WHERE team_id=%s",(self.tid,))
            r = cur.fetchone(); conn.close()
            if r: self.name.setText(r[0])
        except Exception as e: QMessageBox.critical(self,"Error",str(e))

    def _save(self):
        n = self.name.text().strip()
        if not n: QMessageBox.warning(self,"Required","Team name required."); return
        try:
            conn = get_conn(); cur = conn.cursor()
            if self.tid: cur.execute("UPDATE team SET team_name=%s WHERE team_id=%s",(n,self.tid))
            else:        cur.execute("INSERT INTO team (team_name) VALUES (%s)",(n,))
            conn.commit(); conn.close(); self.accept()
        except Exception as e: QMessageBox.critical(self,"Error",str(e))
