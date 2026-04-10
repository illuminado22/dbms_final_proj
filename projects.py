from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QDialog, QFormLayout, QTextEdit, QComboBox, QDialogButtonBox, QMessageBox)
from config import get_conn
from helpers import make_table, fill_table, confirm_delete

class ProjectsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self); layout.setContentsMargins(24,24,24,24)

        h = QHBoxLayout()
        t = QLabel("Projects"); t.setObjectName("title")
        h.addWidget(t); h.addStretch()
        self.search = QLineEdit(); self.search.setPlaceholderText("Search title or description…"); self.search.setFixedWidth(250)
        self.search.textChanged.connect(self._load)
        h.addWidget(self.search)
        btn = QPushButton("+ Add Project"); btn.clicked.connect(lambda: self._open(None))
        h.addWidget(btn); layout.addLayout(h); layout.addSpacing(10)

        self.table = make_table(["ID","Title","Description","Year","Team","Actions"], stretch_cols=[1,2])
        layout.addWidget(self.table)

    def _load(self):
        q = self.search.text().strip()
        try:
            conn = get_conn(); cur = conn.cursor()
            if q:
                cur.execute("""SELECT p.project_id,p.title,p.description,p.year_completed,t.team_name
                               FROM projects p LEFT JOIN team t ON p.team_id=t.team_id
                               WHERE p.title LIKE %s OR p.description LIKE %s""", (f"%{q}%",f"%{q}%"))
            else:
                cur.execute("""SELECT p.project_id,p.title,p.description,p.year_completed,t.team_name
                               FROM projects p LEFT JOIN team t ON p.team_id=t.team_id ORDER BY p.project_id DESC""")
            rows = cur.fetchall(); conn.close()
            fill_table(self.table, rows, 5, self._open, self._delete)
        except Exception as e: QMessageBox.critical(self,"DB Error",str(e))

    def _open(self, pid):
        if ProjectDialog(self, pid).exec(): self._load()

    def _delete(self, pid):
        if confirm_delete(self, "Delete this project?"):
            try:
                conn = get_conn(); cur = conn.cursor()
                for tbl in ["project_adviser","project_panelist","project_files"]:
                    cur.execute(f"DELETE FROM {tbl} WHERE project_id=%s",(pid,))
                cur.execute("DELETE FROM projects WHERE project_id=%s",(pid,))
                conn.commit(); conn.close(); self._load()
            except Exception as e: QMessageBox.critical(self,"Error",str(e))

class ProjectDialog(QDialog):
    def __init__(self, parent, pid=None):
        super().__init__(parent); self.pid = pid
        self.setWindowTitle("Edit Project" if pid else "Add Project"); self.setMinimumWidth(400)
        f = QFormLayout(self); f.setSpacing(12)
        self.title = QLineEdit()
        self.desc  = QTextEdit(); self.desc.setFixedHeight(80)
        self.year  = QLineEdit(); self.year.setPlaceholderText("e.g. 2024")
        self.team  = QComboBox(); self._load_teams()
        f.addRow("Title *", self.title); f.addRow("Description", self.desc)
        f.addRow("Year", self.year);     f.addRow("Team", self.team)
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(self._save); btns.rejected.connect(self.reject); f.addRow(btns)
        if pid: self._load_data()

    def _load_teams(self):
        try:
            conn = get_conn(); cur = conn.cursor()
            cur.execute("SELECT team_id, team_name FROM team")
            for tid, tname in cur.fetchall(): self.team.addItem(tname, tid)
            conn.close()
        except: pass

    def _load_data(self):
        try:
            conn = get_conn(); cur = conn.cursor()
            cur.execute("SELECT title,description,year_completed,team_id FROM projects WHERE project_id=%s",(self.pid,))
            r = cur.fetchone(); conn.close()
            if r:
                self.title.setText(r[0] or ""); self.desc.setText(r[1] or "")
                self.year.setText(str(r[2]) if r[2] else "")
                idx = self.team.findData(r[3])
                if idx >= 0: self.team.setCurrentIndex(idx)
        except Exception as e: QMessageBox.critical(self,"Error",str(e))

    def _save(self):
        t = self.title.text().strip()
        if not t: QMessageBox.warning(self,"Required","Title is required."); return
        try:
            conn = get_conn(); cur = conn.cursor()
            vals = (t, self.desc.toPlainText().strip(), self.year.text().strip() or None, self.team.currentData())
            if self.pid: cur.execute("UPDATE projects SET title=%s,description=%s,year_completed=%s,team_id=%s WHERE project_id=%s",(*vals,self.pid))
            else:        cur.execute("INSERT INTO projects (title,description,year_completed,team_id) VALUES (%s,%s,%s,%s)",vals)
            conn.commit(); conn.close(); self.accept()
        except Exception as e: QMessageBox.critical(self,"Error",str(e))
